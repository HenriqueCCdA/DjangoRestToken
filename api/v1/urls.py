from django.urls import path

from api.v1.views import login, only_with_token, registrar

app_name = 'v1'

urlpatterns = [
    path('registar/', registrar, name='registrar'),
    path('login/', login, name='login'),
    path('valid_token/', only_with_token, name='valid_token')
]
