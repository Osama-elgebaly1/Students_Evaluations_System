from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.admin.models import LogEntry

from Core_app.forms import AdminLoginForm, ResultForm, StudentForm
from Core_app.models import Student, Result

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
            form.save()
            return redirect('students_dash')
    return render(request, 'admin/add_student.html', {'form': form})


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
            form.save()
            return redirect('results_dash')
    return render(request, 'admin/add_result.html', {'form': form})


def students_dash(request):
    """
    Display all students in descending order by ID.
    """
    students = Student.objects.all().order_by('-id')
    return render(request, 'admin/students_dash.html', {'students': students})


def results_dash(request):
    """
    Display all results in descending order by ID.
    """
    results = Result.objects.all().order_by('-id')
    return render(request, 'admin/results_dash.html', {'results': results})


def log_out(request):
    """
    Log out the current user and redirect to result check page.
    """
    logout(request)
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
        messages.warning(request, 'You have to login first...')
        return redirect('login')


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
