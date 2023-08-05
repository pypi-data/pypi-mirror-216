from django.contrib.auth.models import Group
from employee.models import Employee

def user_group(request):
    group_name = None
    if request.user.is_authenticated:
        groups = request.user.groups.all()
        if groups.exists():
            group_name = groups.first().name
    return {'user_group': group_name}


def employee_first_name(request):
    first_name = None
    if request.user.is_authenticated:
        employee = Employee.objects.filter(employeeuser__user=request.user).select_related('employeeuser').first()
        if employee:
            first_name = employee.first_name
    return {'employee_first_name': first_name}