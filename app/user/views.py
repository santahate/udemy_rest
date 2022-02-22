from rest_framework.generics import CreateAPIView

from .serializers import UserSerializer


class CreateUserView(CreateAPIView):
    """
    Create new user
    """
    serializer_class = UserSerializer
