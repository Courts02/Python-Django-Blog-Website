from django.shortcuts import render, redirect, get_object_or_404  # Import functions for rendering templates and redirecting
from django.contrib.auth.models import User, auth  # Import Django's authentication system
from django.contrib.auth import authenticate  # Import authenticate function for user authentication
from django.contrib import messages  # Import messages to display notifications
from django.contrib.auth.decorators import login_required  # Import decorator for login-required views
from django.conf import settings  # Import settings to use media URLs
from .models import *  # Import all models from the current app
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from .models import Comment, Post  # Explicitly import Comment and Post models

# View for the homepage
def index(request):
    return render(request, "index.html", {
        'posts': Post.objects.filter(user_id=request.user.id).order_by("id").reverse(),  # Fetch user-specific posts
        'top_posts': Post.objects.all().order_by("-likes"),  # Fetch top-liked posts
        'recent_posts': Post.objects.all().order_by("-id"),  # Fetch most recent posts
        'user': request.user,  # Pass the logged-in user to the template
        'media_url': settings.MEDIA_URL  # Include media URL for images
    })

# User signup view
def signup(request):
    if request.method == 'POST':  # Check if the request is a POST request (HTTP request used to send data to a server to create or update a resource.)
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:  # Ensure passwords match
            if User.objects.filter(username=username).exists():  # Check if username exists
                messages.info(request, "Username already Exists")
                return redirect('signup')
            if User.objects.filter(email=email).exists():  # Check if email exists
                messages.info(request, "Email already Exists")
                return redirect('signup')
            else:
                User.objects.create_user(username=username, email=email, password=password).save()  # Create new user
                return redirect('signin')
        else:
            messages.info(request, "Password should match")  # Show error if passwords don't match
            return redirect('signup')

    return render(request, "signup.html")

# User signin view
def signin(request):
    if request.method == 'POST':  # Check if request is POST
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)  # Authenticate user

        if user is not None:
            auth.login(request, user)  # Log in user if authentication is successful
            return redirect("index")
        else:
            messages.info(request, 'Username or Password is incorrect')  # Show error message
            return redirect("signin")

    return render(request, "signin.html")

# User logout view
def logout(request):
    auth.logout(request)  # Logout user
    return redirect('index')

# Blog page view
def blog(request):
    return render(request, "blog.html", {
        'posts': Post.objects.filter(user_id=request.user.id).order_by("id").reverse(),
        'top_posts': Post.objects.all().order_by("-likes"),
        'recent_posts': Post.objects.all().order_by("-id"),
        'user': request.user,
        'media_url': settings.MEDIA_URL
    })

# @login_required  # Ensure only logged-in users can create posts
# def create_post(request):
#     if request.method == "POST":
#         try:
#             # Directly get the form data
#             data = request.POST
#             image = request.FILES.get("image")

#             # Create the new post directly without checking individual fields manually
#             post = Post.objects.create(
#                 postname=data.get("postname", "").strip(),
#                 content=data.get("content", "").strip(),
#                 category=data.get("category", "").strip(),
#                 image=image,
#                 user=request.user
#             )

#             # HTMX request handling (if applicable)
#             if request.headers.get("HX-Request"):
#                 return render(request, "post.html", {"post": post})

#             # Default response for non-HTMX requests
#             return JsonResponse({"success": True, "message": "Post created successfully!"})

#         except Exception as e:
#             # General error response
#             return JsonResponse({"success": False, "error": str(e)}, status=400)

#     # If the method isn't POST, return an error
#     return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)

# logger = logging.getLogger(__name__)

# @login_required  # Ensure only logged-in users can create posts
# def create_post(request):
#     logger.info(f"Request method: {request.method}")  # Log the request method
    
#     if request.method == "POST":
#         try:
#             logger.info("Processing POST request")  # Log that we are processing a POST request
            
#             # Get the form data and file
#             data = request.POST
#             image = request.FILES.get("image")
            
#             # Check that all necessary fields are present
#             postname = data.get("postname", "").strip()
#             content = data.get("content", "").strip()
            
#             if not postname or not content:
#                 logger.warning("Postname or content missing")
#                 return JsonResponse({"success": False, "error": "Postname and content are required."}, status=400)
            
#             # Create the new post
#             post = Post.objects.create(
#                 postname=postname,
#                 content=content,
#                 category=data.get("category", "").strip(),
#                 image=image,
#                 user=request.user
#             )
            
#             # HTMX request handling (if applicable)
#             if request.headers.get("HX-Request"):
#                 return render(request, "post.html", {"post": post})

#             # Default response for non-HTMX requests
#             return JsonResponse({"success": True, "message": "Post created successfully!"})

#         except Exception as e:
#             # General error response
#             logger.error(f"Error creating post: {e}")
#             return JsonResponse({"success": False, "error": str(e)}, status=400)

#     # If the method isn't POST, return an error
#     logger.warning(f"Invalid request method: {request.method}")
#     return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)
   

def create_post(request):
    if request.method == "POST":
        try:
            # Get data from the form
            data = request.POST
            image = request.FILES.get("image")
            postname = request.POST.get("postname")
            content = request.POST.get("content")
            category = request.POST.get("category")

            # Create a new post object and save it to the database
            post = Post.objects.create(
                postname=data.get("postname", "").strip(),
                content=data.get("content", "").strip(),
                category=data.get("category", "").strip(),
                image=image, # Handle optional image upload
                user=request.user # Associate post with the logged-in user
            )

            # return JsonResponse({"success": True, "message": "Post created successfully!"})

        except Exception as e:
            # Handle errors and return an appropriate response
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    # If it's a GET request, render the form template
    return render(request, "form.html")





# Edit user profile
def profileedit(request, id):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']

        user = User.objects.get(id=id)  # Fetch user by ID
        user.first_name = firstname
        user.email = email
        user.last_name = lastname
        user.save()  # Save updated user details
        return profile(request, id)  # Redirect to profile

    return render(request, "profileedit.html", {
        'user': User.objects.get(id=id),  # Fetch user data for editing
    })

# Increase likes on a post
def increaselikes(request, id):
    if request.method == 'POST':
        post = Post.objects.get(id=id)
        post.likes += 1  # Increment likes
        post.save()
    return redirect("index")  # Redirect to homepage

def post(request, id):
    post = get_object_or_404(Post, id=id)
    comments = Comment.objects.filter(post_id=post.id)  # Fetch all comments

    context = {
        "user": request.user,
        "post": post,
        "recent_posts": Post.objects.all().order_by("-id"),  # Fetch recent posts
        "media_url": settings.MEDIA_URL,
        "comments": comments,
        "total_comments": comments.count()  # Count comments efficiently
    }

    return render(request, "post_detail.html", context)

# Save a comment on a post
def savecomment(request, id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        content = request.POST['message']
        Comment(post_id=post.id, user_id=request.user.id, content=content).save()  # Save comment
        return redirect("index")

# Delete a comment
def deletecomment(request, id):
    comment = Comment.objects.get(id=id)
    postid = comment.post.id
    comment.delete()  # Delete the comment
    return post(request, postid)  # Redirect to post details

# Edit a post
def editpost(request, id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        try:
            postname = request.POST['postname']
            content = request.POST['content']
            category = request.POST['category']

            post.postname = postname
            post.content = content
            post.category = category
            post.save()  # Save edited post
        except:
            print("Error")

        return profile(request, request.user.id)  # Redirect to user profile

    return render(request, "postedit.html", {
        'post': post  # Pass post data to template
    })

# Delete a post
def deletepost(request, id):
    Post.objects.get(id=id).delete()  # Delete post
    return profile(request, request.user.id)  # Redirect to profile

# Contact Us page
def contact_us(request):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        obj = Contact(name=name, email=email, subject=subject, message=message)  # Create new contact entry
        obj.save()
        context['message'] = f"Dear {name}, Thanks for your time!"  # Display success message

    return render(request, "contact.html")

def post_list(request):
    posts = Post.objects.all().order_by("-id")
    return render(request, "partials/post_list.html", {"posts": posts})

def profile(request, id):
    user = get_object_or_404(User, id=id)
    return render(request, "profile.html", {"user": user})