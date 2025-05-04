from django import forms
from .models import Result,Student
from django.contrib.auth.models import User


class ExcelUploadForm(forms.Form):
    file = forms.FileField()


class EditStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'student_id']  # Adjust based on your model
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
class EditResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'grade','rating','message','month' ]  # Adjust based on your model
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'grade': forms.NumberInput(attrs={'class': 'form-control'}),
            'rating': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.TextInput(attrs={'class': 'form-control'}),
            'month': forms.Select(attrs={'class': 'form-control'}),
        }

class AdminRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")


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
