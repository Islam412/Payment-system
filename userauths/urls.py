from django.urls import path

from userauths import views , api


app_name = 'userauths'


urlpatterns = [
    path('sign-up/', views.register_view, name='sign-up'),
    path('sign-in/', views.login_view, name='sign-in'),
    path('sign-out/', views.logout_view, name='sign-out'),

    # api
    path('api/register/', api.RegisterAPIView.as_view(), name='api-register'),
]