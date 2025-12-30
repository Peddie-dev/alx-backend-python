from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message


# -------------------------------------------------------------
#   Recursive function to fetch replies for a message
# -------------------------------------------------------------
def build_thread_tree(message):
    """
    Recursively builds a nested tree structure of replies.
    """
    return {
        "message": message,
        "replies": [
            build_thread_tree(reply)
            for reply in message.replies.all().order_by("timestamp")
        ]
    }


# -------------------------------------------------------------
#   View: Unread inbox messages
# -------------------------------------------------------------
@login_required
def inbox_view(request):
    """
    Displays only unread messages for the logged-in user.
    Uses the custom UnreadMessagesManager with optimized querying.
    """

    unread_messages = Message.unread.for_user(request.user)

    return render(request, "messaging/inbox.html", {
        "messages": unread_messages
    })


# -------------------------------------------------------------
#   View: List all messages between two users (threaded)
# -------------------------------------------------------------
@login_required
def conversation_view(request, user_id):
    """
    Fetches a threaded conversation between the logged-in user
    and another user.
    """

    other_user = get_object_or_404(User, id=user_id)

    # Mark unread messages from this user as read
    Message.objects.filter(
        sender=other_user,
        receiver=request.user,
        read=False
    ).update(read=True)

    # Top-level messages only
    messages = (
        Message.objects.filter(
            parent_message__isnull=True,
            sender__in=[request.user, other_user],
            receiver__in=[request.user, other_user]
        )
        .select_related("sender", "receiver", "edited_by")
        .prefetch_related(
            "replies",
            "replies__sender",
            "replies__receiver",
            "replies__edited_by"
        )
        .order_by("timestamp")
    )

    # Build threaded structure
    threaded_messages = [build_thread_tree(msg) for msg in messages]

    return render(request, "messaging/conversation.html", {
        "threaded_messages": threaded_messages,
        "other_user": other_user
    })


# -------------------------------------------------------------
#   View: Reply to a specific message (threaded reply)
# -------------------------------------------------------------
@login_required
def reply_to_message(request, message_id):
    """
    Allows a user to reply to a specific message.
    """

    parent_msg = get_object_or_404(Message, id=message_id)

    if request.method == "POST":
        content = request.POST.get("content")

        Message.objects.create(
            sender=request.user,
            receiver=parent_msg.sender
            if parent_msg.sender != request.user
            else parent_msg.receiver,
            content=content,
            parent_message=parent_msg
        )

        return redirect(
            "conversation_view",
            user_id=(
                parent_msg.sender.id
                if parent_msg.sender != request.user
                else parent_msg.receiver.id
            )
        )

    return render(request, "messaging/reply.html", {
        "parent_message": parent_msg
    })

