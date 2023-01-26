from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser


class IsCompanyAdmin(permissions.BasePermission):
    """
    Return True if the user is a company admin
    """

    def has_permission(self, request, view):
        if type(request.user) is AnonymousUser or not hasattr(request.user, 'employee'):
            return False
        employee = request.user.employee
        return employee.is_company_admin


class IsEmployee(permissions.BasePermission):
    """
    Return True if the user is an employee (or company admin)
    """

    def has_permission(self, request, view):
        if type(request.user) is AnonymousUser or request.user.employee is None:
            return False
        return True
