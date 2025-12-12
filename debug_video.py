import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'vlogproject.settings'

import django
django.setup()

from vlogapp.models import VlogPost
from vlogapp.templatetags.vlog_tags import extract_youtube_id, get_video_embed_url, is_youtube

post = VlogPost.objects.first()

print("="*50)
print("DEBUG VIDEO INFO")
print("="*50)
print(f"Post Title: {post.title}")
print(f"Video URL stored: {post.video_url}")
print(f"Is YouTube?: {is_youtube(post.video_url)}")
print(f"Extracted ID: {extract_youtube_id(post.video_url)}")
print(f"Embed URL: {get_video_embed_url(post.video_url)}")
print("="*50)
