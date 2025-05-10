from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.admin.models import LogEntry

from Core_app.forms import PasswordResetForm, EditStudentForm, EditResultForm,AdminRegistrationForm,AdminLoginForm, ResultForm, StudentForm
from Core_app.models import Student, Result
from django.contrib.auth.models import User

from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from functools import wraps

def superuser_required(view_func):
    """
    A decorator that checks if the user is authenticated , if not ( login page ),
    And check if the user is superuser , if not (main_dashboard page)

    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # If not authenticated, redirect to login page or some other page
            return redirect('admin-login')  # Change 'login_url' to the actual login page name

        if not request.user.is_superuser:
            # Add error message when user is not staff
            messages.error(request, "You do not have permission to access this page.")
            return redirect('main_dash')  # Change 'check_results' to the actual page name

        return view_func(request, *args, **kwargs)
    
    return _wrapped_view


def staff_required(view_func):
    """
    A decorator that checks if the user is authenticated , if not ( login page ),
    And check if the user is Staff , if not (Check_results page )

    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # If not authenticated, redirect to login page or some other page
            return redirect('admin-login')  # Change 'login_url' to the actual login page name

        if not request.user.is_staff:
            # Add error message when user is not staff
            messages.error(request, "You do not have permission to access this page.")
            return redirect('check_results')  # Change 'check_results' to the actual page name

        return view_func(request, *args, **kwargs)
    
    return _wrapped_view


def log_action(user, obj, action_flag, message):

    LogEntry.objects.log_action(
        user_id=user.pk,
        content_type_id=ContentType.objects.get_for_model(obj.__class__).pk,
        object_id=obj.pk,
        object_repr=str(obj),
        action_flag=action_flag,
        change_message=message,
    )



# Excel upload imports 
import pandas as pd
from Core_app.forms import ExcelUploadForm
from datetime import datetime


@staff_required
def upload_excel(request):
    """
    Handles the upload of an Excel file to update student results.

    This view is accessible only to Staff users. It processes the uploaded file, 
    extracts student data (Student ID, Name, Sector, Month, Grade, Rating, and Message), and updates the database.
    If the student or result doesn't exist, it creates new records.

    Redirects to the student dashboard after successful upload.
    Shows an upload form on GET requests.

    Excel columns expected: ['Student ID', 'Student Name' , 'Sector', 'Grade', 'Rating', 'Message', 'Month']

    """
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            form = ExcelUploadForm(request.POST, request.FILES)
            if form.is_valid():
                excel_file = request.FILES['file']
                df = pd.read_excel(excel_file)

                for _, row in df.iterrows():
                    # Get or create student
                    student, _ = Student.objects.get_or_create(
                        student_id=row['Student ID'],
                        defaults={'name': row['Student Name'],
                                  'sector':row['Sector']}
                    )

                    # Convert month (e.g., "2024-04" or "April") to date object
                    try:
                        if isinstance(row['Month'], str):
                            # if format is "April" or "Apr"
                            month_date = datetime.strptime(row['Month'], '%B')  # "April"
                            # assign a dummy year (like current year)
                            month_date = month_date.replace(year=datetime.now().year, day=1)
                        else:
                            # if it's already a timestamp or datetime
                            month_date = pd.to_datetime(row['Month']).to_pydatetime().replace(day=1)
                    except Exception as e:
                        print(f"Invalid month format: {row['Month']}")
                        continue  # skip this row

                    # Check if result exists
                    if not Result.objects.filter(student=student, month=month_date).exists():
                        Result.objects.create(
                            student=student,
                            grade=row['Grade'],
                            rating=row['Rating'],
                            message=row.get('Message', ''),
                            month=month_date
                        )

                return redirect('students_dash')
        else:
            form = ExcelUploadForm()

        return render(request, 'admin/upload_excel.html', {'form': form})
    else:
        messages.error(request,'You have to login as administrator to access this page...')
        return redirect('check_results')


@staff_required
def get_results(request, pk):
    """
    Display all results for a given student (by primary key).

    - Only accessible to authenticated staff users.
    - Retrieves the most recent result and all previous ones.
    - Passes the student, latest result, and previous results to the template.

    Redirects to 'check_results' if the user is not authorized.
    """
    results = Result.objects.filter(student=pk).order_by('-id')
    if results.exists():
        last_result = results.first()
        previous_results = results[1:]
        return render(request, 'admin/get_results.html', {
                'student': last_result.student,
                'last_result': last_result,
                'previous_results': previous_results
        })
    else:
        messages.warning(request, "This student has no results yet.")
        return redirect('students_dash')  # or show an empty result page


@superuser_required
def admins_dash(request):
    """
    Display all Admins .
    """
    admins = User.objects.filter(is_staff=True)
    return render(request,'admin/admin_dash.html',{'admins':admins})



@superuser_required
def delete_admin(request,pk):
        admin = User.objects.get(id=pk,is_staff=True)
        admin.delete()
        log_action(
                user=request.user,
                obj=admin,
                action_flag=DELETION,
                message="Admin deleted via custom view" 
                )
        return redirect('admins_dash')




@staff_required
def reset_password(request):
        if request.method == 'POST':
            user = User.objects.get(username  = request.user.username)
            new_password = request.POST['password']
            confirmed_password = request.POST['confirm_password']

            if new_password and confirmed_password and new_password == confirmed_password:
                user.set_password(new_password)
                user.save()
                messages.success(request,'Password has been reset successfully ...')
                return redirect('admin-login')
            else:
                messages.error(request,'Passwords must be the same ...')
                return redirect('reset_password')
        else:
            return render(request,'admin/reset_password.html')

    

@superuser_required
def add_admin(request):
    """
    Handle the creation of a new Admin via a form.

    - GET: Show form.
    - POST: Validate and create admin.
    """
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            try:
                    # Save user without committing
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])  # hash the password
                user.is_staff = True  # Grant admin rights
                user.save()  # Commit the user object to save

                    # Log the action
                log_action(
                        user=request.user,
                        obj=user,
                        action_flag=ADDITION,
                        message="Admin created via custom view"
                    )

                messages.success(request, 'Admin created successfully.')
                return redirect('main_dash')  # Redirect to dashboard

            except IntegrityError:
                form.add_error('username', 'This username is already taken.')


    else:
        form = AdminRegistrationForm()

    return render(request, 'admin/add_admin.html', {'form': form})


@staff_required
def delete_student(request,student_id):
    """
    Handle the deleting of a student .

    Delete the student, then redirect to students dashboard.
    """
    student = Student.objects.get(id=student_id)
    student.delete()
    log_action(
                user=request.user,
                obj=student,
                action_flag=DELETION,
                message="Result deleted via custom view" 
            )
    return redirect("students_dash")



@staff_required
def edit_student(request, student_id):
    """
    Handle the editing of a new student via a form.

    - GET: Display the instaced form.
    - POST: Validate and save the student, then redirect to students dashboard.
    """
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        form = EditStudentForm(request.POST, instance=student)
        user = request.user
        if form.is_valid():
            student =form.save()
            log_action(
                user=request.user,
                obj=student,
                action_flag=CHANGE,
                message="Result edited via custom view" + f" by {user}"
                )
            return redirect('students_dash')  # or wherever you want to go after update
    else:
        form = EditStudentForm(instance=student)

    return render(request, 'admin/edit_student.html', {'form': form})

 
@staff_required
def add_student(request):
    """
    Handle the creation of a new student via a form.

    - GET: Display the empty form.
    - POST: Validate and save the student, then redirect to dashboard.
    """
    form = StudentForm() 
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            log_action(
                user=request.user,
                obj=student,
                action_flag=ADDITION,
                message="Student created via custom view"
            )
            return redirect('students_dash')
    return render(request, 'admin/add_student.html', {'form': form})



@staff_required
def delete_result(request,result_id):
    """
    Handle the deleting of a  result for a student.

    - Delete result and redirect to results dashboard on success.
    """
    result = Result.objects.get(id=result_id)
    result.delete()
    log_action(
                user=request.user,
                obj=result,
                action_flag=DELETION,
                message="Result deleted via custom view"
            )
    return redirect('results_dash')


@staff_required
def edit_result(request, result_id):
    """
    Handle the Editing of a result for a student.

    - GET: Display the instaced  result form.
    - POST: Save result and redirect to results dashboard on success  .
    """
    result = get_object_or_404(Result, id=result_id)

    if request.method == 'POST':
        form = EditResultForm(request.POST, instance=result)
        user = request.user
        if form.is_valid():
            result = form.save()
            log_action(
                user=request.user,
                obj=result,
                action_flag=CHANGE,
                message="Result edited via custom view"+ f" by {user}"
                )
            return redirect('results_dash')  # or wherever you want to go after update
    else:
        form = EditResultForm(instance=result)

    return render(request, 'admin/edit_result.html', {'form': form})


@staff_required
def add_result(request):
    """
    Handle the creation of a new result for a student.

    - GET: Display the empty result form.
    - POST: Save result and redirect to results dashboard on success.
    """
    form = ResultForm() 
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            result = form.save()
            log_action(
                user=request.user,
                obj=result,
                action_flag=ADDITION,
                message="Result created via custom view"
            )
            return redirect('results_dash')
            
    return render(request, 'admin/add_result.html', {'form': form})

    

@staff_required
def students_dash(request):
    """
    Display all students in descending order by ID.
    """
    students = Student.objects.all().order_by('-id')
    return render(request, 'admin/students_dash.html', {'students': students})


@staff_required
def results_dash(request):
    """
    Display all results in descending order by ID.
    """
    results = Result.objects.all().order_by('-month')
    return render(request, 'admin/results_dash.html', {'results': results})


@staff_required
def log_out(request):
    """
    Log out the current user and redirect to result check page.
    """
    logout(request)
    return redirect('check_results')


@staff_required
def main_dash(request):
    """
    Display the admin dashboard with recent activity logs.
    Only accessible by logged-in staff members.
    """
    activity = LogEntry.objects.all().order_by('-action_time')[:10]
    return render(request, 'admin/dash.html', {'activities': activity})



def log_in(request):
    """
    Handle admin login using username and password.

    - GET: Show the login form.
    - POST: Authenticate and login admin, redirect to dashboard on success.
    """
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('main_dash')
    
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_staff:
                login(request, user)
                return redirect('main_dash')
            else:
                form.add_error(None, 'Invalid credentials or not an admin.')
    else:  
        form = AdminLoginForm()

    return render(request, 'admin/login.html', {'form': form})
