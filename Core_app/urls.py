from django.urls import path
from .views import students_views, admin_views

urlpatterns = [
    # Student-facing route
    path('', students_views.check_results, name='check_results'),

    # Admin authentication
    path('login/', admin_views.log_in, name='admin-login'),
    path('logout/', admin_views.log_out, name='admin-logout'),

    # Main dashboard 
    path('main_dashboard/', admin_views.main_dash, name='main_dash'),
    path('results_dashboard/', admin_views.results_dash, name='results_dash'),
    path('students_dashboard/', admin_views.students_dash, name='students_dash'),
    path('admins_dash/', admin_views.admins_dash, name='admins_dash'),

    # Admin actions
    path('add_result/', admin_views.add_result, name='add_result'),
    path('add_student/', admin_views.add_student, name='add_student'),
    path('add_admin/', admin_views.add_admin, name='add_admin'),
    path('reset_password/', admin_views.reset_password, name='reset_password'),
    path('delete_admin/<int:pk>', admin_views.delete_admin, name='delete_admin'),
    
    #  Get Sudent Results 
    path('get_results/<int:pk>',admin_views.get_results,name='get_results'),
    path('edit_result/<int:result_id>/', admin_views.edit_result, name='edit_result'),
    path('delete_result/<int:result_id>/', admin_views.delete_result, name='delete_result'),

    # Actions on students 
    path('edit_student/<int:student_id>/', admin_views.edit_student, name='edit_student'),
    path('delete_student/<int:student_id>/', admin_views.delete_student, name='delete_student'),

    # Upload Excel 
    path('upload_excel/', admin_views.upload_excel, name='upload_excel'),
    



]
