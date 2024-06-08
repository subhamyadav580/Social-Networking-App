from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (
    RegisterSerializer, 
    UserSerializer, 
    LoginSerializer, 
    FriendRequestSerializer,
)
from rest_framework import permissions, authentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authtoken.models import Token
from .models import User, FriendRequest
from rest_framework import status, pagination
from .throttles import FriendRequestThrottle
from django.db.models import Q


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_data = UserSerializer(user, context=self.get_serializer_context()).data
        user_data['user_id'] = user_data['id']
        del user_data['id']
        return Response({
            "message": "User successfully created",
            "user": user_data,
            "token": Token.objects.get(user=user).key
        })


# Login API
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        user_data = UserSerializer(user, context=self.get_serializer_context()).data
        user_data['user_id'] = user_data['id']
        del user_data['id']
        return Response({
            "message": "Logged in successfully",
            "user": user_data,
            "token": Token.objects.get(user=user).key
        })

class FriendList(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request, format=None):
        sent_requests = FriendRequest.objects.filter(from_user=request.user, is_accepted=True).values_list('to_user', flat=True)
        received_requests = FriendRequest.objects.filter(to_user=request.user, is_accepted=True).values_list('from_user', flat=True)
        friend_ids = set(sent_requests).union(set(received_requests))
        friends = User.objects.filter(id__in=friend_ids)
        serializer = UserSerializer(friends, many=True)
        all_data = serializer.data
        if len(all_data) > 0:
            for item in all_data:
                item['user_id'] = item['id']
                del item['id']
            return Response({"friends_list": all_data})
        return Response({"message": "no friends", "friends_list": all_data})
        

class SendFriendRequest(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [FriendRequestThrottle]

    def post(self, request, user_id):
        try:
            to_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        from_user = request.user
        if from_user == to_user:
            return Response({'error': 'You cannot send a friend request to yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
        if created:
            return Response({'message': 'Friend request sent.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Friend request already sent.'}, status=status.HTTP_200_OK)


class AcceptFriendRequest(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id):
        try:
            friend_request = FriendRequest.objects.get(id=request_id)
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend request does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if friend_request.to_user != request.user:
            return Response({'error': 'You cannot accept this friend request.'}, status=status.HTTP_400_BAD_REQUEST)
        
        friend_request.is_accepted = True
        friend_request.save()
        return Response({'message': 'Friend request accepted.'}, status=status.HTTP_200_OK)

class PendingFriendRequests(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        requests = FriendRequest.objects.filter(to_user=request.user, is_accepted=False)
        serializer = FriendRequestSerializer(requests, many=True)
        all_requests = serializer.data
        if len(all_requests) > 0:
            for item in all_requests:
                item['request_id'] = item['id']
                del item['id']
            return Response({"pending_requests": all_requests}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No pending requests", "pending_requests": all_requests}, status=status.HTTP_200_OK)

# Reject Friend Request
class RejectFriendRequest(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id):
        try:
            friend_request = FriendRequest.objects.get(id=request_id)
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend request does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if friend_request.to_user != request.user:
            return Response({'error': 'You cannot reject this friend request.'}, status=status.HTTP_400_BAD_REQUEST)
        
        friend_request.delete()
        return Response({'message': 'Friend request rejected.'}, status=status.HTTP_200_OK)

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


# Search Users
class UserSearch(generics.ListAPIView):
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        keyword = self.request.query_params.get('search', '')
        return User.objects.filter(
            Q(email__iexact=keyword) | Q(full_name__icontains=keyword)
        )
