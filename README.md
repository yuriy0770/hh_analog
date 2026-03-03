# 💼 JobBoard — Платформа для поиска работы и сотрудников

![Django](https://img.shields.io/badge/Django-5.0-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 О проекте

**JobBoard** — это полноценная платформа для поиска работы и сотрудников, разработанная на Django. Проект разделяет пользователей на **соискателей** и **работодателей**, предоставляя каждому свой функционал.

### ✨ Ключевые возможности

#### Для соискателей:
- 🔍 Просмотр актуальных вакансий с фильтрацией по категориям, городам и типу занятости
- 📝 Отклики на вакансии с сопроводительными письмами
- ⭐ Избранное (в разработке)
- 👤 Личный профиль с информацией о пользователе

#### Для работодателей:
- 🏢 Создание и управление компанией
- 📝 Публикация и редактирование вакансий
- 👀 Просмотр откликов на вакансии
- 📊 Личный кабинет с аналитикой

#### Общий функционал:
- 🔐 Аутентификация и регистрация с разделением по ролям
- 👥 Профили пользователей (автоматическое создание через сигналы)
- 🎨 Адаптивный дизайн на Bootstrap 5
- 🌙 Темная тема

---

## 🛠 Технологический стек

| Компонент | Технология |
|-----------|------------|
| **Backend** | Django 5.0, Python 3.11 |
| **Database** | PostgreSQL |
| **Frontend** | HTML5, CSS3, Bootstrap 5 |
| **Аутентификация** | Django Auth + Custom User |
| **Файлы** | Media handling (ImageField) |
| **URLs** | ЧПУ (slugify) |
| **Сигналы** | Автосоздание профилей |
| **ORM** | Django ORM с оптимизацией запросов |

---


---

## 🗄 Модели данных

### **CustomUser** (users/models.py)
- Наследуется от `AbstractUser`
- Поля: `phone`, `user_type` (employer/seeker)
- Автоматическое создание профиля через сигналы

### **Profile** (users/models.py)
- One-to-One с CustomUser
- Поля: `avatar`, `birth_date`, `city`, `address`

### **Company** (main/models.py)
- Владелец (One-to-One с CustomUser)
- Поля: `name`, `description`, `logo`, `slug`

### **Category** (main/models.py)
- Поля: `name`, `description`, `slug`

### **Vacancy** (main/models.py)
- Связи: `company`, `category`
- Поля: `title`, `description`, `salary`, `city`
- Choices: `work_type` (remote/office/hybrid), `experience`
- Индексы для оптимизации запросов

### **Application** (applications/models.py)
- Связи: `vacancy`, `applicant`
- Поля: `cover_letter`, `status` (pending/accepted/rejected)

---

## ⚡ Сигналы

При регистрации нового пользователя автоматически создается профиль:

```python
@receiver(post_save, sender=CustomUsers)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

### 🎯 Планы по развитию
- Celery + Redis — фоновая отправка уведомлений
- Email-уведомления — при откликах и изменении статуса
- Избранное — сохранение вакансий
- Расширенный поиск — фильтры по зарплате, опыту
- Чат — между соискателями и работодателями
- Тесты — покрытие кода тестами
- Docker — контейнеризация проекта
- CI/CD — автоматический деплой


