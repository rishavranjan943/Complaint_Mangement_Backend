from rest_framework import serializers
from .models import Complaint, Department, User

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'email', 'password', 'aadhar_number', 'role')
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'required': False}
        }

    def create(self, validated_data):
        request = self.context.get('request')
        role = validated_data.get('role', 'user')
        if request and request.user.role != 'admin' and role != 'user':
            raise serializers.ValidationError({'role': 'Only admins can assign staff/admin roles.'})
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class ComplaintSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    user_name = serializers.CharField(source='user.username', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Complaint
        fields = '__all__'

    def validate(self, data):
        request = self.context['request']
        if request.user.role == 'admin' and 'user' not in data:
            raise serializers.ValidationError({'user': 'This field is required for admins.'})
        return data

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
