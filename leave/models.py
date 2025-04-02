from django.db import models

class HostelUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)  # In production, use hashed passwords
    email = models.EmailField()
    contact = models.CharField(max_length=15)
    address = models.TextField()
    role = models.CharField(max_length=10, choices=[('student', 'Student'), ('rector', 'Rector')])
    last_login = models.DateTimeField(auto_now=True)  # Manually add the last_login field
    date_joined = models.DateTimeField(auto_now_add=True)  # Manually add the date_joined field

    def __str__(self):
        return self.username
    

class LeaveApplication(models.Model):
    student = models.ForeignKey(HostelUser, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=255, default="No reason provided")
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')

    def __str__(self):
        return f"{self.student.username} - {self.status}"
