"""
Models for Vlog Application
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import URLValidator
from django.urls import reverse


class Category(models.Model):
    """Category model for classifying vlogs"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Auto-generate slug from name if not provided"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class VlogPost(models.Model):
    """
    VlogPost Model - Represents a single vlog post
    
    Fields:
    - title: The title of the vlog (max 200 characters)
    - slug: URL-friendly version of the title (auto-generated, unique)
    - video_url: URL to the video (supports YouTube, Vimeo, etc.)
    - description: Detailed description of the vlog content
    - author: Foreign key to Django User model
    - published_date: When the vlog was published
    - updated_date: When the vlog was last updated
    - category: Foreign key to Category model
    - tags: Comma-separated tags for better searchability
    - thumbnail: Optional custom thumbnail image
    - views_count: Track number of views
    - created_at: Auto timestamp when created
    """

    title = models.CharField(
        max_length=200,
        help_text="Enter the title of your vlog"
    )
    
    slug = models.SlugField(
        unique=True,
        help_text="URL-friendly version of the title (auto-generated)"
    )
    
    video_url = models.URLField(
        help_text="Enter the URL of your video (YouTube, Vimeo, etc.)",
        validators=[URLValidator()]
    )
    
    description = models.TextField(
        help_text="Detailed description of your vlog content"
    )
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='vlogs'
    )
    
    published_date = models.DateTimeField(
        help_text="Date when the vlog was published"
    )
    
    updated_date = models.DateTimeField(
        auto_now=True,
        help_text="Automatically updated when the vlog is modified"
    )
    
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='vlogs'
    )
    
    tags = models.CharField(
        max_length=500,
        blank=True,
        help_text="Enter tags separated by commas (e.g., tutorial, beginner, django)"
    )
    
    thumbnail = models.ImageField(
        upload_to='thumbnails/',
        blank=True,
        null=True,
        help_text="Upload a custom thumbnail image for your vlog"
    )
    
    views_count = models.IntegerField(
        default=0,
        help_text="Track the number of times this vlog has been viewed"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-published_date']
        indexes = [
            models.Index(fields=['-published_date']),
            models.Index(fields=['author']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Auto-generate slug from title if not provided"""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return the URL for this vlog"""
        return reverse('vlog-detail', kwargs={'pk': self.id, 'slug': self.slug})

    def get_tags_list(self):
        """Return tags as a list"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

    def increment_views(self):
        """Increment the view count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
