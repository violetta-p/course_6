from django.urls import path
from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, ProfileView, generate_new_password, EmailActivateView, \
    SuccessVerifView, FailedVerifView, SignUpMessageView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/genpassword/', generate_new_password, name='generate_new_password'),
    path('activate/<uidb64>/<token>', EmailActivateView.as_view(), name='activate'),
    path('activate/success/', SuccessVerifView.as_view(), name='success_verification'),
    path('activate/failure/', FailedVerifView.as_view(), name='failed_verification'),
    path('activate/message/', SignUpMessageView.as_view(), name='sign_up_message')
]