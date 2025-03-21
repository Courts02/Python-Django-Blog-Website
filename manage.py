#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os  # Importing the os module to interact with the operating system
import sys  # Importing the sys module to access command-line arguments and system functions

def main():
    """Run administrative tasks."""  # A docstring explaining what this function does
    
    # Setting the default Django settings module for the project
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
    
    try:
        # Importing Django's execute_from_command_line function, which processes commands like runserver, migrate, etc.
        from django.core.management import execute_from_command_line  
    except ImportError as exc:
        # If Django is not installed or not found, raise an error with a helpful message
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc  # This 'from exc' part preserves the original ImportError details for debugging
    
    # Execute the command-line utility with the provided system arguments
    execute_from_command_line(sys.argv)

# This ensures that the script runs only if it's executed directly (not when imported as a module)
if __name__ == "__main__":
    main()  # Calls the main function to start Django's management commands

