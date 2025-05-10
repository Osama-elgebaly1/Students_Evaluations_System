from django.db import models

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=255)
    student_id = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.name
    

class Result(models.Model):
    MONTH_CHOICES = (
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    )
    
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    grade = models.IntegerField()
    rating = models.CharField(max_length=2)
    message = models.TextField(max_length=500,null=True,blank=True)
    month = models.DateField()  

    def __str__(self):
        return f"{self.student.name} - {self.rating}"
    
    