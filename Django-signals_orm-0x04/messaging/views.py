from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User


@login_required
def delete_user(request):
    """
    Allows a logged-in user to delete their account.
    After deletion, the post_delete signal will automatically
    clean up related messages, notifications, and histories.
    """
    user = request.user

    # Log the user out before deletion
    logout(request)

    # Delete the user (triggers post_delete signal)
    user.delete()

    return redirect("home")  # redirect anywhere you prefer
