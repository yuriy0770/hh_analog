from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Vacancy, Category


def index(request):
    """Главная страница"""

    # Получаем последние вакансии для всех пользователей
    recent_vacancies = Vacancy.objects.filter(is_active=True).order_by('-created_at')[:6]

    # Категории для фильтра
    categories = Category.objects.all()

    context = {
        'recent_vacancies': recent_vacancies,
        'categories': categories,
    }

    return render(request, 'main/index.html', context)


class VacancyListView(ListView):
    """Список всех вакансий"""
    model = Vacancy
    template_name = 'main/vacancy_list.html'
    context_object_name = 'vacancies'
    paginate_by = 10

    def get_queryset(self):
        queryset = Vacancy.objects.filter(is_active=True).select_related('category', 'company')

        # Фильтр по категории
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Фильтр по городу
        city = self.request.GET.get('city')
        if city:
            queryset = queryset.filter(city__icontains=city)

        # Фильтр по типу работы
        work_type = self.request.GET.get('work_type')
        if work_type:
            queryset = queryset.filter(work_type=work_type)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['cities'] = Vacancy.objects.values_list('city', flat=True).distinct()
        context['work_types'] = Vacancy.WorkType.choices
        return context


class VacancyDetailView(DetailView):
    model = Vacancy
    template_name = 'main/vacancy_detail.html'
    context_object_name = 'vacancy'
    slug_url_kwarg = 'vacancy_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Проверяем, авторизован ли пользователь
        if self.request.user.is_authenticated:
            # Для соискателя - проверял ли он уже отклик
            if self.request.user.user_type == 'seeker':
                from applications.models import Application
                context['has_applied'] = Application.objects.filter(
                    vacancy=self.object,
                    applicant=self.request.user
                ).exists()

            # Для работодателя - количество откликов
            elif self.request.user.user_type == 'employer':
                context['applications_count'] = self.object.applications.count()

        return context