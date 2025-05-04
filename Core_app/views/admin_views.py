from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.admin.models import LogEntry

from Core_app.forms import EditStudentForm, EditResultForm,AdminRegistrationForm,AdminLoginForm, ResultForm, StudentForm
from Core_app.models import Student, Result
from django.contrib.auth.models import User

from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType

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
from django.shortcuts import render, redirect
from Core_app.forms import ExcelUploadForm
from Core_app.models import Student, Result


def upload_excel(request):
    """
    Handle the upload of an Excel file to add students and their results.

    - Accepts POST requests with an Excel file containing student and result data.
    - For each row in the Excel file:
        - Creates a Student if it doesn't already exist (based on student_id).
        - Adds a Result for the student if one doesn't already exist for the same month.

    Redirects to the student dashboard after successful upload.
    Shows an upload form on GET requests.

    Excel columns expected: ['Student ID', 'Student Name', 'Grade', 'Rating', 'Message', 'Month']
    """
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            form = ExcelUploadForm(request.POST, request.FILES)
            if form.is_valid():
                excel_file = request.FILES['file']
                df = pd.read_excel(excel_file)

                for _, row in df.iterrows():
                    # 1. Get or create the student
                    student, created = Student.objects.get_or_create(
                        student_id=row['Student ID'],
                        defaults={'name': row['Student Name']}
                    )

                    # 2. Check if the result for this student & month already exists
                    exists = Result.objects.filter(student=student, month=row['Month']).exists()
                    if not exists:
                        # 3. Create the result
                        Result.objects.create(
                            student=student,
                            grade=row['Grade'],
                            rating=row['Rating'],
                            message=row.get('Message', ''),  # optional field
                            month=row['Month']
                        )

                return redirect('students_dash')  # or wherever you want
        else:
            form = ExcelUploadForm()
        return render(request, 'admin/upload_excel.html', {'form': form})
    else:
        messages.error(request,'You have to login as administrator to access this page...')
        return redirect('check_results')



def get_results(request, pk):
    """
    Display all results for a given student (by primary key).

    - Only accessible to authenticated staff users.
    - Retrieves the most recent result and all previous ones.
    - Passes the student, latest result, and previous results to the template.

    Redirects to 'check_results' if the user is not authorized.
    """
    if request.user.is_authenticated and  request.user.is_staff:
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
            messages.warning(request, "..............This student has no results yet.")
            return redirect('students_dash')  # or show an empty result page
    else:
        messages.error(request,'You have to login as administrator to access this page...')
        return redirect('check_results')



def admins_dash(request):
    """
    Display all Admins .
    """

    if request.user.is_authenticated and  request.user.is_superuser:
        admins = User.objects.filter(is_staff=True)
        return render(request,'admin/admin_dash.html',{'admins':admins})

    else:
        messages.error(request,'You have to login as administrator to access this page...')
        return redirect('check_results')


def add_admin(request):
    """
    Handle the creation of a new Admin via a form.

    - GET: Display the empty form.
    - POST: Validate and save the Admin, then redirect to dashboard.
    """
    if request.user.is_authenticated and  request.user.is_staff:

        if request.method == 'POST':
            form = AdminRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.is_staff = True  # Gives access to admin dashboard if needed
                admin = user.save()
                log_action(
                user=request.user,
                obj=admin,
                action_flag=ADDITION,
                message="Admin created via custom view"
                )
                return redirect('main_dash')

        else:
            form = AdminRegistrationForm()
            return render(request,'admin/add_admin.html',{'form':form})
  
    else:
        messages.error(request,'You have to be a Super User to access this page...')
        return redirect('check_results')


def delete_student(request,student_id):
    """
    Handle the deleting of a student .

    Delete the student, then redirect to students dashboard.
    """
    if request.user.is_authenticated and request.user.is_staff:
        student = Student.objects.get(id=student_id)
        student.delete()
        log_action(
                user=request.user,
                obj=student,
                action_flag=DELETION,
                message="Result deleted via custom view" 
                )
        return redirect('students_dash')

    else:
        messages.warning(request, 'You have to login as administrator to access this page...')
        return redirect('check_results')


def edit_student(request, student_id):
    """
    Handle the editing of a new student via a form.

    - GET: Display the instaced form.
    - POST: Validate and save the student, then redirect to students dashboard.
    """
    if request.user.is_authenticated and request.user.is_staff:
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
    else:
        messages.warning(request, 'You have to login as administrator to access this page...')
        return redirect('check_results')
    

def add_student(request):
    """
    Handle the creation of a new student via a form.

    - GET: Display the empty form.
    - POST: Validate and save the student, then redirect to dashboard.
    """
    if request.user.is_authenticated and request.user.is_staff:
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
    else:
        messages.warning(request, 'You have to login as administrator to access this page...')
        return redirect('check_results')



def delete_result(request,result_id):
    """
    Handle the deleting of a  result for a student.

    - Delete result and redirect to results dashboard on success.
    """
    if request.user.is_authenticated and request.user.is_staff:
        result = Result.objects.get(id=result_id)
        result.delete()
        log_action(
                user=request.user,
                obj=result,
                action_flag=DELETION,
                message="Result deleted via custom view"
                )
        return redirect('results_dash')


    else:
        messages.warning(request, 'You have to login as administrator to access this page...')
        return redirect('check_results')


def edit_result(request, result_id):
    """
    Handle the Editing of a result for a student.

    - GET: Display the instaced  result form.
    - POST: Save result and redirect to results dashboard on success  .
    """
    if request.user.is_authenticated and request.user.is_staff:
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
    else:
        messages.warning(request, 'You have to login as administrator to access this page...')
        return redirect('check_results')


def add_result(request):
    """
    Handle the creation of a new result for a student.

    - GET: Display the empty result form.
    - POST: Save result and redirect to results dashboard on success.
    """
    if request.user.is_authenticated and request.user.is_staff:
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
    else:
        messages.warning(request, 'You have to login as administrator to access this page...')
        return redirect('check_results')
    


def students_dash(request):
    """
    Display all students in descending order by ID.
    """
    if request.user.is_authenticated and request.user.is_staff:
        students = Student.objects.all().order_by('-id')
        return render(request, 'admin/students_dash.html', {'students': students})
    else:
        messages.warning(request, 'You have to login as administrator to access this page...')
        return redirect('check_results')


def results_dash(request):
    """
    Display all results in descending order by ID.
    """
    if request.user.is_authenticated and request.user.is_staff:
        results = Result.objects.all().order_by('-id')
        return render(request, 'admin/results_dash.html', {'results': results})
    else:
        messages.warning(request, 'You have to login as administrator to access this page...')
        return redirect('check_results')


def log_out(request):
    """
    Log out the current user and redirect to result check page.
    """
    if request.user.is_authenticated and request.user.is_staff:
        logout(request)
        return redirect('check_results')
    else:
        messages.warning(request, 'You have to login as administrator to access this page...')
        return redirect('check_results')


def main_dash(request):
    """
    Display the admin dashboard with recent activity logs.

    Only accessible by logged-in staff members.
    """
    if request.user.is_staff and request.user.is_authenticated:
        activity = LogEntry.objects.all().order_by('-action_time')[:10]
        return render(request, 'admin/dash.html', {'activities': activity})
    else:
        messages.warning(request, 'You have to login as administrator to access this page...')
        return redirect('check_results')


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
