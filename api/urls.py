from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from .token import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



router = DefaultRouter()
router.register(r'complaints', ComplaintViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'users', AdminUserViewSet)  # Admin route to add/view users



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterUserView.as_view()),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('me/', get_user_profile),
]
