from app import app, db, User, Category, News, Program, Job
from datetime import datetime

with app.app_context():
    # Create all tables
    db.create_all()
    print("✅ Database created in:", app.instance_path)
    
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
    
    print("\n" + "="*60)
    print("✅ DATABASE INITIALIZATION COMPLETE!")
    print("="*60)
    print(f"\n📁 Database location: {app.instance_path}\\abbay.db")
    print("\n📊 STATISTICS:")
    print(f"   Categories: {Category.query.count()}")
    print(f"   Users: {User.query.count()}")
    print(f"   News: {News.query.count()}")
    print(f"   Programs: {Program.query.count()}")
    print(f"   Jobs: {Job.query.count()}")
    print("\n🔑 LOGIN CREDENTIALS:")
    print("   Admin: admin@abbaytv.com / admin123")
    print("   User:  john@example.com / password123")
    print("="*60)