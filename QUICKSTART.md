"""
Quick Start Guide for Vlog Application

This file provides quick commands to get started with the application.
"""

# ====== INSTALLATION ======

# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# ====== SETUP ======

# 3. Run migrations
python manage.py makemigrations
python manage.py migrate

# 4. Initialize sample data
python manage.py initialize_app
# This creates:
#   - Admin user: admin / admin123
#   - Creator user: creator / creator123
#   - 4 sample categories
#   - 4 sample vlogs

# ====== RUN APPLICATION ======

# 5. Start development server
python manage.py runserver

# 6. Visit URLs
# Home: http://localhost:8000/
# Admin: http://localhost:8000/admin/
# Categories: http://localhost:8000/categories/
# Create Vlog: http://localhost:8000/vlog/new/

# ====== USEFUL COMMANDS ======

# Create new superuser
python manage.py createsuperuser

# Collect static files (for production)
python manage.py collectstatic --noinput

# Create database backup
python manage.py dumpdata > backup.json

# Restore database
python manage.py loaddata backup.json

# Clear all data
python manage.py flush

# Run Django shell
python manage.py shell

# Check for issues
python manage.py check

# ====== PROJECT STRUCTURE ======

# Models (Section 1)
# - VlogPost: Title, Video URL, Description, Author, Category, Tags, Thumbnail, Views
# - Category: Name, Slug, Description

# Views (Section 2)
# - VlogListView: List with pagination and search
# - VlogDetailView: Show single vlog
# - VlogCreateView: Create new vlog
# - VlogUpdateView: Edit vlog
# - VlogDeleteView: Delete vlog

# Forms (Section 4)
# - VlogPostForm: Full form for creating/editing
# - VlogPostModalForm: Quick form for modal
# - CategoryForm: Category management

# Templates (Section 3)
# - base.html: Base template with navigation
# - vlog_list.html: List with pagination and filtering
# - vlog_detail.html: Full vlog display
# - vlog_form.html: Create/Edit form
# - category_list.html: Categories display

# URLs (Section 5)
# / - Home
# /vlog/<id>/<slug>/ - Detail
# /vlog/new/ - Create
# /vlog/<id>/edit/ - Edit
# /vlog/<id>/delete/ - Delete
# /categories/ - Categories

# Admin (Section 6)
# /admin/ - Django Admin
# Features: List displays, filters, search, custom actions

# Deployment (Section 7)
# See AWS_DEPLOYMENT.md for Elastic Beanstalk setup

# ====== FEATURES ======

# ✓ Multi-user vlog creation
# ✓ Category management
# ✓ Tag system
# ✓ Pagination (10 per page)
# ✓ Search functionality
# ✓ View counting
# ✓ Custom admin interface
# ✓ Responsive Bootstrap design
# ✓ Video embedding (YouTube, Vimeo)
# ✓ Thumbnail upload
# ✓ Author-only edit/delete
# ✓ Related vlogs suggestions

# ====== API ENDPOINTS ======

# Note: This is a traditional Django app, not a REST API.
# To add API, consider adding:
# - Django REST Framework
# - API endpoints for mobile/JavaScript apps
# - JWT authentication
# - CORS support

# ====== CUSTOMIZATION ======

# 1. Change admin site title
#    Edit vlogapp/admin.py

# 2. Add new fields to VlogPost
#    Update models.py → makemigrations → migrate

# 3. Customize styles
#    Edit vlogapp/static/css/style.css

# 4. Change pagination size
#    Edit vlogapp/views.py (paginate_by = 10)

# 5. Add more features
#    - Comments system
#    - Rating system
#    - Recommendations
#    - User subscriptions

# ====== PRODUCTION CHECKLIST ======

# [ ] Change SECRET_KEY
# [ ] Set DEBUG = False
# [ ] Update ALLOWED_HOSTS
# [ ] Use PostgreSQL instead of SQLite
# [ ] Setup HTTPS/SSL
# [ ] Configure S3 for media files
# [ ] Setup email backend
# [ ] Enable CSRF protection
# [ ] Add logging
# [ ] Setup monitoring
# [ ] Create backup strategy
# [ ] Load test application
# [ ] Security audit

# ====== CONTACT & SUPPORT ======

# For issues or questions:
# - Check README.md
# - Review AWS_DEPLOYMENT.md for deployment help
# - Check Django docs: https://docs.djangoproject.com/
# - Check Bootstrap docs: https://getbootstrap.com/

print("""
═══════════════════════════════════════════════════════════════
           🎬 VLOG APPLICATION - QUICK START GUIDE 🎬
═══════════════════════════════════════════════════════════════

✓ Django Project Structure Created
✓ Models Configured (VlogPost, Category)
✓ Views Implemented (List, Detail, Create, Update, Delete)
✓ Forms Created (VlogPostForm, CategoryForm)
✓ Templates Built (Responsive Bootstrap 5)
✓ Admin Interface Customized
✓ URL Patterns Configured
✓ Static Files & Media Setup
✓ AWS Deployment Guide Provided

═══════════════════════════════════════════════════════════════

NEXT STEPS:

1. Install Dependencies:
   pip install -r requirements.txt

2. Run Migrations:
   python manage.py migrate

3. Initialize Sample Data:
   python manage.py initialize_app

4. Start Server:
   python manage.py runserver

5. Visit:
   - Home: http://localhost:8000/
   - Admin: http://localhost:8000/admin/

═══════════════════════════════════════════════════════════════

TEST ACCOUNTS (after running initialize_app):
- Username: admin
- Password: admin123

═══════════════════════════════════════════════════════════════
""")
