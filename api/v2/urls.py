from django.urls import path

from api.v2.views import MyObtainAuthToken, view_protegida, registrar


app_name = 'v2'
urlpatterns = [
    path('registrar/', registrar, name='registrar'),
    path('login/', MyObtainAuthToken.as_view(), name='login'),
    path('view_protegida/', view_protegida, name='view_protegida'),
]
