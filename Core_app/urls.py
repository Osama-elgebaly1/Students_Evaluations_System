from django.urls import path
from .views import students_views, admin_views

urlpatterns = [
    # Student-facing route
    path('', students_views.check_results, name='check_results'),

    # Admin authentication
    path('login/', admin_views.log_in, name='admin-login'),
    path('logout/', admin_views.log_out, name='admin-logout'),

    # Admin dashboard views
    path('main_dashboard/', admin_views.main_dash, name='main_dash'),
    path('results_dashboard/', admin_views.results_dash, name='results_dash'),
    path('students_dashboard/', admin_views.students_dash, name='students_dash'),

    # Admin actions
    path('add_result/', admin_views.add_result, name='add_result'),
    path('add_student/', admin_views.add_student, name='add_student'),
]
