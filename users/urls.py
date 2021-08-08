from users.models import Organizations
from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import  OrgUserViewSet, OrganizationViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'user', OrgUserViewSet)
router.register(r'orgainzation', OrganizationViewSet)
router.register(r'manage-user', UserViewSet)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
