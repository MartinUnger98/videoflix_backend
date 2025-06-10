from django.urls import path
from .views import ActivateUserView, RegisterView, CustomLoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateUserView.as_view(), name='activate-user'),
    path('login/', CustomLoginView.as_view(), name='login'),
]
