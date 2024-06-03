from django.shortcuts import render, get_object_or_404, redirect
from .models import ChatRoom, ChatMessage
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

@login_required
def chat_room_list(request):
    rooms = ChatRoom.objects.all()
    return render(request, 'chat/room_list.html', {'rooms': rooms})

@login_required
def chat_room(request, room_name):
    room = get_object_or_404(ChatRoom, name=room_name)
    messages = ChatMessage.objects.filter(room=room).order_by('timestamp')
    return render(request, 'chat/room.html', {
        'room': room,
        'messages': messages,
    })

@login_required
@csrf_protect
def create_room(request):
    chat_room = get_object_or_404(ChatRoom, Participants=request.user)
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        print ('room_name')
        if room_name:
            room, created = ChatRoom.objects.get_or_create(name=room_name)
            print ('room')
            if created:
                room.Participants.add(request.user)
                room.save()
                return redirect('chat_room', room_name=room.name)
            else:
                return redirect('chat_room', room_name=room.name)
    return render(request, 'chat/create_room.html')
