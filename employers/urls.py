from django.urls import path
from . import views

app_name = 'employers'

urlpatterns = [
    path('dashboard/', views.employer_dashboard, name='dashboard'),
    path('company/create/', views.create_company, name='create_company'),
    path('company/edit/', views.edit_company, name='edit_company'),
    path('vacancy/create/', views.create_vacancy, name='create_vacancy'),
    path('vacancy/<int:vacancy_id>/edit/', views.edit_vacancy, name='edit_vacancy'),
    path('vacancy/<int:vacancy_id>/applications/', views.vacancy_applications, name='vacancy_applications'),
    path('application/<int:app_id>/respond/', views.respond_application, name='respond_application'),
]