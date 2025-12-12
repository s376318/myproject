"""
Admin Configuration for Vlog Application

This module registers the VlogPost and Category models with Django's admin
interface and provides customizations for better management experience.
"""

from django.contrib import admin
from django.utils.html import format_html, mark_safe
from .models import VlogPost, Category
from .forms import VlogPostForm, CategoryForm


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for Category model
    
    Features:
    - Display category name and slug
    - Search by name
    - Filter by creation date
    - Auto-generate slug from name
    """
    list_display = ('name', 'slug', 'created_at', 'vlog_count')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'slug')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description')
        }),
        ('Metadata', {
            'fields': ('slug', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def vlog_count(self, obj):
        """Display number of vlogs in this category"""
        count = obj.vlogs.count()
        return format_html(
            '<span style="background-color: #007bff; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            count
        )
    vlog_count.short_description = 'Vlogs in Category'


@admin.register(VlogPost)
class VlogPostAdmin(admin.ModelAdmin):
    """
    Admin interface for VlogPost model
    
    Features:
    - Display title, author, category, published date, and view count
    - Filter by author, category, and published date
    - Search by title, description, and tags
    - Enable actions for bulk operations
    - Custom display for thumbnail and author
    - Auto-generate slug from title
    - Organize fields into sections (fieldsets)
    """
    
    form = VlogPostForm
    list_display = (
        'title',
        'author',
        'category',
        'published_date',
        'views_count',
        'thumbnail_preview',
        'status_badge'
    )
    list_filter = ('category', 'author', 'published_date', 'created_at')
    search_fields = ('title', 'description', 'tags', 'author__username')
    readonly_fields = ('slug', 'created_at', 'updated_date', 'views_count', 'thumbnail_preview')
    
    # Organize fields into sections
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description')
        }),
        ('Media', {
            'fields': ('video_url', 'thumbnail', 'thumbnail_preview'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('author', 'category', 'tags')
        }),
        ('Publishing', {
            'fields': ('published_date', 'created_at', 'updated_date')
        }),
        ('Statistics', {
            'fields': ('views_count',),
            'classes': ('collapse',)
        }),
    )
    
    # Filter by category for better management
    list_per_page = 20
    date_hierarchy = 'published_date'
    ordering = ('-published_date',)
    actions = ['reset_views', 'publish_vlog', 'delete_vlogs']
    change_list_template = 'admin/vlogapp/vlogpost/change_list.html'
    
    def thumbnail_preview(self, obj):
        """Display thumbnail preview in admin"""
        if obj.thumbnail:
            return format_html(
                '<img src="{}" width="100" height="auto" />',
                obj.thumbnail.url
            )
        return mark_safe('<span style="color: #999;">No image</span>')
    thumbnail_preview.short_description = 'Thumbnail Preview'
    
    def status_badge(self, obj):
        """Display vlog status as a colored badge"""
        from django.utils import timezone
        if obj.published_date > timezone.now():
            color = 'orange'
            status = 'Scheduled'
        else:
            color = 'green'
            status = 'Published'
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            status
        )
    status_badge.short_description = 'Status'
    
    def reset_views(self, request, queryset):
        """Action to reset view count"""
        updated = queryset.update(views_count=0)
        self.message_user(request, f'{updated} vlog(s) had their view count reset.')
    reset_views.short_description = 'Reset view count for selected vlogs'
    
    def publish_vlog(self, request, queryset):
        """Action to update published date to current time"""
        from django.utils import timezone
        updated = queryset.update(published_date=timezone.now())
        self.message_user(request, f'{updated} vlog(s) published.')
    publish_vlog.short_description = 'Publish selected vlogs now'
    
    def delete_vlogs(self, request, queryset):
        """Custom action to delete selected vlogs with confirmation"""
        count = queryset.count()
        queryset.delete()
        self.message_user(
            request, 
            f'✓ {count} vlog(s) successfully deleted.',
            level='success'
        )
    delete_vlogs.short_description = '🗑️ Delete selected vlogs'


# Customize admin site


# Customize admin site appearance
admin.site.site_header = "Vlog Application Admin"
admin.site.site_title = "Vlog Admin"
admin.site.index_title = "Welcome to Vlog Management System"
