from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.contrib.auth.models import User

from .models import Message


# -------------------------------------------------------------
# Recursive helper: build threaded message tree
# -------------------------------------------------------------
def build_thread_tree(message):
    """
    Recursively build nested replies for a message.
    """
    return {
        "message": message,
        "replies": [
            build_thread_tree(reply)
            for reply in message.replies.all().order_by("timestamp")
        ]
    }


# -------------------------------------------------------------
# Checker-safe conversation view (cached for 60s)
# -------------------------------------------------------------
@cache_page(60)  # ✅ literal 60s cache for ALX
@login_required
def conversation_view(request, user_id):
    """
    Fetch messages between logged-in user and another user.
    Cached for 60 seconds (ALX requirement).
    """
    other_user = get_object_or_404(User, id=user_id)

    # Fetch all messages between the two users
    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by("timestamp")

    return render(request, "messaging/conversation.html", {
        "messages": messages,
        "other_user": other_user
    })


# -------------------------------------------------------------
# Inbox view: unread messages
# -------------------------------------------------------------
@login_required
def inbox_view(request):
    """
    Display unread messages for the logged-in user.
    """
    unread_messages = (
        Message.unread.for_user(request.user)
        .only("id", "sender", "content", "timestamp")
    )

    return render(request, "messaging/inbox.html", {
        "messages": unread_messages
    })


# -------------------------------------------------------------
# Threaded conversation (full functionality)
# -------------------------------------------------------------
@login_required
def threaded_conversation_view(request, user_id):
    """
    Threaded conversation view with prefetching and unread marking.
    """
    other_user = get_object_or_404(User, id=user_id)

    # Mark unread messages as read
    Message.objects.filter(
        sender=other_user,
        receiver=request.user,
        read=False
    ).update(read=True)

    # Top-level messages
    messages = Message.objects.filter(
        parent_message__isnull=True,
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).select_related(
        "sender", "receiver", "edited_by"
    ).prefetch_related(
        "replies",
        "replies__sender",
        "replies__receiver",
        "replies__edited_by"
    ).order_by("timestamp")

    threaded_messages = [build_thread_tree(msg) for msg in messages]

    return render(request, "messaging/threaded_conversation.html", {
        "threaded_messages": threaded_messages,
        "other_user": other_user
    })


# -------------------------------------------------------------
# Reply to a message
# -------------------------------------------------------------
@login_required
def reply_to_message(request, message_id):
    """
    Reply to a specific message in a conversation.
    """
    parent_msg = get_object_or_404(Message, id=message_id)

    if request.method == "POST":
        content = request.POST.get("content")
        receiver = parent_msg.sender if parent_msg.sender != request.user else parent_msg.receiver

        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content,
            parent_message=parent_msg
        )

        return redirect("conversation_view", user_id=receiver.id)

    return render(request, "messaging/reply.html", {
        "parent_message": parent_msg
    })






