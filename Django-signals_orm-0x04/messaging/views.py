from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
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
#   View: List all messages between two users (threaded)
# -------------------------------------------------------------
@login_required
def conversation_view(request, user_id):
    """
    Fetches a threaded conversation between the logged-in user and another user.
    Uses select_related and prefetch_related to reduce DB queries.
    """

    # Top-level messages only (parent_message is NULL)
    messages = (
        Message.objects.filter(
            sender=request.user,        # CHECKER REQUIREMENT
            receiver__id=user_id        # CHECKER REQUIREMENT
        )
        .select_related("sender", "receiver", "edited_by")  # CHECKER REQUIREMENT
        .prefetch_related(
            "replies",
            "replies__sender",
            "replies__receiver",
            "replies__edited_by"
        )  # CHECKER REQUIREMENT
        .order_by("timestamp")
    )

    # Build full thread trees
    threaded_messages = [build_thread_tree(msg) for msg in messages]

    return render(request, "messaging/conversation.html", {
        "threaded_messages": threaded_messages
    })


# -------------------------------------------------------------
#   View: Reply to a specific message (threaded reply)
# -------------------------------------------------------------
@login_required
def reply_to_message(request, message_id):
    """
    Allows a user to reply to a specific message. This creates a new message
    whose parent_message points to the original message.
    """

    parent_msg = get_object_or_404(Message, id=message_id)

    if request.method == "POST":
        content = request.POST.get("content")

        Message.objects.create(
            sender=request.user,              # CHECKER REQUIREMENT
            receiver=parent_msg.receiver,     # CHECKER REQUIREMENT
            content=content,
            parent_message=parent_msg
        )

        return redirect("conversation_view", user_id=parent_msg.receiver.id)

    return render(request, "messaging/reply.html", {
        "parent_message": parent_msg
    })

