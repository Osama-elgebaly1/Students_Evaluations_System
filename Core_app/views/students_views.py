from django.shortcuts import render,get_object_or_404
from Core_app.models import Student,Result
from django.contrib.auth.decorators import user_passes_test
# Create your views here.



from django.shortcuts import render, get_object_or_404
from Core_app.models import Student, Result

def check_results(request):
    """
    Handle result checking for students based on student ID.

    - GET: Display the result input form.
    - POST: Look up student by ID, fetch results, and show the latest + previous ones.
    """
    if request.method == 'POST':
        student_id = request.POST.get('student_id')

        student = get_object_or_404(Student, student_id=student_id)
        results = Result.objects.filter(student=student).order_by('-id')
        last_result = results.first()
        previous_results = results[1:]

        return render(request, 'student_templates/results.html', {
            'student': student,
            'last_result': last_result,
            'previous_results': previous_results,
        })

    return render(request, 'student_templates/check_results.html')


