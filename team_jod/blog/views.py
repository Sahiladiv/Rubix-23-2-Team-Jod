from django.shortcuts import render
from .models import Blogs
# Create your views here.
def home(request):

    all_blogs = Blogs.objects.all()
    print(all_blogs)
    return render(request, 'blogs.html')

def people_blog(request, q):
    all_blogs = Blogs.objects.all()
    q = q.upper()
    blog_posts = []
    for i in all_blogs:
        if q == i.blog_category: blog_posts.append(i)
    
    print(blog_posts)
    return render(request, 'people_blogs.html', {'blog_posts': blog_posts})

def show_blog(request, id):
    blog = Blogs.objects.get(id = id)
    
    return render(request, 'blog_content.html', {'blog': blog})
    
