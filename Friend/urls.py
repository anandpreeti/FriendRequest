from django.urls import path
from . import views

app_name='Friend'

urlpatterns = [
	path('', views.homepage, name='homepage'),
    path('signup/', views.signupview, name='signupview'),
    path('login/', views.loginview, name='login'),
    path('logout/', views.logoutview, name='logoutview'),
    path('send_friend_request/<int:userID>/',
     views.send_friend_request, name = 'send friend request'),
    path('accept_friend_request/<int:requestID>/',
    	views.accept_friend_request, name='accept friend request'),
    path('to_accept_friend_request/', views.to_accept_request, name='to accept friend request'),
    path('ajax/requests/', views.postRequest, name="post_request"),
    path('friend_request_details/', views.friend_request_view, name='friend_request_detail'),
    path('api/friend_requests/', views.friend_request_list, name='friend_request_lsit'),
    # path('accepted_friend_request/<int:friendID>/', views.friend_request_accepted, name='accepted_friend_request'),
    path('accepted_friend_request/<int:friendID>/', views.friend_request_accepted, name='accepted_friend_request'),
    path('deleted_friend_request/<int:friendID>/', views.friend_request_deleted, name='deleted_friend_request'),
]