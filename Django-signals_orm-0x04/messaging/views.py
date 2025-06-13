# messaging/views.py

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()

@login_required
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect('home')  # Redirect to home or another desired page


@login_required
def user_conversations(request):
    user = request.user

    # Get top-level messages with prefetch on replies
    messages = Message.objects.filter(
        receiver=user, parent_message__isnull=True
    ).select_related('sender', 'receiver').prefetch_related('replies')

    return render(request, 'messaging/conversations.html', {'messages': messages})


@login_required
def threaded_conversation(request, message_id):
    # Recursively collect all replies to a message
    def get_threaded_replies(message):
        replies = []
        for reply in message.replies.all():
            replies.append({
                'message': reply,
                'replies': get_threaded_replies(reply)
            })
        return replies

    top_message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver').prefetch_related('replies'),
        id=message_id
    )

    thread = {
        'message': top_message,
        'replies': get_threaded_replies(top_message)
    }

    return render(request, 'messaging/thread.html', {'thread': thread})

@login_required
def sent_messages(request):
    messages = Message.objects.filter(
        sender=request.user, parent_message__isnull=True
    ).select_related('receiver').prefetch_related('replies')

    return render(request, 'messaging/sent_messages.html', {'messages': messages})