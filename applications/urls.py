from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('apply/<int:vacancy_id>/', views.apply_to_vacancy, name='apply'),
]