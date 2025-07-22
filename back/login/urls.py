from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserWriteViewSet, AuthRegister, IconViewSet, FollowViewSet, FollowListViewSet, ChangePasswordView, SchoolSerachViewSet, BannerViewSet


router = DefaultRouter()
router.register('post', UserWriteViewSet)
router.register('index', UserViewSet)
router.register('Icon', IconViewSet)
router.register('Banner', BannerViewSet)
router.register('Follow', FollowViewSet)
router.register('FollowList', FollowListViewSet)
router.register('GrandeSearch', SchoolSerachViewSet)

#djoser.views.TokenCreateView = CustomToken



urlpatterns = [
    path('register/', AuthRegister.as_view()),
    path('', include(router.urls)),
    path('change_password/', ChangePasswordView.as_view()),
]