from django.urls import path
from auth_api.views import UserView, UserLoginView
urlpatterns = [
    path('user/', UserView.as_view(), name='user'),
    path('user/<int:user_id>/', UserView.as_view(), name='user'), 
    path('login/', UserLoginView.as_view(), name='login')
]
