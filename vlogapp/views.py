"""
Views for Vlog Application

This module contains all the views for displaying and managing vlogs:
- VlogListView: Display all vlogs with pagination (10 per page)
- VlogDetailView: Display a single vlog post
- VlogCreateView: Create a new vlog (requires login)
- VlogUpdateView: Edit an existing vlog (author-only)
- VlogDeleteView: Delete a vlog (author-only)
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Q
from .models import VlogPost, Category
from .forms import VlogPostForm, CategoryForm


class VlogListView(ListView):
    """
    Display all vlogs with pagination
    
    Features:
    - Shows 10 vlogs per page
    - Ordered by most recent first
    - Supports filtering by category via query parameters
    - Shows category information
    """
    model = VlogPost
    template_name = 'vlogapp/vlog_list.html'
    context_object_name = 'vlogs'
    paginate_by = 10
    
    def get_queryset(self):
        """Get vlogs and filter by category if specified"""
        queryset = VlogPost.objects.select_related('author', 'category').all()
        
        # Filter by category if provided
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Search functionality
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(tags__icontains=search_query)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Add categories and search info to context"""
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_category'] = self.request.GET.get('category', '')
        return context


class VlogDetailView(DetailView):
    """
    Display a single vlog post with full details
    
    Features:
    - Shows title, description, video, author, published date
    - Displays category and tags
    - Shows view count
    - Automatically increments view count
    """
    model = VlogPost
    template_name = 'vlogapp/vlog_detail.html'
    context_object_name = 'vlog'
    
    def get_object(self, queryset=None):
        """Get vlog by pk and slug"""
        obj = super().get_object(queryset)
        # Increment views when page is accessed
        obj.increment_views()
        return obj
    
    def get_context_data(self, **kwargs):
        """Add related vlogs to context"""
        context = super().get_context_data(**kwargs)
        # Get other vlogs from same category
        context['related_vlogs'] = VlogPost.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:5]
        return context


class VlogCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new vlog post
    
    Features:
    - Requires user to be logged in
    - Auto-sets author to current user
    - Displays form with all fields
    - Modal form included for quick creation
    """
    model = VlogPost
    form_class = VlogPostForm
    template_name = 'vlogapp/vlog_form.html'
    success_url = reverse_lazy('vlog-list')
    
    def form_valid(self, form):
        """Set the author to the current user before saving"""
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        """Add action label for template"""
        context = super().get_context_data(**kwargs)
        context['action'] = 'Create New Vlog'
        context['button_text'] = 'Create Vlog'
        return context


class VlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Edit an existing vlog post
    
    Features:
    - Requires user to be logged in
    - Only author can edit their own vlogs
    - Provides full edit form
    """
    model = VlogPost
    form_class = VlogPostForm
    template_name = 'vlogapp/vlog_form.html'
    
    def test_func(self):
        """Check if user is the author"""
        vlog = self.get_object()
        return self.request.user == vlog.author
    
    def form_valid(self, form):
        """Set the author and update"""
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirect to detail view after update"""
        return self.object.get_absolute_url()
    
    def get_context_data(self, **kwargs):
        """Add action label for template"""
        context = super().get_context_data(**kwargs)
        context['action'] = 'Edit Vlog'
        context['button_text'] = 'Update Vlog'
        return context


class VlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a vlog post
    
    Features:
    - Requires user to be logged in
    - Only author can delete their own vlogs
    - Requires confirmation
    """
    model = VlogPost
    template_name = 'vlogapp/vlog_confirm_delete.html'
    success_url = reverse_lazy('vlog-list')
    
    def test_func(self):
        """Check if user is the author"""
        vlog = self.get_object()
        return self.request.user == vlog.author


class CategoryListView(ListView):
    """
    Display all categories
    """
    model = Category
    template_name = 'vlogapp/category_list.html'
    context_object_name = 'categories'
    
    def get_context_data(self, **kwargs):
        """Add vlog counts for each category"""
        context = super().get_context_data(**kwargs)
        for category in context['categories']:
            category.vlog_count = category.vlogs.count()
        return context
