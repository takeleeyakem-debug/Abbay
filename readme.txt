================================================
🎬 ABBAYTV - COMPLETE MEDIA WEBSITE
================================================

Thank you for purchasing AbbayTV! This is a complete,
professional media website for Ethiopian news, programs,
and job listings.

================================================
📋 SYSTEM REQUIREMENTS
================================================

- Windows 7/8/10/11 or MacOS or Linux
- Python 3.7 or higher
- 100MB free disk space
- 512MB RAM minimum
- Modern web browser (Chrome, Firefox, Edge)

================================================
🚀 QUICK START GUIDE
================================================

STEP 1: Install Python
----------------------
Download from: https://www.python.org/downloads/
Make sure to check "Add Python to PATH" during installation.

STEP 2: Setup the Website
-------------------------
Double-click the "setup.bat" file
Wait for installation to complete (about 2-3 minutes)

STEP 3: Start the Website
-------------------------
Double-click the "runsite.bat" file
The website will start and show:
   * Running on http://127.0.0.1:5000

STEP 4: Open in Browser
-----------------------
Open your browser and go to:
   http://localhost:5000

================================================
🔑 LOGIN CREDENTIALS
================================================

ADMIN ACCESS (Full Control):
   Email: admin@abbaytv.com
   Password: admin123

USER ACCESS (Regular User):
   Email: john@example.com
   Password: password123

⚠️ IMPORTANT: Change these passwords after first login!

================================================
📁 FOLDER STRUCTURE
================================================

AbbayTV/
├── app.py              # Main website code
├── run.py              # Starts the website
├── setup.bat           # One-click setup
├── runsite.bat         # One-click launcher
├── requirements.txt    # Python packages
├── instance/           # Database folder
│   └── abbay.db        # Your data (BACKUP THIS!)
├── static/             # Website files
│   ├── css/
│   │   └── style.css   # All styles
│   ├── js/
│   │   └── main.js     # All interactions
│   └── images/         # Your logos & banners
└── templates/          # All pages
    ├── base.html
    ├── index.html      # Homepage
    ├── news.html       # News page
    ├── programs.html   # Programs page
    ├── jobs.html       # Jobs page
    ├── live.html       # Live streaming
    ├── login.html      # Login page
    ├── signup.html     # Registration
    ├── profile.html    # User profile
    └── admin.html      # Admin panel

================================================
👑 ADMIN PANEL - HOW TO MANAGE YOUR SITE
================================================

1. Login with admin account
2. Click "Admin" in top menu
3. You'll see tabs for:

   📰 NEWS TAB
   • Add news articles with YouTube videos
   • Edit existing news
   • Delete news
   • Categorize by Politics, Sports, etc.

   📺 PROGRAMS TAB
   • Add TV programs
   • Upload YouTube episodes
   • Manage program categories

   💼 JOBS TAB
   • Post job opportunities
   • Set job type (Full-time, Remote, etc.)
   • Manage applications

   🔴 LIVE TAB
   • Turn live stream ON/OFF
   • Add YouTube live URL
   • Enable/disable chat

   🏷️ CATEGORIES TAB
   • Create content categories
   • Add icons to categories
   • Organize your content

   👥 USERS TAB
   • View all registered users
   • Make users admin
   • Delete users

================================================
🎨 CUSTOMIZING YOUR SITE
================================================

CHANGING LOGO:
1. Prepare your logo (PNG format)
2. Save as: static/images/logo.png
3. Recommended size: 150x50 pixels

CHANGING BANNER:
1. Prepare banner image
2. Save as: static/images/banner.png
3. Recommended size: 1200x400 pixels

CHANGING COLORS:
Edit static/css/style.css
• Gold color: #FFD700
• Black: #000000
• Background: #0A0A0A

ADDING SOCIAL MEDIA:
Edit templates/base.html
Find the social-links section and add your URLs

================================================
📱 FEATURES INCLUDED
================================================

✓ Black & Gold premium design
✓ Mobile responsive (works on phones)
✓ YouTube video integration
✓ Automatic video thumbnails
✓ Live streaming support
✓ User registration & login
✓ Admin panel (full control)
✓ News categories (Politics, Sports, etc.)
✓ Search & filter functionality
✓ Job posting system
✓ User profiles
✓ Flash messages
✓ Hamburger menu for mobile
✓ Beautiful animations
✓ Database backup ready

================================================
💾 BACKUP YOUR DATA
================================================

Your entire website data is in:
   C:\Users\Eyakem\Desktop\Abbay\instance\abbay.db

TO BACKUP:
1. Copy this file to a safe location
2. That's it! All users, news, programs saved

TO RESTORE:
1. Replace the abbay.db file with your backup
2. Restart the website

================================================
⚠️ TROUBLESHOOTING
================================================

PROBLEM: "Python is not recognized"
SOLUTION: Install Python from python.org

PROBLEM: "Port 5000 already in use"
SOLUTION: Close other programs or change port in run.py

PROBLEM: Can't login
SOLUTION: Run setup.bat again to reset database

PROBLEM: No thumbnails showing
SOLUTION: Check YouTube URLs are correct

PROBLEM: Admin panel not showing
SOLUTION: Login with admin@abbaytv.com

================================================
🚀 GOING LIVE (INTERNET ACCESS)
================================================

To make your site accessible online:

OPTION 1: Local Network
Edit run.py, change to:
   app.run(host='0.0.0.0', port=5000, debug=True)
Access from other devices: http://YOUR-IP:5000

OPTION 2: PythonAnywhere (Free)
1. Create account at pythonanywhere.com
2. Upload files via FTP
3. Follow their Flask setup guide

OPTION 3: Hosting Service
• DigitalOcean
• Heroku
• AWS Elastic Beanstalk

================================================
📞 SUPPORT
================================================

If you need help:
• Check this README first
• Look for error messages in the console
• Make sure Python is installed correctly
• Ensure all files are in the right folders

For custom modifications, contact your developer.

================================================
✅ DELIVERY CONFIRMATION
================================================

You have received:
✓ Complete source code
✓ Working database system
✓ Admin control panel
✓ User registration system
✓ YouTube integration
✓ Live streaming feature
✓ 10+ content categories
✓ Mobile responsive design
✓ Professional black/gold theme
✓ One-click setup & launcher
✓ This documentation

================================================
🎉 THANK YOU FOR PURCHASING ABBAYTV!
================================================

We wish you great success with your Ethiopian media platform!

For questions or support, contact your developer.

Enjoy your new website! 🇪🇹✨

================================================