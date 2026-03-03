
from django.utils.html import format_html
from django.contrib import admin
from .models import Company, Category, Vacancy

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Админка для компаний"""
    list_display = ['name', 'owner', 'created_at']
    list_display_links = ['name']
    search_fields = ['name', 'description']
    list_filter = ['created_at']
    prepopulated_fields = {'slug': ('name',)}  # авто-заполнение слага
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'logo', 'owner')
        }),
        ('URL', {
            'fields': ('slug',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # сворачиваемый блок
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка для категорий"""
    list_display = ['name', 'vacancies_count']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

    def vacancies_count(self, obj):
        """Количество вакансий в категории"""
        return obj.vacancies.count()

    vacancies_count.short_description = 'Вакансий'
    vacancies_count.admin_order_field = 'vacancies__count'


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    """Админка для вакансий"""

    # ✅ Поля только для чтения
    readonly_fields = ['created_at', 'updated_at', 'get_absolute_url_link']

    # Что показывать в списке
    list_display = [
        'title',
        'company_name',
        'category',
        'work_type_badge',
        'experience_badge',
        'salary_display',
        'city',
        'is_active',
        'created_at'
    ]

    # По каким полям кликабельно
    list_display_links = ['title']

    # Поиск
    search_fields = ['title', 'description', 'city']

    # Фильтры справа
    list_filter = [
        'is_active',
        'work_type',
        'experience',
        'category',
        'city',
        'created_at'
    ]

    # Редактирование прямо в списке
    list_editable = ['is_active']

    # Предзаполнение слага
    prepopulated_fields = {'slug': ('title',)}

    # Группировка полей
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'description', 'salary', 'city')
        }),
        ('Тип вакансии', {
            'fields': ('work_type', 'experience')
        }),
        ('Связи', {
            'fields': ('category', 'company')
        }),
        ('Статус', {
            'fields': ('is_active', 'is_featured', 'slug')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Ссылка', {
            'fields': ('get_absolute_url_link',),
            'classes': ('collapse',)
        }),
    )

    # Пагинация
    list_per_page = 25

    # Сортировка по умолчанию
    ordering = ['-created_at']

    # Кастомные методы для отображения
    def company_name(self, obj):
        return obj.company.name if obj.company else '—'

    company_name.short_description = 'Компания'
    company_name.admin_order_field = 'company__name'

    def salary_display(self, obj):
        return f"{obj.salary:,} ₽".replace(',', ' ') if obj.salary else '—'

    salary_display.short_description = 'Зарплата'

    def work_type_badge(self, obj):
        colors = {'remote': 'green', 'office': 'blue', 'hybrid': 'purple'}
        text = dict(Vacancy.WorkType.choices).get(obj.work_type, '')
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 10px;">{}</span>',
            colors.get(obj.work_type, 'gray'), text
        )

    work_type_badge.short_description = 'Формат'

    def experience_badge(self, obj):
        colors = {'no': 'green', 'junior': 'lightgreen', 'middle': 'orange', 'senior': 'red'}
        text = dict(Vacancy.Experience.choices).get(obj.experience, '')
        return format_html(
            '<span style="background: {}; color: {}; padding: 3px 10px; border-radius: 10px;">{}</span>',
            colors.get(obj.experience, 'gray'),
            'black' if obj.experience in ['junior', 'no'] else 'white', text
        )

    experience_badge.short_description = 'Опыт'

    def get_absolute_url_link(self, obj):
        if obj.pk and obj.slug:
            url = obj.get_absolute_url()
            return format_html('<a href="{}" target="_blank">🔗 Открыть на сайте</a>', url)
        return '—'

    get_absolute_url_link.short_description = 'Ссылка'

    # Действия над выбранными объектами
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"✅ {queryset.count()} вакансий активировано")

    make_active.short_description = "Активировать выбранные вакансии"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"❌ {queryset.count()} вакансий деактивировано")

    make_inactive.short_description = "Деактивировать выбранные вакансии"
