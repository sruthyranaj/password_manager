from rest_framework import permissions
from .models import OrganizationsUsers

class IsAuthenticated(permissions.BasePermission):        
    
    def has_permission(self, request, view):
        """
        Method to restrict the api access.
        only post method is permitted.
        for accessing other methods user need to be login.
        """

        # Otherwise, only allow authenticated requests
        return request.user and request.user.is_authenticated



class IsGETorSuperAdmin(permissions.BasePermission):        
    
    def has_permission(self, request, view):
        """
        Method to restrict the api access.
        only post method is permitted.
        for accessing other methods user need to be login.
        """
        # allow all POST requests
        if request.method == 'GET':
            return True
        
        # only allow authenticated requests
        # only allow superadmin
        if request.user.is_authenticated and request.user.is_superuser:
            return True       


class IsPostOrIsAuthenticated(permissions.BasePermission):        
    
    def has_permission(self, request, view):
        """
        Method to restrict the api access.
        only post method is permitted.
        for accessing other methods user need to be login.
        """
        # allow all POST requests
        if request.method == 'POST':
            return True
        
        # Otherwise, only allow authenticated requests
        return request.user and request.user.is_authenticated

class DeleteorEditbyAdminPermission(permissions.BasePermission):        
    
    def has_permission(self, request, view):
        """
        Method to restrict the api access.
        only post method is permitted.
        for accessing other methods user need to be login.
        """
        # allow all POST requests
        user_id = view.kwargs.get("pk")
        if request.method == 'DELETE':
            if request.user.is_authenticated:
                if adm_check.same_org_user(request.user, user_id):
                        if adm_check.check_admin(request.user):
                            return True
            # check whether admin is going to delete the user            
            
        
        if request.method == 'PUT':
            if request.user.is_authenticated:
                # Allow If user going to update their own password
                if user_id == request.user.id:
                    return True
                else:
                    if adm_check.same_org_user(request.user, user_id):
                        if adm_check.check_admin(request.user):
                            return True

class AdminChecking:

    def check_admin(self, user):
        """
        Method to check same organizations admin
        """
        if user.is_authenticated:
            l = user.groups.values_list('name',flat = True) # QuerySet Object
            l_as_list = list(l)   
            if 'admin' in l_as_list:
                return True   
        return False
    
    def same_org_user(self, user, user_to_edit_id):
        """
        Method to check users which we are going to edit and the requested 
        user are under same organization
        """
        try:
            orgUser = OrganizationsUsers.objects.get(user=user)
        except:
            orgUser = None
        if orgUser:
            try:
                # check admin of same organization
                org_obj = OrganizationsUsers.objects.get(user__pk=user_to_edit_id)
                if orgUser.organization == org_obj.organization:
                    return True
            except:
                pass
        return False

adm_check = AdminChecking()