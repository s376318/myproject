"""
URL Configuration for vlogapp

Patterns:
- /vlog/ - List all vlogs with pagination
- /vlog/<id>/<slug>/ - View single vlog
- /vlog/new/ - Create new vlog
- /vlog/<id>/edit/ - Edit vlog
- /vlog/<id>/delete/ - Delete vlog
- /categories/ - List all categories
"""

from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    VlogListView,
    VlogDetailView,
    VlogCreateView,
    VlogUpdateView,
    VlogDeleteView,
    CategoryListView,
)

urlpatterns = [
    # Vlog views
    path('', VlogListView.as_view(), name='vlog-list'),
    path('vlog/<int:pk>/<slug:slug>/', VlogDetailView.as_view(), name='vlog-detail'),
    path('vlog/new/', VlogCreateView.as_view(), name='vlog-create'),
    path('vlog/<int:pk>/edit/', VlogUpdateView.as_view(), name='vlog-update'),
    path('vlog/<int:pk>/delete/', VlogDeleteView.as_view(), name='vlog-delete'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    
    # Category views
    path('categories/', CategoryListView.as_view(), name='category-list'),
]
