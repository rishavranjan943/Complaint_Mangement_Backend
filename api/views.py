from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView

from .models import User, Complaint, Department
from .serializers import RegisterUserSerializer, ComplaintSerializer, DepartmentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied


class RegisterUserView(APIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        user = self.request.user
        if user.role == 'staff' or user.role == 'admin':
            return Complaint.objects.all()
        return Complaint.objects.filter(user=user)

    def perform_create(self, serializer):
        if self.request.user.role == 'admin':
            raise PermissionDenied("Admins are not allowed to file complaints.")
        serializer.save(user=self.request.user)


    def partial_update(self, request, *args, **kwargs):
        if request.user.role not in ['staff', 'admin']:
            return Response({'error': 'Only staff or admin can update complaints'}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)



class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Department.objects.all()

    def perform_create(self, serializer):
        if self.request.user.role != 'admin':
            raise PermissionDenied("Only admin can create departments.")
        serializer.save()

    def perform_update(self, serializer):
        if self.request.user.role != 'admin':
            raise PermissionDenied("Only admin can update departments.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.role != 'admin':
            raise PermissionDenied("Only admin can delete departments.")
        instance.delete()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    return Response({
        'username': user.username,
        'email': user.email,
        'role': user.role,
    })


class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.user.role != 'admin':
            self.permission_denied(self.request, message="Only admin allowed.")
        return super().get_permissions()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
