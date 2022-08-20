from http import HTTPStatus

from django.contrib.auth import get_user_model
from rest_framework.decorators import (
                                        api_view,
                                        authentication_classes,
                                        permission_classes
                                        )
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from api.v2.forms import RegistroForm
from api.core.models import Profile

User = get_user_model()


@api_view(['POST'])
def registrar(request):

    form = RegistroForm(request.data)

    if not form.is_valid():
        return Response({'errors': _list_errors(form.errors)}, status=HTTPStatus.BAD_REQUEST)

    email = form.cleaned_data['email']
    password = form.cleaned_data['password1']

    name = form.cleaned_data['name']
    phone = form.cleaned_data['phone']
    institution = form.cleaned_data['institution']
    role = form.cleaned_data['role']

    if User.objects.filter(email=email).exists():
        return Response({'errors': [{'email': ['This email already register']}]}, status=HTTPStatus.BAD_REQUEST)

    user = User.objects.create_user(email=email, password=password)
    Profile.objects.create(user=user, name=name, phone=phone, institution=institution, role=role)

    if user:
        Token.objects.create(user=user)

    data = _userToDict(user)

    return Response(data, status=HTTPStatus.CREATED)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def view_protegida(request):
    user = request.user
    return Response({'data': f'Good news, {user} user have a valid token !!'})


class MyObtainAuthToken(ObtainAuthToken):
    '''
    Error response example
    {
    "errors": [
        {
            "username": ["This field is required."]
        },
        {
            "password": ["This field is required."]
        }
    ]
    }
    '''
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return Response({'errors': _list_errors(serializer.errors)}, status=HTTPStatus.BAD_REQUEST)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'id': user.id, 'token': token.key})


def _userToDict(user):
    return {
        'id': user.id,
        'email': user.email,
        'token': user.auth_token.key,
        'name': user.profile.name,
        'phone': user.profile.phone,
        'institution': user.profile.institution,
        'role': user.profile.role,
    }


def _list_errors(errors):
    return [{k: v} for k, v in errors.items()]
