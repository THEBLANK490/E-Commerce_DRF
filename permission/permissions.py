from rest_framework.permissions import BasePermission

class Is_User(BasePermission):    
    def has_object_permission(self, request,view, obj):
        return request.user == obj
    
class AllowOnlyAuthorized(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        elif request.user and (request.user.role =="STAFF" or request.user.roll == "ADMIN"):
            return True
        return False
    
class IsAdmin(BasePermission):
    def has_permission(self,request,view):
        return bool(request.user and request.user.role=="ADMIN")
    
class AllowAny(BasePermission):
    def has_permission(self, request, view):
        return True

class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
    

