from http import HTTPStatus

from django.contrib.auth.models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token


from api.v2.forms import RegistroForm


@api_view(['POST'])
def registrar(request):

    form = RegistroForm(request.data)

    if not form.is_valid():
        return Response({'error': form.errors}, status=HTTPStatus.BAD_REQUEST)

    username = form.cleaned_data['username']
    email = form.cleaned_data['email']
    password = form.cleaned_data['password1']

    if User.objects.filter(username=username).exists():
        return Response({'error': { 'username' :f'User {username} already exists'}}, status=HTTPStatus.BAD_REQUEST)

    usuario = User.objects.create_user(username, email=email, password=password)

    if usuario:
        Token.objects.create(user=usuario)

    return Response(status=HTTPStatus.NO_CONTENT)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def only_with_token(request):
    user = request.user
    return Response({'data': f'Good news, {user} user have a valid token !!'})
