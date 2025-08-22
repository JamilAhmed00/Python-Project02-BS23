from django.urls import path
from .views import SignupAPI, signup_page, login_page, logout_page

app_name = 'accounts'

urlpatterns = [
    # API
    path('api/signup/', SignupAPI.as_view(), name='api-signup'),
    # HTML
    path('signup/', signup_page, name='signup'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
]
