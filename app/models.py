from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    is_warden = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student')
    name = models.CharField(max_length=50)
    course = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    email = models.EmailField()
    phone_no = models.CharField(max_length=10)
    photo = models.ImageField(upload_to='profile', null=True)
    approval_status = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='parent')
    name = models.CharField(max_length=50)
    student_name = models.ForeignKey(Student, on_delete=models.CASCADE)
    email = models.EmailField()
    address = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=10)
    photo = models.ImageField(upload_to='profile')
    approval_status = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Hostel(models.Model):
    Hostel_name = models.CharField(max_length=50)
    Total_rooms = models.CharField(max_length=100)
    Vacant_rooms = models.CharField(max_length=100)
    Room_facilities = models.CharField(max_length=200)
    Rent = models.CharField(max_length=50)
    Address = models.CharField(max_length=100)
    Email = models.EmailField()
    Contact_no = models.CharField(max_length=10)
    Photo = models.ImageField(upload_to='hostel_images')

    def __str__(self):
        return self.Hostel_name


DAYS = (('', 'Select the day'),
    ('Sunday', 'Sunday'),
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'), ('Friday', 'Friday'),
    ('Saturday', 'Saturday')

)


class Food(models.Model):
    Day = models.CharField(max_length=50, choices=DAYS)
    Breakfast = models.CharField(max_length=100)
    Lunch = models.CharField(max_length=100)
    Dinner = models.CharField(max_length=100)

    def __str__(self):
        return self.Day


class Notifications(models.Model):
    Posted_On = models.DateField(auto_now=True)
    Time = models.TimeField()
    Posted_To = models.CharField(max_length=50)
    Notifications = models.TextField(max_length=300)


class Warden(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='warden')
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    email = models.EmailField()
    phone_no = models.CharField(max_length=10)
    photo = models.ImageField(upload_to='warden')
    Date_of_joining = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Reviews(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    comments = models.TextField(max_length=300)

    def __str__(self):
        return self.date


class Complaints(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    complaint = models.CharField(max_length=200)
    reply = models.CharField(max_length=200, null=True, blank=True)


class BookRoom(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    booking_date = models.DateField()
    date = models.DateField(auto_now=True)
    status = models.IntegerField(default=0)
    booked_by = models.ForeignKey(User, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.student


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance")
    date = models.DateField(auto_now=True)
    attendance = models.CharField(max_length=10)
    time = models.TimeField()


class ParentReviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    comments = models.TextField(max_length=300)


class LeaveApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_date = models.DateField(auto_now=True)
    current_time = models.TimeField(auto_now=True)
    leave_from = models.DateField()
    leave_to = models.DateField()
    reason = models.CharField(max_length=100)
    status = models.IntegerField(default=0)

    @property
    def total_leave_days(self):
        if self.leave_from and self.leave_to:
            total_days = self.leave_to - self.leave_from
            return total_days.days + 1
        else:

            return None


class InOut(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='in_out')
    date = models.DateField(auto_now=True)
    out_time = models.TimeField()
    in_time = models.TimeField(blank=True, null=True)
    reason = models.TextField(max_length=300)
    status = models.IntegerField(default=0)


def calculate_bill_due_date():
    # Calculate the default due date, e.g., 10 days from today
    due_date = datetime.now() + timedelta(days=5)
    return due_date.strftime('%Y-%m-%d')


class Payment(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    bill_no = models.IntegerField()
    bill_date = models.DateField(auto_now=True)
    bill_start_date = models.DateField()
    bill_end_date = models.DateField()
    bill_due_date = models.DateField(default=calculate_bill_due_date)
    mess_bill = models.FloatField()
    amount = models.IntegerField()
    status = models.IntegerField(default=0)

    # def get_total_amount(self):
    #     return 3000 + self.mess_bill
