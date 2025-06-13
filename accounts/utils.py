from .models import UserDepartmentRight

def has_department_right(user, department, right_code: str) -> bool:
    return UserDepartmentRight.objects.filter(
        user=user,
        department=department,
        right__name__iexact=right_code
    ).exists()
