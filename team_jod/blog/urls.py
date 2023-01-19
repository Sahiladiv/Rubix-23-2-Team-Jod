from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="Blogs"),
    path('<q>', views.people_blog, name="Blogs of the category"),
    path('blog_post/<id>', views.show_blog, name="Show Blog")
    

]