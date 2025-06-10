from django.urls import path
from .views import ActivateUserView, RegisterView, CustomLoginView, PasswordResetRequestView, PasswordResetCompleteView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateUserView.as_view(), name='activate-user'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(), name='password-reset-complete'),
]
