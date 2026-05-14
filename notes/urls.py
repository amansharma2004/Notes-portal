from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('subject/<slug:subject_slug>/', views.subject_detail, name='subject_detail'),
    path('api/subject/<slug:subject_slug>/units/', views.units_and_notes, name='units_and_notes'),
    path('note/<int:note_id>/view/', views.view_note_pdf, name='view_note_pdf'),
    path('courses/', views.courses_list, name='courses_list'),
    path('courses/<slug:slug>/', views.course_detail, name='course_detail'),
]