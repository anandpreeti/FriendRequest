
from django.http import HttpResponse, JsonResponse
from django.core import serializers
# from django.contrib.auth.models import User
from .models import User, Friend_Request
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserCreateForm, FriendRequestCreateForm
from .serializers import FriendRequestSerializer
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.shortcuts import get_object_or_404

def signupview(request):
	if request.method == "POST":
		form = UserCreateForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			new_user = authenticate(
				username = form.cleaned_data['username'],
				password = form.cleaned_data['password1'])
			login(request, new_user)
			return HttpResponse('loggedIn')
		else:
			print(request.POST, form.errors)
			return render(request, 'signup.html', {'form': form, 'error': form.errors})
	else:
		form = UserCreateForm()
		return render(request, 'signup.html', {'form': form})

def loginview(request):
	if request.method == "POST":
		user = authenticate(
			request,
			username = request.POST['username'],
			password = request.POST['password'])
		print(request.POST['username'])
		print(request.POST['password'])

		print(user)
		
		if user is not None:
			login(request, user)
			return HttpResponse('login Successful')
			
		else:			
			return HttpResponse('login Unsuccessful')
	else:
		
		return render(request, 'login.html')

def logoutview(request):
	
	logout(request)
	return HttpResponse('logout successful')


def homepage(request):
	return render(request, 'homepage.html')


@login_required
def send_friend_request(request, userID):
	from_user = request.user
	to_user = User.objects.get(id =userID)
	friend_request, created = Friend_Request.objects.get_or_create(
		from_user=from_user, to_user=to_user)
	if created:
		return HttpResponse('friend request sent')
	else:
		return HttpResponse('friend request was already sent')


@login_required
def to_accept_request(request):
	if request.method == 'GET':
		to_user = request.user
		friend_requests =  Friend_Request.objects.filter(to_user = to_user)
		return render(request, 'accept_friend_request.html', {'all_friend_requests': friend_requests})
	else:
		return HttpResponse("Request method is not GET")

@login_required
def accept_friend_request(request, requestID):
	friend_request = Friend_Request.objects.get(id=requestID)
	if friend_request.to_user == request.user:		
		friend_request.to_user.friends.add(friend_request.from_user)
		friend_request.from_user.friends.add(friend_request.to_user)
		friend_request.delete()
		msg = 'Friend Request Accepted'		
	else:		
		msg = 'Friend Request Not Accepted'
	return render(request, 'accepted_friend_request.html', {'msg': msg, 'friend_request': friend_request})

def displayRequests(request):
	form = FriendRequestCreateForm()
	friend_requests = Friend_Request.objects.all()
	return render(request, "index.html", {"form": form, "friend_requests": friend_requests})

def postRequest(request):
	if request.is_ajax and request.method == "POST":
		form = FriendRequestCreateForm(request.POST)
		print(form)
		if form.is_valid():
			instance= form.save()
			ser_instance = serializers.serialize('json', [instance, ])
			return JsonResponse({'instance':ser_instance}, status=200)
		else:
			return JsonResponse({"error": form.errors}, status = 400)
	return JsonResponse({'error':""}, status=400)

@csrf_exempt
def friend_request_list(request):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
    	userID= request.user.id
    	friend_requests = Friend_Request.objects.filter(to_user_id=userID)
    	ids = [friend_request.id for friend_request in friend_requests]
    	from_users = [friend_request.from_user for friend_request in friend_requests]
    	serializer = FriendRequestSerializer(friend_requests, many=True, context={'request': request})
    	for friend_request in friend_requests:
    		friend_request.save()    	  	
    	
    	return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = FriendRequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)



def friend_request_view(request):
	if not request.user.is_authenticated:
		return HttpResponse('Not allowed')

	if request.method == "GET":
		to_user = request.user
		friend_requests = Friend_Request.objects.filter(to_user=to_user)
		
		return render(request, 'new_accept_friend_request.html', {'all_friend_requests': friend_requests})
	else:
		return HttpResponse("Request method is not GET")

def friend_request_accepted(request, friendID):
	
	accepted_friend = get_object_or_404(User, pk=friendID)
	friend_request = get_object_or_404(Friend_Request, from_user_id=friendID)
	friend_request.delete()
	msg = str(request.user) + ' is now friends with ' + str(accepted_friend.username)
	# return render(request, 'accepted_friend_request.html', {'friend': accepted_friend})
	return render(request, 'new_accept_friend_request.html', {'msg': msg})

def friend_request_deleted(request, friendID):	
	accepted_friend = get_object_or_404(User, pk=friendID)
	friend_request = get_object_or_404(Friend_Request, from_user_id=friendID)
	friend_request.delete()
	msg = 'Request from  ' + str(accepted_friend.username)	+ ' was deleted'
	return render(request, 'new_accept_friend_request.html', {'msg': msg})

# def unfriend(request, friendID):	
# 	from_user = get_object_or_404(User, pk=friendID)
# 	friend_request = get_object_or_404(Friend_Request, to_user_id = request.user.id, from_user_id = friendID)
# 	if not friend_request:
# 		friend_request = get_object_or_404(Friend_Request, from_user_id = request.user.id, to_user_id = friendID)
# 	friend_request.delete()
# 	msg = ' You have successfully unfriended '+ str(from_user.username)

# def is_mutual_friend(request, otherID):
# 	other_user = get_object_or_404(User, pk=otherID)
	

		
