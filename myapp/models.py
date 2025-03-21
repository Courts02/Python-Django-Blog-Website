from django.db import models  # Import Django's model framework
from django.contrib.auth.models import User  # Import Django's built-in User model
from datetime import datetime  # Import datetime module

# Get the current date in "Day Month Year" format (e.g., "20 March 2025")
now = datetime.now()
time = now.strftime("%d %B %Y")

# Post model to store blog posts
class Post(models.Model):
    postname = models.CharField(max_length=600)  # Title of the post
    category = models.CharField(max_length=600)  # Category of the post
    image = models.ImageField(upload_to='images/posts', blank=True, null=True)  # Optional image
    content = models.CharField(max_length=100000)  # Main content of the post
    time = models.CharField(default=time, max_length=100, blank=True)  # Time of creation (default is current time)
    likes = models.IntegerField(null=True, blank=True, default=0)  # Number of likes (default is 0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link post to the user who created it

    def __str__(self):
        return str(self.postname)  # Return post title as string representation

# Comment model to store comments on posts
class Comment(models.Model):
    content = models.CharField(max_length=200)  # Comment text
    time = models.CharField(default=time, max_length=100, blank=True)  # Time of creation
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # Link comment to a post
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link comment to the user who posted it

    def __str__(self):
        return f"{self.id}.{self.content[:20]}..."  # Return first 20 characters of the comment for display

# Contact model to store messages sent via the contact form
class Contact(models.Model):
    name = models.CharField(max_length=600)  # Name of the sender
    email = models.EmailField(max_length=600)  # Email of the sender
    subject = models.CharField(max_length=1000)  # Subject of the message
    message = models.CharField(max_length=10000, blank=True)  # Message content (optional)
