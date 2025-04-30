from django import forms
from .models import Result,Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'student_id']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter student name'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter student ID'}),
        }




class AdminLoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter password'
    }))


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'grade', 'rating', 'message', 'month']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'grade': forms.NumberInput(attrs={'class': 'form-control'}),
            'rating': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 2}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional message...'}),
            'month': forms.Select(attrs={'class': 'form-control'}),
        }
