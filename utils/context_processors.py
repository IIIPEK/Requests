from django.urls import reverse

def menu_context(request):
    menu = [
        {'title': 'Заявки', 'url': reverse('requests:request_list')},
    ]

    if request.user.is_authenticated:
        menu.append({
            'title': f'Профиль ({request.user.username})',
            'submenu': [
                {'title': 'Профиль', 'url': reverse('accounts:profile')},
                {'title': 'Редактировать', 'url': reverse('accounts:profile_edit')},
                {'title': 'Сменить пароль', 'url': reverse('accounts:password_change')},
                {'title': 'Выход', 'url': reverse('accounts:logout')},
            ]
        })
    else:
        menu.append({
            'title': 'Войти',
            'submenu': [
                {'title': 'Вход', 'url': reverse('accounts:login')},
                {'title': 'Регистрация', 'url': reverse('accounts:register')},
            ]
        })

    return {'menu_items': menu}
