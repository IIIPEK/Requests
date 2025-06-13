from django import template
from accounts.models import UserDepartmentRight, Right, Department

register = template.Library()

@register.filter
def has_right(user, dept_code_right):
    try:
        dept_code, right_code = dept_code_right.split(":")
        return UserDepartmentRight.objects.filter(
            user=user,
            department__code=dept_code,
            right__name__iexact=right_code
        ).exists()
    except:
        return False
