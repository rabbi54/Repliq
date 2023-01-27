from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import UserPassesTestMixin

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



class CompanyAdminTest(UserPassesTestMixin):
    def test_func(self):
        if type(self.request.user) is AnonymousUser or not hasattr(self.request.user, 'employee'):
            return False
        employee = self.request.user.employee
        return employee.is_company_admin