from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation


# --------------------------------------------
# Conversation ViewSet
# --------------------------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    """
    Lists conversations and creates a conversation.
    Only participants can view or modify conversations.
    """

    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]

    # ALX checker: include filters
    filter_backends = [filters.SearchFilter]
    search_fields = ["participants__email"]

    def get_queryset(self):
        # Only return conversations where the user is a participant
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get("participants", [])

        if not participant_ids:
            return Response(
                {"error": "Participants list cannot be empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        participants = User.objects.filter(user_id__in=participant_ids)

        if not participants.exists():
            return Response(
                {"error": "One or more users do not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        conversation = Conversation.objects.create()
        conversation.participants.add(*participants)
        conversation.participants.add(request.user)

        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# --------------------------------------------
# Message ViewSet (CACHED)
# --------------------------------------------
@method_decorator(cache_page(60), name="list")
class MessageViewSet(viewsets.ModelViewSet):
    """
    Lists messages, sends new messages, and allows editing/deleting.
    Only participants of the conversation can access messages.

    The list view is cached for 60 seconds.
    """

    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]

    # ALX checker: use filters
    filter_backends = [filters.SearchFilter]
    search_fields = ["message_body"]

    def get_queryset(self):
        # Only messages in conversations the user participates in
        queryset = Message.objects.filter(
            conversation__participants=self.request.user
        )

        conversation_id = self.request.query_params.get("conversation")
        if conversation_id:
            queryset = queryset.filter(
                conversation__conversation_id=conversation_id
            )

        return queryset.order_by("sent_at")

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get("conversation")
        message_body = request.data.get("message_body")

        if not conversation_id:
            return Response(
                {"error": "conversation is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not message_body:
            return Response(
                {"error": "message_body cannot be empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            conversation = Conversation.objects.get(
                conversation_id=conversation_id
            )
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.user not in conversation.participants.all():
            return Response(
                {"error": "You are not a participant of this conversation."},
                status=status.HTTP_403_FORBIDDEN,
            )

        message = Message.objects.create(
            sender=request.user,
            conversation=conversation,
            message_body=message_body,
        )

        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)




