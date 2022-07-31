from http import HTTPStatus

from django.contrib.auth.models import User
import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.shortcuts import resolve_url

client = APIClient

CONTENT_TYPE = 'application/json'

HTTP_METHODS = {
    'get': client().get,
    'post': client().post,
    'put': client().put,
    'patch': client().patch,
    'delete': client().delete
}


def test_register_successfull(client, db):

    payload = dict(
        username='test1',
        email='test1@email.com',
        password1='123456!!',
        password2='123456!!'
    )

    resp = client.post(resolve_url('v2:registrar'), data=payload, content_type=CONTENT_TYPE)

    body = resp.json()

    assert resp.status_code == HTTPStatus.CREATED
    assert body['username'] == payload['username']
    assert body['email'] == payload['email']
    assert 'token' in body


def test_register_wrong_email(client, db):

    payload = dict(
        username='test1',
        email='test1',
        password1='123456!!',
        password2='123456!!'
    )

    resp = client.post(resolve_url('v2:registrar'), data=payload, content_type=CONTENT_TYPE)

    body = resp.json()

    assert resp.status_code == HTTPStatus.BAD_REQUEST
    assert body['error'] == {'email': ['Enter a valid email address.']}


def test_register_wrong_password_dont_mach(client, db):

    payload = dict(
        username='test1',
        email='test1@email.com',
        password1='123456!!',
        password2='123455!!'
    )

    resp = client.post(resolve_url('v2:registrar'), data=payload, content_type=CONTENT_TYPE)

    body = resp.json()

    assert resp.status_code == HTTPStatus.BAD_REQUEST
    assert body['error'] == {'password2': ['The two password fields didn’t match.']}


@pytest.mark.parametrize("method", ['get', 'put', 'patch', 'delete'])
def test_register_not_allowed_method(method, db):

    resp = HTTP_METHODS[method](resolve_url('v2:registrar'), content_type=CONTENT_TYPE)
    assert resp.status_code == HTTPStatus.METHOD_NOT_ALLOWED


def test_view_protegida_without_token(client):

    resp = client.get(resolve_url('v2:view_protegida'), content_type=CONTENT_TYPE)

    assert resp.status_code == HTTPStatus.UNAUTHORIZED
    assert resp['WWW-Authenticate'] == 'Token'


def test_view_protegida_with_token(client, db):

    user = User.objects.create_user(username='test1',
                                    email='test1@email.com',
                                    password='123456!!')
    token = Token.objects.create(user=user)

    header = {'HTTP_AUTHORIZATION': f'Token {token}'}

    resp = client.get(resolve_url('v2:view_protegida'),
                      content_type=CONTENT_TYPE,
                      **header)

    assert resp.status_code == HTTPStatus.OK


@pytest.mark.parametrize("method", ['post', 'put', 'patch', 'delete'])
def test_view_protegida_not_allowed_method(client, method, db):

    user = User.objects.create_user(username='test1',
                                    email='test1@email.com',
                                    password='123456!!')
    token = Token.objects.create(user=user)

    header = {'HTTP_AUTHORIZATION': f'Token {token}'}

    resp = HTTP_METHODS[method](resolve_url('v2:view_protegida'),
                                content_type=CONTENT_TYPE,
                                **header)
    assert resp.status_code == HTTPStatus.METHOD_NOT_ALLOWED
