from http import HTTPStatus

import pytest

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.shortcuts import resolve_url


User = get_user_model()

client = APIClient

CONTENT_TYPE = 'application/json'

HTTP_METHODS = {
    'get': client().get,
    'post': client().post,
    'put': client().put,
    'patch': client().patch,
    'delete': client().delete
}

@pytest.fixture
def payload():
    return dict(
        email='test1@email.com',
        password1='123456!!',
        password2='123456!!',
        name='test1',
        phone='1111111',
        institution='UFRJ',
        role='Medico'
    )


def test_register_successfull(client, payload, db):

    resp = client.post(resolve_url('v2:registrar'), data=payload, content_type=CONTENT_TYPE)

    body = resp.json()
    assert resp.status_code == HTTPStatus.CREATED
    payload.pop('password1')
    payload.pop('password2')
    payload['institution'] = payload['institution'].lower()
    payload['role'] = payload['role'].lower()


    for k in payload:
        assert body[k] == payload[k]
    assert 'token' in body


@pytest.mark.parametrize('field, error', [
    ('email', ['This field is required.']),
    ('name', ['This field is required.']),
    ('phone', ['This field is required.']),
    ('institution', ['This field is required.']),
    ('role', ['This field is required.'])
    ]
)
def test_resgiter_missing_fields(field, error, client, payload, db):

    payload.pop(field)

    resp = client.post(resolve_url('v2:registrar'), data=payload, content_type=CONTENT_TYPE)

    body = resp.json()

    assert resp.status_code == HTTPStatus.BAD_REQUEST
    assert body['errors'] == {field: error}


def test_register_invalid_email(client, payload, db):

    payload['email'] = 'test.com'

    resp = client.post(resolve_url('v2:registrar'), data=payload, content_type=CONTENT_TYPE)

    body = resp.json()

    assert resp.status_code == HTTPStatus.BAD_REQUEST
    assert body['errors'] == {'email': ['Enter a valid email address.']}


def test_register_password_dont_mach(client, payload, db):

    payload['password2'] = payload['password1'] + '1'
    resp = client.post(resolve_url('v2:registrar'), data=payload, content_type=CONTENT_TYPE)

    body = resp.json()

    assert resp.status_code == HTTPStatus.BAD_REQUEST
    assert body['errors'] == {'password2': ['The two password fields didn’t match.']}


@pytest.mark.parametrize("method", ['get', 'put', 'patch', 'delete'])
def test_register_not_allowed_method(method, db):

    resp = HTTP_METHODS[method](resolve_url('v2:registrar'), content_type=CONTENT_TYPE)
    assert resp.status_code == HTTPStatus.METHOD_NOT_ALLOWED


def test_view_protegida_without_token(client):

    resp = client.get(resolve_url('v2:view_protegida'), content_type=CONTENT_TYPE)

    assert resp.status_code == HTTPStatus.UNAUTHORIZED
    assert resp['WWW-Authenticate'] == 'Token'


def test_view_protegida_with_token(client, db):

    user = User.objects.create_user(email='test1@email.com', password='123456!!')
    token = Token.objects.create(user=user)

    header = {'HTTP_AUTHORIZATION': f'Token {token}'}

    resp = client.get(resolve_url('v2:view_protegida'),
                      content_type=CONTENT_TYPE,
                      **header)

    assert resp.status_code == HTTPStatus.OK


@pytest.mark.parametrize("method", ['post', 'put', 'patch', 'delete'])
def test_view_protegida_not_allowed_method(client, method, db):

    user = User.objects.create_user(email='test1@email.com', password='123456!!')
    token = Token.objects.create(user=user)

    header = {'HTTP_AUTHORIZATION': f'Token {token}'}

    resp = HTTP_METHODS[method](resolve_url('v2:view_protegida'),
                                content_type=CONTENT_TYPE,
                                **header)
    assert resp.status_code == HTTPStatus.METHOD_NOT_ALLOWED
