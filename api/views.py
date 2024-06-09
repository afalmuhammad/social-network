from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import User, FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate

def generate_token_for_user(user):
    # Delete any existing token for the user
    Token.objects.filter(user=user).delete()
    # Create a new token for the user
    token = Token.objects.create(user=user)
    return token.key
# User Registration and Login

class UserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        # Your authentication logic here
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=401)

# Search Users
class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword', '')
        return User.objects.filter(Q(email__iexact=keyword) | Q(username__icontains=keyword))

# Send Friend Request
class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]
    # throttle_classes = [UserSpecificThrottle]

    def post(self, request):
        requester = request.user
        receiver_id = request.data.get('receiver_id')
        if not receiver_id:
            return Response({'error': 'Receiver ID is required'}, status=status.HTTP_400_BAD_REQUEST)
            # Check if requester and receiver are the same
        if requester.id == receiver_id:
            return Response({'error': 'Requester and receiver cannot be the same'},
                            status=status.HTTP_400_BAD_REQUEST)
        existing_friend_request = FriendRequest.objects.filter(requester=requester, receiver__id=receiver_id).first()
        if existing_friend_request:
            if existing_friend_request.status == FriendRequest.PENDING:
                return Response({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)
            elif existing_friend_request.status == FriendRequest.ACCEPTED:
                return Response({'error': 'Requester is already a friend of receiver'},
                                status=status.HTTP_400_BAD_REQUEST)
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests = FriendRequest.objects.filter(requester=requester, created_at__gte=one_minute_ago).count()
        if recent_requests >= 3:
            return Response({'error': 'You can send a maximum of 3 friend request in one minute.Please try after one minute'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        friend_request = FriendRequest(requester=requester, receiver_id=receiver_id)
        friend_request.save()
        return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_201_CREATED)

# Accept/Reject Friend Request
class ManageFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id, action):
        try:
            friend_request = FriendRequest.objects.get(id=request_id, receiver=request.user)
        except:
            return Response({'error': 'Friend request matching query doesnt exist'}, status=status.HTTP_400_BAD_REQUEST)

        if action == 'accept':
            friend_request.status = FriendRequest.ACCEPTED
        elif action == 'reject':
            friend_request.status = FriendRequest.REJECTED
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

        friend_request.save()
        return Response(FriendRequestSerializer(friend_request).data)

# List Friends
class FriendsListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        accepted_requests = FriendRequest.objects.filter(
            Q(requester=user, status=FriendRequest.ACCEPTED) |
            Q(receiver=user, status=FriendRequest.ACCEPTED)
        )
        friend_ids = list(accepted_requests.values_list('requester', flat=True)) + list(
            accepted_requests.values_list('receiver', flat=True))
        return User.objects.filter(id__in=friend_ids).exclude(id=user.id)

# List Pending Friend Requests
class PendingFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(receiver=self.request.user, status=FriendRequest.PENDING)
