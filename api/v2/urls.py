from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from api.v2.views import only_with_token, registrar


app_name = 'v2'
urlpatterns = [
    path('registrar/', registrar, name='registrar'),
    path('login/', obtain_auth_token, name='api-token-auth'),
    path('valid_token/', only_with_token, name='valid_token'),
]
