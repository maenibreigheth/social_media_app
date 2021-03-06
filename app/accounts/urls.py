from django.urls import path, include
from rest_framework import routers

from .views import UserRelatedView, ActivateUserView

router = routers.DefaultRouter()

router.register('users', UserRelatedView)

app_name = 'user'

urlpatterns = [
    path('', include(router.urls)),
]
