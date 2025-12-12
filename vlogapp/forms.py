"""
Forms for Vlog Application
"""

from django import forms
from django.forms import ModelForm
from .models import VlogPost, Category


class VlogPostForm(ModelForm):
    """
    Form for creating and editing VlogPost instances
    
    This form includes fields for:
    - title: The main title of the vlog
    - video_url: URL to the video content
    - description: Detailed description
    - category: Classification category
    - tags: Comma-separated tags
    - thumbnail: Optional custom thumbnail
    - published_date: Publication date and time
    """

    published_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
        }),
        help_text='Select when this vlog should be published'
    )

    class Meta:
        model = VlogPost
        fields = ['title', 'video_url', 'description', 'category', 'tags', 'thumbnail', 'published_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your vlog title',
                'maxlength': '200',
            }),
            'video_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.youtube.com/watch?v=...',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Write a detailed description of your vlog...',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'tutorial, django, python, beginner (comma-separated)',
            }),
            'thumbnail': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
        }

    def clean_tags(self):
        """Validate and clean tags field"""
        tags = self.cleaned_data.get('tags', '')
        # Validate that tags are comma-separated and not too long
        if len(tags) > 500:
            raise forms.ValidationError('Tags field is too long (max 500 characters)')
        return tags


class VlogPostModalForm(forms.ModelForm):
    """
    Lightweight form for creating VlogPost via modal dialog
    Used for quick vlog creation without full page reload
    """

    class Meta:
        model = VlogPost
        fields = ['title', 'video_url', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Vlog title',
            }),
            'video_url': forms.URLInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Video URL',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select form-select-sm',
            }),
        }


class CategoryForm(forms.ModelForm):
    """Form for creating and editing categories"""

    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Category name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Category description (optional)',
            }),
        }
