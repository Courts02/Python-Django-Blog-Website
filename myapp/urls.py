from . import views  # Import views from the current directory
from django.urls import path  # Import path to define URL patterns

# Define URL patterns for the application
urlpatterns = [
    path("", views.index, name="index"),  # Homepage
    path("blog", views.blog, name="blog"),  # Blog page
    path("signin", views.signin, name="signin"),  # Sign-in page
    path("signup", views.signup, name="signup"),  # Sign-up page
    path("logout", views.logout, name="logout"),  # Logout functionality
    path("create", views.create, name="create"),  # Create a new blog post
    
    # Increase likes for a post (expects an integer ID for the post)
    path("increaselikes/<int:id>", views.increaselikes, name='increaselikes'),
    
    # View user profile (expects an integer ID for the user)
    path("profile/<int:id>", views.profile, name='profile'),
    
    # Edit user profile (expects an integer ID for the user)
    path("profile/edit/<int:id>", views.profileedit, name='profileedit'),
    
    # View a specific blog post (expects an integer post ID)
    path("post/<int:id>", views.post, name="post"),
    
    # Save a comment on a post (expects post ID)
    path("post/comment/<int:id>", views.savecomment, name="savecomment"),
    
    # Delete a comment from a post (expects comment ID)
    path("post/comment/delete/<int:id>", views.deletecomment, name="deletecomment"),
    
    # Edit an existing blog post (expects post ID)
    path("post/edit/<int:id>", views.editpost, name="editpost"),
    
    # Delete a blog post (expects post ID)
    path("post/delete/<int:id>", views.deletepost, name="deletepost"),
    
    # Contact page
    path("contact", views.contact_us, name="contact"),
]
