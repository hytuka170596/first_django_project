from rest_framework.authentication import (
    TokenAuthentication,
    SessionAuthentication,
    BasicAuthentication,
)
from rest_framework.decorators import api_view
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import ListAPIView, CreateAPIView

from django.contrib.auth.models import Group, User

from myauth.models import Profile
from .serializers import (
    GroupSerializer,
    UserSerializer,
    ArticleSerializer,
    ArticleCreateSerializer,
    ProfileSerializer,
)

from blogapp.models import Article, Author


@api_view()
def hello_world_view(request: Request) -> Response:
    """
    A simple API view that returns a greeting.
    """

    return Response({"message": "Hello World!"})


class GroupsListView(ListAPIView):
    """List of groups"""

    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    ]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class UsersListView(ListAPIView):
    """List of users"""

    authentication_classes = [TokenAuthentication]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class ArticleListView(ListAPIView):
    """List of articles"""

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ArticleCreateView(CreateAPIView):
    """Create an article"""

    queryset = Article.objects.all()
    serializer_class = ArticleCreateSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        author_name = self.request.user.username
        author = Author.objects.get_or_create(name_author=author_name)
        serializer.save(author=author)


class ProfilesListView(ListAPIView):
    """List of profiles"""

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
