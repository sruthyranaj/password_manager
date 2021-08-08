# api/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import Organizations, OrganizationsUsers


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serialize fields of user model
    """
    class Meta:
        model = Organizations
        fields = ('id', 'name', 'address')


class UserSerializer(serializers.ModelSerializer):
    """
    Serialize fields of user model
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'password', 'email')
    


class OrgUserSerializer(serializers.ModelSerializer):
    """
    Serialize fields of user model
    """
    user = UserSerializer(many=False, read_only=True)
    organization = OrganizationSerializer(many=False, read_only=True)

    userId = serializers.CharField(source = "user.id", read_only=True)
    organizationId = serializers.CharField(source = "organization.id")
    username = serializers.CharField(source = "user.username")
    email = serializers.CharField(source = "user.email")
    first_name = serializers.CharField(source = "user.first_name")
    last_name = serializers.CharField(source = "user.last_name")
    password = serializers.CharField(source = "user.password")
    org_name = serializers.CharField(source = "organization.name", read_only=True)


    class Meta:
        model = OrganizationsUsers
        fields = ('userId', 'organizationId', 'user', 'organization', 'username', 'first_name', 'last_name', 'org_name', 'email', 'password')
        

    def validate(self, attrs):
        """
        Method to check the user exist with given username or email
        """

        # get the user object with entered username or email.

        user_obj = User.objects.filter(email=attrs.get("email")).first()
        if user_obj:
            raise serializers.ValidationError("Email already registered")
        return super().validate(attrs)
