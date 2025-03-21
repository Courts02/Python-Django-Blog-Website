"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin  # Import Django's admin module
from django.urls import path, include  # Import path and include for routing URLs
from django.conf import settings  # Import settings to access MEDIA configurations
from django.conf.urls.static import static  # Import static to serve media files

# Define the URL patterns for the project
urlpatterns = [
    path("admin/", admin.site.urls),  # URL for Django admin panel
    path("", include("myapp.urls")),  # Include URLs from the 'myapp' application
]

# Serve media files during development (not needed in production)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
