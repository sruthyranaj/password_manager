# api/views.py
from users.models import Organizations, OrganizationsUsers
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from users.models import Organizations
from .serializer import UserSerializer, OrganizationSerializer, OrgUserSerializer
from .permissions import IsGETorSuperAdmin, IsPostOrIsAuthenticated, DeleteorEditbyAdminPermission


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    Only super admin can create organization but can be
    listed to all the users while creating account
    """
    queryset = Organizations.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsGETorSuperAdmin]


class OrgUserViewSet(viewsets.ModelViewSet):
    queryset = OrganizationsUsers.objects.all()
    serializer_class = OrgUserSerializer
    permission_classes = [IsPostOrIsAuthenticated]

    def list(self, request):
        """
        List details of users to the authenticated users only user 
        can view details under his own organization
        """
        try:
            orgUser = OrganizationsUsers.objects.get(user=request.user)
        except:
            orgUser = None
        if orgUser:
            queryset = OrganizationsUsers.objects.filter(
                organization=orgUser.organization
            ).all()
            serializer = OrgUserSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response([], status=status.HTTP_200_OK)

    def create(self, request):
        """
        Method to customize user creation by generating hashed 
        password
        """
        user_data = {
            "username": request.data.get("username"),
            "email": request.data.get("email"),
            "first_name": request.data.get("first_name"),
            "last_name": request.data.get("last_name"),
            "password": make_password(
                request.data.get('password'))
        }
        # check organization exist
        org_id = request.data.get("organizationId")
        if org_id:
            try:
                orgObj = Organizations.objects.get(pk=org_id)
            except:
                orgObj = None

            if not orgObj:
                return Response({"status": "failed",
                                 "message": "Organization not found"
                                 }, status=status.HTTP_400_BAD_REQUEST)
        else:
            Response({"status": "failed",
                                "message": "Organization Id not found"
                      }, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            userId = serializer.data.get("id")
            # assign user to organization
            userObj = User.objects.get(pk=userId)
            orgUsr = OrganizationsUsers(organization=orgObj,
                                        user=userObj)
            orgUsr.save()
            # return user data if the user creation is successful
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        # return error message if the user creation fails
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    Provide delete and edit functinality to user
    Only admin role can edit password of other users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [DeleteorEditbyAdminPermission]

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.password = make_password(
                request.data.get('password'))
            instance.save()
            return Response({"status": "success",
                             "message": "password updated"
                             }, status=status.HTTP_200_OK)
        except:
            pass
        return Response({"status": "failed",
                         "message": "Unable to update"
                         }, status=status.HTTP_400_BAD_REQUEST)
