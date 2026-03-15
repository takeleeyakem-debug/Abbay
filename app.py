from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from datetime import datetime
import os
import os

# Database configuration
database_url = os.environ.get('DATABASE_URL', 'sqlite:///instance/abbay.db')

# Fix for Render PostgreSQL URL (starts with postgres://)
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
import os

# Ensure instance folder exists
os.makedirs(os.path.join(os.path.dirname(__file__), 'instance'), exist_ok=True)
import re
import json

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-this')

# Fix database path - absolute path to instance folder
basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')
os.makedirs(instance_path, exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(instance_path, 'abbay.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_youtube_id(url):
    """Extract YouTube video ID from URL"""
    if not url:
        return None
    patterns = [
        r'youtube\.com/watch\?v=([^&]+)',
        r'youtu\.be/([^?]+)',
        r'youtube\.com/embed/([^?]+)',
        r'youtube\.com/v/([^?]+)',
        r'youtube\.com/live/([^?]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_youtube_thumbnail(url):
    """Get YouTube thumbnail URL"""
    video_id = get_youtube_id(url)
    if video_id:
        return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    return None

def get_youtube_embed(url):
    """Get YouTube embed URL"""
    video_id = get_youtube_id(url)
    if video_id:
        return f"https://www.youtube.com/embed/{video_id}"
    return url

def time_ago(date):
    """Convert datetime to time ago string (like Instagram)"""
    now = datetime.utcnow()
    diff = now - date
    
    if diff.days > 365:
        years = diff.days // 365
        return f"{years}y"
    elif diff.days > 30:
        months = diff.days // 30
        return f"{months}mo"
    elif diff.days > 0:
        return f"{diff.days}d"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours}h"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes}m"
    else:
        return "Just now"

app.jinja_env.globals.update(
    get_youtube_id=get_youtube_id,
    get_youtube_thumbnail=get_youtube_thumbnail,
    get_youtube_embed=get_youtube_embed,
    time_ago=time_ago
)

# ============================================
# DATABASE MODELS
# ============================================

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    bio = db.Column(db.String(200), default='')
    profile_pic = db.Column(db.String(200), default='default.jpg')
    is_verified = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    news_comments = db.relationship('NewsComment', backref='author', lazy=True, cascade='all, delete-orphan')
    program_comments = db.relationship('ProgramComment', backref='author', lazy=True, cascade='all, delete-orphan')
    news_likes = db.relationship('NewsLike', backref='user', lazy=True, cascade='all, delete-orphan')
    program_likes = db.relationship('ProgramLike', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    icon = db.Column(db.String(20), default='📰')
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    youtube_url = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False, default=1)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    views = db.Column(db.Integer, default=0)
    tags = db.Column(db.String(200), default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    author = db.relationship('User', backref='news_posts')
    category = db.relationship('Category')
    comments = db.relationship('NewsComment', backref='post', lazy=True, cascade='all, delete-orphan', order_by='NewsComment.created_at.desc()')
    likes = db.relationship('NewsLike', backref='post', lazy=True, cascade='all, delete-orphan')
    
    @property
    def like_count(self):
        return len(self.likes)
    
    @property
    def comment_count(self):
        return len(self.comments)
    
    def is_liked_by(self, user):
        if not user.is_authenticated:
            return False
        return NewsLike.query.filter_by(user_id=user.id, post_id=self.id).first() is not None

class Program(db.Model):
    __tablename__ = 'programs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    youtube_url = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False, default=1)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    views = db.Column(db.Integer, default=0)
    tags = db.Column(db.String(200), default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    author = db.relationship('User', backref='programs')
    category = db.relationship('Category')
    comments = db.relationship('ProgramComment', backref='post', lazy=True, cascade='all, delete-orphan', order_by='ProgramComment.created_at.desc()')
    likes = db.relationship('ProgramLike', backref='post', lazy=True, cascade='all, delete-orphan')
    
    @property
    def like_count(self):
        return len(self.likes)
    
    @property
    def comment_count(self):
        return len(self.comments)
    
    def is_liked_by(self, user):
        if not user.is_authenticated:
            return False
        return ProgramLike.query.filter_by(user_id=user.id, post_id=self.id).first() is not None

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    job_type = db.Column(db.String(50), default='Full-time')
    salary = db.Column(db.String(100), default='Negotiable')
    category = db.Column(db.String(50), default='General')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Comment Models (Instagram Style)
class NewsComment(db.Model):
    __tablename__ = 'news_comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('news.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('news_comments.id'), nullable=True)  # For replies
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    replies = db.relationship('NewsComment', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')
    
    @property
    def time_ago(self):
        return time_ago(self.created_at)

class ProgramComment(db.Model):
    __tablename__ = 'program_comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('program_comments.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    replies = db.relationship('ProgramComment', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')
    
    @property
    def time_ago(self):
        return time_ago(self.created_at)

# Like Models (Instagram Style)
class NewsLike(db.Model):
    __tablename__ = 'news_likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('news.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'post_id', name='unique_news_like'),)

class ProgramLike(db.Model):
    __tablename__ = 'program_likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'post_id', name='unique_program_like'),)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_required(f):
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('You need admin access to view this page.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# ============================================
# PUBLIC ROUTES
# ============================================

@app.route('/')
def index():
    """Homepage with latest content"""
    latest_news = News.query.order_by(News.created_at.desc()).limit(6).all()
    latest_programs = Program.query.order_by(Program.created_at.desc()).limit(6).all()
    return render_template('index.html', news=latest_news, programs=latest_programs)

@app.route('/news')
def news():
    """News listing with filters"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', 'all')
    search = request.args.get('search', '')
    sort = request.args.get('sort', 'newest')
    
    query = News.query
    
    # Apply category filter
    if category != 'all':
        cat = Category.query.filter_by(slug=category).first()
        if cat:
            query = query.filter_by(category_id=cat.id)
    
    # Apply search
    if search:
        query = query.filter(News.title.contains(search) | News.description.contains(search))
    
    # Apply sorting
    if sort == 'newest':
        query = query.order_by(News.created_at.desc())
    elif sort == 'popular':
        query = query.order_by(News.views.desc())
    elif sort == 'liked':
        query = query.outerjoin(NewsLike).group_by(News.id).order_by(db.func.count(NewsLike.id).desc())
    
    pagination = query.paginate(page=page, per_page=9, error_out=False)
    categories = Category.query.all()
    
    return render_template('news.html', news=pagination.items, pagination=pagination,
                         categories=categories, current_category=category, 
                         current_search=search, current_sort=sort)

@app.route('/news/<int:id>')
def news_detail(id):
    """Single news detail with Instagram-style comments"""
    news_item = News.query.get_or_404(id)
    news_item.views += 1
    db.session.commit()
    
    # Get top-level comments (not replies)
    comments = NewsComment.query.filter_by(post_id=id, parent_id=None).order_by(NewsComment.created_at.desc()).all()
    
    # Get related news
    related_news = News.query.filter(
        News.category_id == news_item.category_id,
        News.id != news_item.id
    ).order_by(News.created_at.desc()).limit(4).all()
    
    return render_template('news-detail.html', news=news_item, comments=comments, related_news=related_news)

@app.route('/programs')
def programs():
    """Programs listing with filters"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', 'all')
    search = request.args.get('search', '')
    sort = request.args.get('sort', 'newest')
    
    query = Program.query
    
    # Apply category filter
    if category != 'all':
        cat = Category.query.filter_by(slug=category).first()
        if cat:
            query = query.filter_by(category_id=cat.id)
    
    # Apply search
    if search:
        query = query.filter(Program.title.contains(search) | Program.description.contains(search))
    
    # Apply sorting
    if sort == 'newest':
        query = query.order_by(Program.created_at.desc())
    elif sort == 'popular':
        query = query.order_by(Program.views.desc())
    elif sort == 'liked':
        query = query.outerjoin(ProgramLike).group_by(Program.id).order_by(db.func.count(ProgramLike.id).desc())
    
    pagination = query.paginate(page=page, per_page=9, error_out=False)
    categories = Category.query.all()
    
    return render_template('programs.html', programs=pagination.items, pagination=pagination,
                         categories=categories, current_category=category, 
                         current_search=search, current_sort=sort)

@app.route('/programs/<int:id>')
def program_detail(id):
    """Single program detail with Instagram-style comments"""
    program = Program.query.get_or_404(id)
    program.views += 1
    db.session.commit()
    
    # Get top-level comments (not replies)
    comments = ProgramComment.query.filter_by(post_id=id, parent_id=None).order_by(ProgramComment.created_at.desc()).all()
    
    # Get related programs
    related_programs = Program.query.filter(
        Program.category_id == program.category_id,
        Program.id != program.id
    ).order_by(Program.created_at.desc()).limit(4).all()
    
    return render_template('program-detail.html', program=program, comments=comments, related_programs=related_programs)

# ============================================
# LIKE ROUTES (Instagram Style)
# ============================================

@app.route('/api/news/<int:id>/like', methods=['POST'])
@login_required
def like_news(id):
    """Like or unlike a news post"""
    news = News.query.get_or_404(id)
    
    # Check if already liked
    like = NewsLike.query.filter_by(user_id=current_user.id, post_id=id).first()
    
    if like:
        # Unlike
        db.session.delete(like)
        db.session.commit()
        return jsonify({'liked': False, 'count': news.like_count})
    else:
        # Like
        like = NewsLike(user_id=current_user.id, post_id=id)
        db.session.add(like)
        db.session.commit()
        return jsonify({'liked': True, 'count': news.like_count})

@app.route('/api/program/<int:id>/like', methods=['POST'])
@login_required
def like_program(id):
    """Like or unlike a program post"""
    program = Program.query.get_or_404(id)
    
    # Check if already liked
    like = ProgramLike.query.filter_by(user_id=current_user.id, post_id=id).first()
    
    if like:
        # Unlike
        db.session.delete(like)
        db.session.commit()
        return jsonify({'liked': False, 'count': program.like_count})
    else:
        # Like
        like = ProgramLike(user_id=current_user.id, post_id=id)
        db.session.add(like)
        db.session.commit()
        return jsonify({'liked': True, 'count': program.like_count})

# ============================================
# COMMENT ROUTES (Instagram Style)
# ============================================

@app.route('/api/news/<int:id>/comment', methods=['POST'])
@login_required
def comment_news(id):
    """Add a comment to a news post"""
    news = News.query.get_or_404(id)
    content = request.json.get('content', '').strip()
    parent_id = request.json.get('parent_id')
    
    if not content:
        return jsonify({'error': 'Comment cannot be empty'}), 400
    
    comment = NewsComment(
        content=content,
        user_id=current_user.id,
        post_id=id,
        parent_id=parent_id
    )
    
    db.session.add(comment)
    db.session.commit()
    
    return jsonify({
        'id': comment.id,
        'content': comment.content,
        'username': current_user.username,
        'time_ago': comment.time_ago,
        'comment_count': news.comment_count
    })

@app.route('/api/program/<int:id>/comment', methods=['POST'])
@login_required
def comment_program(id):
    """Add a comment to a program post"""
    program = Program.query.get_or_404(id)
    content = request.json.get('content', '').strip()
    parent_id = request.json.get('parent_id')
    
    if not content:
        return jsonify({'error': 'Comment cannot be empty'}), 400
    
    comment = ProgramComment(
        content=content,
        user_id=current_user.id,
        post_id=id,
        parent_id=parent_id
    )
    
    db.session.add(comment)
    db.session.commit()
    
    return jsonify({
        'id': comment.id,
        'content': comment.content,
        'username': current_user.username,
        'time_ago': comment.time_ago,
        'comment_count': program.comment_count
    })

@app.route('/api/news/<int:id>/comments')
def get_news_comments(id):
    """Get comments for a news post"""
    news = News.query.get_or_404(id)
    comments = []
    
    for comment in news.comments:
        if comment.parent_id is None:  # Only top-level comments
            replies = []
            for reply in comment.replies:
                replies.append({
                    'id': reply.id,
                    'content': reply.content,
                    'username': reply.author.username,
                    'time_ago': reply.time_ago
                })
            
            comments.append({
                'id': comment.id,
                'content': comment.content,
                'username': comment.author.username,
                'time_ago': comment.time_ago,
                'replies': replies
            })
    
    return jsonify(comments)

@app.route('/api/program/<int:id>/comments')
def get_program_comments(id):
    """Get comments for a program post"""
    program = Program.query.get_or_404(id)
    comments = []
    
    for comment in program.comments:
        if comment.parent_id is None:
            replies = []
            for reply in comment.replies:
                replies.append({
                    'id': reply.id,
                    'content': reply.content,
                    'username': reply.author.username,
                    'time_ago': reply.time_ago
                })
            
            comments.append({
                'id': comment.id,
                'content': comment.content,
                'username': comment.author.username,
                'time_ago': comment.time_ago,
                'replies': replies
            })
    
    return jsonify(comments)

# ============================================
# JOBS ROUTES
# ============================================

@app.route('/jobs')
def jobs():
    """Jobs listing with filters"""
    page = request.args.get('page', 1, type=int)
    job_type = request.args.get('type', 'all')
    search = request.args.get('search', '')
    
    query = Job.query
    if job_type != 'all':
        query = query.filter_by(job_type=job_type)
    if search:
        query = query.filter(Job.title.contains(search) | Job.company.contains(search))
    
    pagination = query.order_by(Job.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    job_types = ['Full-time', 'Part-time', 'Contract', 'Remote', 'Internship']
    
    return render_template('jobs.html', jobs=pagination.items, pagination=pagination,
                         job_types=job_types, current_type=job_type, current_search=search)

@app.route('/jobs/<int:id>')
def job_detail(id):
    """Single job detail"""
    job = Job.query.get_or_404(id)
    return render_template('job-detail.html', job=job)

@app.route('/live')
def live():
    """Live streaming page"""
    live_data = {'live_url': '', 'live_title': 'AbbayTV Live', 'is_live': False, 'chat_enabled': True}
    if os.path.exists('live_config.json'):
        with open('live_config.json', 'r') as f:
            live_data.update(json.load(f))
    return render_template('live.html', live=live_data)

@app.route('/api/live/status')
def live_status():
    """API endpoint for live status"""
    if os.path.exists('live_config.json'):
        with open('live_config.json', 'r') as f:
            return jsonify(json.load(f))
    return jsonify({'is_live': False})

# ============================================
# AUTH ROUTES
# ============================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('index'))
        flash('Invalid email or password.', 'danger')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')
        
        if password != confirm:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('signup'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return redirect(url_for('signup'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('signup'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('signup'))
        
        # First user becomes admin
        is_admin = (User.query.count() == 0)
        
        user = User(
            username=username, 
            email=email,
            is_verified=True,
            is_admin=is_admin
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Signup successful! You can now login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile page"""
    if request.method == 'POST':
        if request.form.get('action') == 'update_profile':
            current_user.username = request.form.get('username')
            current_user.email = request.form.get('email')
            current_user.bio = request.form.get('bio', '')
            db.session.commit()
            flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    user_news = News.query.filter_by(author_id=current_user.id).all()
    user_programs = Program.query.filter_by(author_id=current_user.id).all()
    return render_template('profile.html', user_news=user_news, user_programs=user_programs)

# ============================================
# ADMIN ROUTES
# ============================================

@app.route('/admin')
@admin_required
def admin():
    """Admin dashboard"""
    stats = {
        'users': User.query.count(),
        'news': News.query.count(),
        'programs': Program.query.count(),
        'jobs': Job.query.count(),
        'categories': Category.query.count(),
        'comments': NewsComment.query.count() + ProgramComment.query.count(),
        'likes': NewsLike.query.count() + ProgramLike.query.count()
    }
    return render_template('admin.html', stats=stats,
                         users=User.query.all(),
                         news_items=News.query.all(),
                         programs=Program.query.all(),
                         jobs=Job.query.all(),
                         categories=Category.query.all())

# ============================================
# ADMIN: NEWS CRUD
# ============================================

@app.route('/admin/news/add', methods=['POST'])
@admin_required
def admin_news_add():
    """Add new news"""
    news = News(
        title=request.form.get('title'),
        youtube_url=request.form.get('youtube_url'),
        description=request.form.get('description'),
        category_id=request.form.get('category_id', 1),
        tags=request.form.get('tags', ''),
        author_id=current_user.id
    )
    db.session.add(news)
    db.session.commit()
    flash('News added successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/news/edit/<int:id>', methods=['POST'])
@admin_required
def admin_news_edit(id):
    """Edit news"""
    news = News.query.get_or_404(id)
    news.title = request.form.get('title')
    news.youtube_url = request.form.get('youtube_url')
    news.description = request.form.get('description')
    news.category_id = request.form.get('category_id')
    news.tags = request.form.get('tags', '')
    db.session.commit()
    flash('News updated successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/news/delete/<int:id>', methods=['POST'])
@admin_required
def admin_news_delete(id):
    """Delete news"""
    db.session.delete(News.query.get_or_404(id))
    db.session.commit()
    flash('News deleted successfully!', 'success')
    return redirect(url_for('admin'))

# ============================================
# ADMIN: PROGRAMS CRUD
# ============================================

@app.route('/admin/program/add', methods=['POST'])
@admin_required
def admin_program_add():
    """Add new program"""
    program = Program(
        title=request.form.get('title'),
        youtube_url=request.form.get('youtube_url'),
        description=request.form.get('description'),
        category_id=request.form.get('category_id', 1),
        tags=request.form.get('tags', ''),
        author_id=current_user.id
    )
    db.session.add(program)
    db.session.commit()
    flash('Program added successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/program/edit/<int:id>', methods=['POST'])
@admin_required
def admin_program_edit(id):
    """Edit program"""
    program = Program.query.get_or_404(id)
    program.title = request.form.get('title')
    program.youtube_url = request.form.get('youtube_url')
    program.description = request.form.get('description')
    program.category_id = request.form.get('category_id')
    program.tags = request.form.get('tags', '')
    db.session.commit()
    flash('Program updated successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/program/delete/<int:id>', methods=['POST'])
@admin_required
def admin_program_delete(id):
    """Delete program"""
    db.session.delete(Program.query.get_or_404(id))
    db.session.commit()
    flash('Program deleted successfully!', 'success')
    return redirect(url_for('admin'))

# ============================================
# ADMIN: JOBS CRUD
# ============================================

@app.route('/admin/job/add', methods=['POST'])
@admin_required
def admin_job_add():
    """Add new job"""
    job = Job(
        title=request.form.get('title'),
        company=request.form.get('company'),
        location=request.form.get('location'),
        description=request.form.get('description'),
        job_type=request.form.get('job_type', 'Full-time'),
        salary=request.form.get('salary', 'Negotiable'),
        category=request.form.get('category', 'General')
    )
    db.session.add(job)
    db.session.commit()
    flash('Job added successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/job/edit/<int:id>', methods=['POST'])
@admin_required
def admin_job_edit(id):
    """Edit job"""
    job = Job.query.get_or_404(id)
    job.title = request.form.get('title')
    job.company = request.form.get('company')
    job.location = request.form.get('location')
    job.description = request.form.get('description')
    job.job_type = request.form.get('job_type')
    job.salary = request.form.get('salary')
    job.category = request.form.get('category')
    db.session.commit()
    flash('Job updated successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/job/delete/<int:id>', methods=['POST'])
@admin_required
def admin_job_delete(id):
    """Delete job"""
    db.session.delete(Job.query.get_or_404(id))
    db.session.commit()
    flash('Job deleted successfully!', 'success')
    return redirect(url_for('admin'))

# ============================================
# ADMIN: CATEGORIES CRUD
# ============================================

@app.route('/admin/category/add', methods=['POST'])
@admin_required
def admin_category_add():
    """Add new category"""
    name = request.form.get('name')
    category = Category(
        name=name,
        slug=name.lower().replace(' ', '-'),
        icon=request.form.get('icon', '📰'),
        description=request.form.get('description', '')
    )
    db.session.add(category)
    db.session.commit()
    flash('Category added successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/category/delete/<int:id>', methods=['POST'])
@admin_required
def admin_category_delete(id):
    """Delete category"""
    if id == 1:
        flash('Cannot delete default category.', 'danger')
        return redirect(url_for('admin'))
    db.session.delete(Category.query.get_or_404(id))
    db.session.commit()
    flash('Category deleted successfully!', 'success')
    return redirect(url_for('admin'))

# ============================================
# ADMIN: LIVE STREAM
# ============================================

@app.route('/admin/live/update', methods=['POST'])
@admin_required
def admin_live_update():
    """Update live stream settings"""
    live_data = {
        'live_url': request.form.get('live_url'),
        'live_title': request.form.get('live_title'),
        'live_description': request.form.get('live_description'),
        'is_live': request.form.get('is_live') == 'on',
        'chat_enabled': request.form.get('chat_enabled') == 'on'
    }
    with open('live_config.json', 'w') as f:
        json.dump(live_data, f)
    flash('Live stream settings updated!', 'success')
    return redirect(url_for('admin'))

# ============================================
# ADMIN: USER MANAGEMENT
# ============================================

@app.route('/admin/user/delete/<int:id>', methods=['POST'])
@admin_required
def admin_user_delete(id):
    """Delete user"""
    if current_user.id == id:
        flash('Cannot delete your own account.', 'danger')
        return redirect(url_for('admin'))
    db.session.delete(User.query.get_or_404(id))
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/user/toggle-admin/<int:id>', methods=['POST'])
@admin_required
def admin_user_toggle_admin(id):
    """Toggle admin status"""
    if current_user.id == id:
        flash('Cannot change your own admin status.', 'danger')
        return redirect(url_for('admin'))
    user = User.query.get_or_404(id)
    user.is_admin = not user.is_admin
    db.session.commit()
    flash(f'Admin privileges {"granted" if user.is_admin else "revoked"} for {user.username}.', 'success')
    return redirect(url_for('admin'))

# ============================================
# API ENDPOINTS
# ============================================

@app.route('/api/news/<int:id>')
def api_news_get(id):
    """Get news data for editing"""
    news = News.query.get_or_404(id)
    return jsonify({
        'id': news.id,
        'title': news.title,
        'youtube_url': news.youtube_url,
        'description': news.description,
        'category_id': news.category_id,
        'tags': news.tags
    })

@app.route('/api/program/<int:id>')
def api_program_get(id):
    """Get program data for editing"""
    program = Program.query.get_or_404(id)
    return jsonify({
        'id': program.id,
        'title': program.title,
        'youtube_url': program.youtube_url,
        'description': program.description,
        'category_id': program.category_id,
        'tags': program.tags
    })

@app.route('/api/job/<int:id>')
def api_job_get(id):
    """Get job data for editing"""
    job = Job.query.get_or_404(id)
    return jsonify({
        'id': job.id,
        'title': job.title,
        'company': job.company,
        'location': job.location,
        'description': job.description,
        'job_type': job.job_type,
        'salary': job.salary,
        'category': job.category
    })

# ============================================
# DATABASE INITIALIZATION COMMAND
# ============================================

@app.cli.command("init-db")
def init_db():
    """Initialize database with default data"""
    db.create_all()
    print(f"✅ Database created at: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # Create categories if none exist
    if Category.query.count() == 0:
        categories = [
            {'name': 'General', 'icon': '📰', 'description': 'General news and content'},
            {'name': 'Politics', 'icon': '🏛️', 'description': 'Political news and analysis'},
            {'name': 'Sports', 'icon': '⚽', 'description': 'Sports news and updates'},
            {'name': 'Community', 'icon': '👥', 'description': 'Community events and stories'},
            {'name': 'Business', 'icon': '💼', 'description': 'Business and economy'},
            {'name': 'Technology', 'icon': '💻', 'description': 'Tech news and innovations'},
            {'name': 'Culture', 'icon': '🎭', 'description': 'Ethiopian culture and arts'},
            {'name': 'Education', 'icon': '📚', 'description': 'Educational content'},
            {'name': 'Health', 'icon': '🏥', 'description': 'Health and wellness'},
            {'name': 'Entertainment', 'icon': '🎬', 'description': 'Entertainment news'}
        ]
        for cat in categories:
            db.session.add(Category(
                name=cat['name'],
                slug=cat['name'].lower().replace(' ', '-'),
                icon=cat['icon'],
                description=cat['description']
            ))
        db.session.commit()
        print("✅ Categories created!")
    
    # Create users if none exist
    if User.query.count() == 0:
        admin = User(username='admin', email='admin@abbaytv.com', is_verified=True, is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        
        user = User(username='john_doe', email='john@example.com', is_verified=True, is_admin=False)
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        print("✅ Users created!")
        
        # Get admin for sample data
        admin = User.query.filter_by(email='admin@abbaytv.com').first()
        
        # Create sample news
        politics = Category.query.filter_by(slug='politics').first()
        sports = Category.query.filter_by(slug='sports').first()
        
        news1 = News(
            title='Ethiopia Launches New Development Project',
            youtube_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            description='The Ethiopian government has announced a major infrastructure development project in Addis Ababa. The project aims to boost economic growth and create thousands of jobs.',
            category_id=politics.id if politics else 1,
            author_id=admin.id,
            tags='politics,development,ethiopia',
            views=1500
        )
        db.session.add(news1)
        
        news2 = News(
            title='Ethiopian Athletes Shine in International Competition',
            youtube_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            description='Ethiopian runners have won multiple medals at the international athletics championship, continuing the nation\'s proud tradition of excellence in long-distance running.',
            category_id=sports.id if sports else 1,
            author_id=admin.id,
            tags='sports,athletics,ethiopia',
            views=2300
        )
        db.session.add(news2)
        
        # Create sample programs
        program1 = Program(
            title='Morning Show with Abebe',
            youtube_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            description='Start your day with news, entertainment, and interviews with interesting guests. Hosted by Abebe Kebede.',
            category_id=1,
            author_id=admin.id,
            tags='morning,talk-show,entertainment',
            views=3420
        )
        db.session.add(program1)
        
        program2 = Program(
            title='Tech Talk Ethiopia',
            youtube_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            description='Latest in technology and innovation from Ethiopia and around the world.',
            category_id=6,
            author_id=admin.id,
            tags='tech,innovation,digital',
            views=1870
        )
        db.session.add(program2)
        
        # Create sample jobs
        job1 = Job(
            title='Journalist',
            company='AbbayTV',
            location='Addis Ababa',
            description='Looking for an experienced journalist to cover news and events. Must have strong writing skills and be able to work under pressure.',
            job_type='Full-time',
            salary='Competitive',
            category='Media'
        )
        db.session.add(job1)
        
        job2 = Job(
            title='Video Editor',
            company='Media Corp',
            location='Remote',
            description='Video editing for TV programs and digital content. Experience with Adobe Premiere and After Effects required.',
            job_type='Contract',
            salary='$30-40/hour',
            category='Media'
        )
        db.session.add(job2)
        
        db.session.commit()
        print("✅ Sample content created!")
        
        # Create sample comments and likes
        news_item = News.query.first()
        if news_item:
            comment = NewsComment(
                content='Great news! Thanks for sharing.',
                user_id=user.id,
                post_id=news_item.id
            )
            db.session.add(comment)
            
            like = NewsLike(
                user_id=user.id,
                post_id=news_item.id
            )
            db.session.add(like)
            db.session.commit()
            print("✅ Sample interactions created!")
    
    print("\n" + "="*60)
    print("✅ DATABASE INITIALIZATION COMPLETE!")
    print("="*60)
    print(f"\n📁 Database location: {instance_path}\\abbay.db")
    print("\n📊 STATISTICS:")
    print(f"   Categories: {Category.query.count()}")
    print(f"   Users: {User.query.count()}")
    print(f"   News: {News.query.count()}")
    print(f"   Programs: {Program.query.count()}")
    print(f"   Jobs: {Job.query.count()}")
    print(f"   Comments: {NewsComment.query.count() + ProgramComment.query.count()}")
    print(f"   Likes: {NewsLike.query.count() + ProgramLike.query.count()}")
    print("\n🔑 LOGIN CREDENTIALS:")
    print("   Admin: admin@abbaytv.com / admin123")
    print("   User:  john@example.com / password123")
    print("="*60)

# Create tables automatically when app starts
with app.app_context():
    db.create_all()
    print(f"✅ Database ready at: {instance_path}\\abbay.db")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
