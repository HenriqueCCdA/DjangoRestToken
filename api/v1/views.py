from json import loads
from http import HTTPStatus

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from api.v1.forms import LoginForm, RegistroForm


@csrf_exempt
def registrar(request):

    form = RegistroForm(loads(request.body))

    if not form.is_valid():
        return JsonResponse({'error': form.errors})

    username = form.cleaned_data['username']
    email = form.cleaned_data['email']
    password = form.cleaned_data['password1']

    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': { 'username' :f'User {username} already exists'}})

    usuario = User.objects.create_user(username, email=email, password=password)

    if usuario:
        Token.objects.create(user=usuario)

    return HttpResponse(status=204)


@csrf_exempt
def login(request):

    form = LoginForm(loads(request.body))

    if not form.is_valid():
        return JsonResponse({'error': form.errors})

    username = form.cleaned_data['username']
    password = form.cleaned_data['password']

    usuario = authenticate(request, username=username, password=password)

    if not usuario:
        return JsonResponse({'error': 'credenciais estão erradas'})

    token = usuario.auth_token

    if not token:
        return JsonResponse({'error': f'Usuario {username} não possui um token valido'})

    return JsonResponse({'token': f'Token {str(token)}' })


def only_with_token(request):

    token = request.headers.get('Authorization')

    if not token:
        resp = JsonResponse({'error': 'You not have token !!'}, status=HTTPStatus.UNAUTHORIZED)
        resp['WWW-Authenticate'] = 'Token realm="api"'
        return resp

    method, token = token.split()

    if method != 'Token':
        return JsonResponse({'error': 'Wrong method authentication'}, status=HTTPStatus.BAD_REQUEST)

    token = Token.objects.filter(key=token).first()

    if not token:
        return JsonResponse({'error': 'Invalid token !!'})

    return JsonResponse({'data': f'Good news, {token.user} user have a valid token !!'})
