from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('vacancies/', views.VacancyListView.as_view(), name='vacancy_list'),
    path('vacancy/<slug:vacancy_slug>/', views.VacancyDetailView.as_view(), name='vacancy_detail'),
]
