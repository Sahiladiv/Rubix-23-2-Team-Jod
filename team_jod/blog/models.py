from django.db import models

class Blogs(models.Model):
    
    blog_title = models.CharField(max_length=200)
    blog_category = models.CharField(max_length=200)
    blog_content = models.CharField(max_length=30000)
    blog_summary = models.CharField(max_length=30000)

