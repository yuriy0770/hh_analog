from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.models import Vacancy
from .models import Application


@login_required
def apply_to_vacancy(request, vacancy_id):
    """Откликнуться на вакансию"""
    if request.user.user_type != 'seeker':
        messages.error(request, 'Только соискатели могут откликаться')
        return redirect('main:index')

    vacancy = get_object_or_404(Vacancy, id=vacancy_id, is_active=True)

    # Проверяем, не откликался ли уже
    if Application.objects.filter(vacancy=vacancy, applicant=request.user).exists():
        messages.warning(request, 'Вы уже откликались на эту вакансию')
        return redirect('main:vacancy_detail', vacancy_slug=vacancy.slug)

    if request.method == 'POST':
        cover_letter = request.POST.get('cover_letter', '')

        Application.objects.create(
            vacancy=vacancy,
            applicant=request.user,
            cover_letter=cover_letter
        )

        messages.success(request, '✅ Отклик отправлен!')
        return redirect('main:vacancy_detail', vacancy_slug=vacancy.slug)

    return render(request, 'applications/apply.html', {'vacancy': vacancy})
