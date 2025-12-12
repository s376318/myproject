"""
Custom template tags for vlog application
Handles video URL parsing and embedding
"""

from django import template
import re

register = template.Library()


@register.filter
def extract_youtube_id(url):
    """
    Extract YouTube video ID from various URL formats
    
    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    """
    if not url:
        return None
    
    # Pattern 1: youtube.com/watch?v= (with optional query params after)
    pattern1 = r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})(?:&|$)'
    match = re.search(pattern1, url)
    if match:
        return match.group(1)
    
    # Pattern 2: youtu.be/
    pattern2 = r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]{11})(?:\?|$)'
    match = re.search(pattern2, url)
    if match:
        return match.group(1)
    
    # Pattern 3: youtube.com/embed/
    pattern3 = r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})(?:\?|$)'
    match = re.search(pattern3, url)
    if match:
        return match.group(1)
    
    return None


@register.filter
def extract_vimeo_id(url):
    """
    Extract Vimeo video ID from URL
    
    Supports:
    - https://vimeo.com/VIDEO_ID
    - https://player.vimeo.com/video/VIDEO_ID
    """
    if not url:
        return None
    
    # Pattern 1: vimeo.com/
    pattern1 = r'(?:https?://)?(?:www\.)?vimeo\.com/(\d+)'
    match = re.search(pattern1, url)
    if match:
        return match.group(1)
    
    # Pattern 2: player.vimeo.com/video/
    pattern2 = r'(?:https?://)?player\.vimeo\.com/video/(\d+)'
    match = re.search(pattern2, url)
    if match:
        return match.group(1)
    
    return None


@register.filter
def is_youtube(url):
    """Check if URL is YouTube link"""
    if not url:
        return False
    return 'youtube.com' in url or 'youtu.be' in url


@register.filter
def is_vimeo(url):
    """Check if URL is Vimeo link"""
    if not url:
        return False
    return 'vimeo.com' in url


@register.filter(name='get_video_embed_url')
def get_video_embed_url(url, provider=None):
    """
    Get the embed URL for iframe based on video provider
    """
    if not url:
        return None
    
    # YouTube (using youtube-nocookie.com for better privacy and localhost compatibility)
    if 'youtube.com' in url or 'youtu.be' in url:
        video_id = extract_youtube_id(url)
        if video_id:
            return f"https://www.youtube-nocookie.com/embed/{video_id}"
    
    # Vimeo
    elif 'vimeo.com' in url:
        video_id = extract_vimeo_id(url)
        if video_id:
            return f"https://player.vimeo.com/video/{video_id}"
    
    return None


@register.simple_tag
def youtube_embed_url(url):
    """Template tag for getting YouTube embed URL"""
    return get_video_embed_url(url)


@register.simple_tag
def vimeo_embed_url(url):
    """Template tag for getting Vimeo embed URL"""
    return get_video_embed_url(url)
