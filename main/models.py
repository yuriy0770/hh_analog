from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from users.models import CustomUsers


class Company(models.Model):
    """Модель компании-работодателя"""
    name = models.CharField('Название компании', max_length=100)
    description = models.TextField('Описание компании')
    logo = models.ImageField('Логотип', upload_to='companies/logo/', blank=True, null=True)
    slug = models.SlugField('URL', max_length=100, unique=True)
    owner = models.OneToOneField(CustomUsers,on_delete=models.CASCADE,related_name='company',verbose_name='Владелец')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('company_detail', args=[self.slug])


class Category(models.Model):
    """Категория вакансий (IT, Маркетинг, Продажи...)"""
    name = models.CharField('Название категории', max_length=100)
    description = models.TextField('Описание', blank=True)
    slug = models.SlugField('URL', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', args=[self.slug])


class Vacancy(models.Model):
    """Модель вакансии"""

    class WorkType(models.TextChoices):
        REMOTE = 'remote', '🌍 Удаленная работа'
        OFFICE = 'office', '🏢 В офисе работодателя'
        HYBRID = 'hybrid', '🔄 Гибридный формат'

    class Experience(models.TextChoices):
        NO = 'no', '🙅 Без опыта'
        JUNIOR = 'junior', '🌱 Junior'
        MIDDLE = 'middle', '🌳 Middle'
        SENIOR = 'senior', '🌲 Senior'
    title = models.CharField('Название вакансии', max_length=200)
    description = models.TextField('Описание вакансии')
    salary = models.PositiveIntegerField('Зарплата', blank=True, null=True)
    city = models.CharField('Город', max_length=100)
    work_type = models.CharField(
        'Тип занятости',
        max_length=10,
        choices=WorkType.choices,
        default=WorkType.REMOTE
    )

    experience = models.CharField(
        'Опыт работы',
        max_length=10,
        choices=Experience.choices,
        default=Experience.JUNIOR
    )
    category = models.ForeignKey(Category,on_delete=models.CASCADE, related_name='vacancies',verbose_name='Категория')
    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name='vacancies',verbose_name='Компания',null=True,  blank=True  )
    is_active = models.BooleanField('Активно', default=True)
    is_featured = models.BooleanField('Рекомендуемое', default=False)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    slug = models.SlugField('URL', max_length=200, unique=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-created_at', '-is_featured']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_active', 'work_type']),
        ]

    def save(self, *args, **kwargs):
        # Генерируем slug, если его нет или он некорректный
        if not self.slug or self.slug.strip() == '' or self.slug == '-1' or not self.slug[0].isalnum():
            from django.utils.text import slugify
            base_slug = slugify(self.title)

            # Если slugify вернул пустую строку
            if not base_slug:
                base_slug = f"vacancy-{self.id or 'new'}"

            slug = base_slug
            counter = 1

            # Проверяем уникальность
            while Vacancy.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('main:vacancy_detail', args=[self.slug])

    def short_description(self):
        """Короткое описание для списка"""
        if len(self.description) > 100:
            return self.description[:100] + '...'
        return self.description

    short_description.short_description = 'Описание'
