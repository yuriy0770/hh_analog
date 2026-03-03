from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.models import Company, Vacancy


@login_required
def employer_dashboard(request):
    """Дашборд работодателя"""
    # Проверяем, что пользователь - работодатель
    if request.user.user_type != 'employer':
        messages.error(request, 'Эта страница только для работодателей')
        return redirect('main:index')

    # Пытаемся получить компанию пользователя
    try:
        company = request.user.company
        vacancies = Vacancy.objects.filter(company=company).order_by('-created_at')

        # Считаем статистику
        total_vacancies = vacancies.count()
        active_vacancies = vacancies.filter(is_active=True).count()

        context = {
            'company': company,
            'vacancies': vacancies,
            'total_vacancies': total_vacancies,
            'active_vacancies': active_vacancies,
        }
    except Company.DoesNotExist:
        # Если компании нет - показываем страницу создания
        return redirect('employers:create_company')

    return render(request, 'employers/dashboard.html', context)


@login_required
def create_company(request):
    """Создание компании"""
    if request.user.user_type != 'employer':
        messages.error(request, 'Эта страница только для работодателей')
        return redirect('main:index')

    # Проверяем, нет ли уже компании
    if hasattr(request.user, 'company'):
        messages.warning(request, 'У вас уже есть компания')
        return redirect('employers:dashboard')

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        logo = request.FILES.get('logo')

        if not name or not description:
            messages.error(request, 'Заполните все обязательные поля')
            return render(request, 'employers/create_company.html')

        # Создаем компанию
        company = Company.objects.create(
            name=name,
            description=description,
            logo=logo,
            owner=request.user
        )

        messages.success(request, f'Компания "{company.name}" успешно создана!')
        return redirect('employers:dashboard')

    return render(request, 'employers/create_company.html')


@login_required
def edit_company(request):
    """Редактирование компании"""
    if request.user.user_type != 'employer':
        messages.error(request, 'Эта страница только для работодателей')
        return redirect('main:index')

    try:
        company = request.user.company
    except Company.DoesNotExist:
        return redirect('employers:create_company')

    if request.method == 'POST':
        company.name = request.POST.get('name', company.name)
        company.description = request.POST.get('description', company.description)
        company.logo = request.FILES.get('logo', company.logo)
        company.save()

        messages.success(request, 'Компания обновлена!')
        return redirect('employers:dashboard')

    return render(request, 'employers/edit_company.html', {'company': company})


@login_required
def create_vacancy(request):
    """Создание вакансии"""
    if request.user.user_type != 'employer':
        messages.error(request, 'Эта страница только для работодателей')
        return redirect('main:index')

    try:
        company = request.user.company  # ← Получаем компанию текущего пользователя
    except Company.DoesNotExist:
        messages.error(request, 'Сначала создайте компанию')
        return redirect('employers:create_company')

    from main.models import Category, Vacancy
    from django.utils.text import slugify

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        salary = request.POST.get('salary')
        city = request.POST.get('city')
        work_type = request.POST.get('work_type')
        experience = request.POST.get('experience')
        category_id = request.POST.get('category')

        # Валидация
        if not title or not description or not city:
            messages.error(request, 'Заполните все обязательные поля')
            return redirect('employers:create_vacancy')

        # Генерируем уникальный slug
        base_slug = slugify(title)
        slug = base_slug
        counter = 1

        # Проверяем уникальность slug
        while Vacancy.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        # Создаем вакансию с привязкой к компании
        vacancy = Vacancy.objects.create(
            title=title,
            description=description,
            salary=salary if salary else None,
            city=city,
            work_type=work_type,
            experience=experience,
            category_id=category_id,
            company=company,  # ← ВАЖНО: привязываем к компании
            is_active=True,
            slug=slug  # ← Явно передаем сгенерированный slug
        )

        messages.success(request, f'Вакансия "{vacancy.title}" создана!')
        return redirect('employers:dashboard')

    # GET запрос - показываем форму
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'work_types': Vacancy.WorkType.choices,
        'experiences': Vacancy.Experience.choices,
    }
    return render(request, 'employers/create_vacancy.html', context)


@login_required
def edit_vacancy(request, vacancy_id):
    """Редактирование вакансии"""
    if request.user.user_type != 'employer':
        messages.error(request, 'Эта страница только для работодателей')
        return redirect('main:index')

    try:
        company = request.user.company
        vacancy = Vacancy.objects.get(id=vacancy_id, company=company)
    except (Company.DoesNotExist, Vacancy.DoesNotExist):
        messages.error(request, 'Вакансия не найдена')
        return redirect('employers:dashboard')

    from main.models import Category

    if request.method == 'POST':
        vacancy.title = request.POST.get('title', vacancy.title)
        vacancy.description = request.POST.get('description', vacancy.description)
        vacancy.salary = request.POST.get('salary') if request.POST.get('salary') else None
        vacancy.city = request.POST.get('city', vacancy.city)
        vacancy.work_type = request.POST.get('work_type', vacancy.work_type)
        vacancy.experience = request.POST.get('experience', vacancy.experience)
        vacancy.category_id = request.POST.get('category', vacancy.category_id)
        vacancy.is_active = request.POST.get('is_active') == 'on'
        vacancy.save()

        messages.success(request, 'Вакансия обновлена!')
        return redirect('employers:dashboard')

    categories = Category.objects.all()
    context = {
        'vacancy': vacancy,
        'categories': categories,
        'work_types': Vacancy.WorkType.choices,
        'experiences': Vacancy.Experience.choices,
    }
    return render(request, 'employers/edit_vacancy.html', context)


@login_required
def vacancy_applications(request, vacancy_id):
    """Список откликов на вакансию"""
    if request.user.user_type != 'employer':
        messages.error(request, 'Эта страница только для работодателей')
        return redirect('main:index')

    try:
        company = request.user.company
        vacancy = Vacancy.objects.get(id=vacancy_id, company=company)
        applications = vacancy.applications.all().order_by('-created_at')
    except (Company.DoesNotExist, Vacancy.DoesNotExist):
        messages.error(request, 'Вакансия не найдена')
        return redirect('employers:dashboard')

    context = {
        'vacancy': vacancy,
        'applications': applications,
    }
    return render(request, 'employers/applications.html', context)


@login_required
def respond_application(request, app_id):
    """Ответ на отклик (принять/отклонить)"""
    if request.user.user_type != 'employer':
        messages.error(request, 'Эта страница только для работодателей')
        return redirect('main:index')

    messages.success(request, 'Функция в разработке')
    return redirect('employers:dashboard')
