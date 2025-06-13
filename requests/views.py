from django.contrib.auth.decorators import login_required
from django.db.models import Subquery, OuterRef
from django.shortcuts import render, get_object_or_404, redirect
from .models import Request, RequestStatusHistory, RequestStatus
from .forms import RequestForm
from accounts.models import UserDepartmentRight, Right, Department
from accounts.utils import has_department_right


@login_required
def request_list(request):
    departments = Department.objects.all()
    statuses = RequestStatus.objects.all()
    user_depts = UserDepartmentRight.objects.filter(user=request.user).values_list('department', flat=True).distinct()

    requests_qs = Request.objects.filter(department__in=user_depts)

    # 🔍 Фильтры из GET
    dept_id = request.GET.get('department')
    month = request.GET.get('month')
    year = request.GET.get('year')
    status_code = request.GET.get('status')

    if dept_id:
        requests_qs = requests_qs.filter(department_id=dept_id)
    if month:
        requests_qs = requests_qs.filter(month=month)
    if year:
        requests_qs = requests_qs.filter(year=year)

    if status_code:
        last_status = RequestStatusHistory.objects.filter(
            request=OuterRef('pk')
        ).order_by('-changed_at').values('status__code')[:1]

        requests_qs = requests_qs.annotate(
            last_status_code=Subquery(last_status)
        ).filter(last_status_code=status_code)

    return render(request, 'requests/request_list.html', {
        'requests': requests_qs.order_by('-created_at'),
        'departments': departments,
        'statuses': statuses,
        'filters': {
            'department': dept_id,
            'month': month,
            'year': year,
            'status': status_code,
        }
    })
@login_required
def request_create_or_edit(request, pk=None):
    instance = get_object_or_404(Request, pk=pk) if pk else None

    # if pk and instance.requester != request.user:
    #     return redirect('requests:request_list')
    if pk:
        # Только автор или апрувер в отделе
        print(instance.requester, request.user, instance.department)
        if not (
                instance.requester == request.user or
                has_department_right(request.user, instance.department, 'Approver')
        ):
            return redirect('requests:request_detail', pk=pk)
        last_status = instance.current_status()
        if last_status and last_status.status.code in ('approved', 'done', 'cancelled'):
            return redirect('requests:request_detail', pk=pk)



    if request.method == 'POST':
        form = RequestForm(request.POST, instance=instance)
        if form.is_valid():
            req = form.save(commit=False)
            req.requester = request.user

            if not has_department_right(request.user, req.department, 'Requester') and not has_department_right(request.user, req.department, 'Approver'):
                form.add_error(None, 'У вас нет прав на создание заявки в этом отделе.')
            else:
                req.save()

                # Только при создании (без pk ранее)
                if not pk:
                    draft_status = RequestStatus.objects.get(code='draft')
                    RequestStatusHistory.objects.create(
                        request=req,
                        status=draft_status,
                        changed_by=request.user
                    )

                return redirect('requests:request_list')
    else:
        form = RequestForm(instance=instance)



    return render(request, 'requests/request_form.html', {'form': form, 'edit': pk is not None})


@login_required
def request_detail(request, pk):
    req = get_object_or_404(Request, pk=pk)
    history = req.status_history.all().order_by('-changed_at')

    # Отладка — показать права текущего пользователя в отделе заявки
    user_rights = UserDepartmentRight.objects.filter(
        user=request.user,
        department=req.department
    )
    user_right_names = list(user_rights.values_list('right__name', flat=True))

    return render(request, 'requests/request_detail.html', {
        'request_obj': req,
        'history': history,
        'user_rights': user_rights,
        'user_right_names': user_right_names,
    })

@login_required
def change_request_status(request, pk, new_status):
    req = get_object_or_404(Request, pk=pk)

    if not has_department_right(request.user, req.department, 'Approver'):
        return redirect('requests:request_detail', pk=pk)

    status_obj = get_object_or_404(RequestStatus, code=new_status)

    RequestStatusHistory.objects.create(
        request=req,
        status=status_obj,
        changed_by=request.user
    )

    # TODO: бизнес-логика: присваивание approver, обновление других флагов
    if new_status == 'approved' and req.approver is None:
        req.approver = request.user
        req.save()

    return redirect('requests:request_detail', pk=pk)
