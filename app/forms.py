import datetime
import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from app.models import User, Student, Parent, Hostel, Food, Notifications, Warden, Reviews, Complaints, BookRoom, \
    Attendance, ParentReviews, InOut, Payment


class Date(forms.DateInput):
    input_type = 'date'


class Time(forms.TimeInput):
    input_type = 'time'


def phone_no_validation(value):
    if not re.compile(r'^[6-9]\d{9}$').match(value):
        raise ValidationError('Not valid number')


class UserRegister(UserCreationForm):
    username = forms.CharField()
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class Studentreg(forms.ModelForm):
    phone_no = forms.CharField(validators=[phone_no_validation])
    email = forms.CharField(validators=[
        RegexValidator(regex='^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$', message='Not valid Email')])

    class Meta:
        model = Student
        exclude = ('user', 'approval_status')

    def clean_email(self):
        mail = self.cleaned_data['email']
        email_qs_stu = Student.objects.filter(email=mail)
        email_qs_parent = Parent.objects.filter(email=mail)
        email_qs_warden = Warden.objects.filter(email=mail)
        if email_qs_stu.exists() or email_qs_parent.exists() or email_qs_warden.exists():
            raise forms.ValidationError('Email already linked with another account')
        return mail

    def clean_phone_no(self):
        phone_num = self.cleaned_data['phone_no']
        phone_qs_stu = Student.objects.filter(phone_no=phone_num)
        phone_qs_parent = Parent.objects.filter(phone_no=phone_num)
        phone_qs_warden = Warden.objects.filter(phone_no=phone_num)
        if phone_qs_stu.exists() or phone_qs_parent.exists() or phone_qs_warden.exists():
            raise ValidationError('Number already linked with another account')
        return phone_num


class Parentreg(forms.ModelForm):
    phone_no = forms.CharField(validators=[phone_no_validation])
    email = forms.CharField(validators=[
        RegexValidator(regex='^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$', message='Not valid Email')])

    class Meta:
        model = Parent
        exclude = ('user', "approval_status")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student_name'].empty_label = "select the student"

    def clean_email(self):
        mail = self.cleaned_data['email']
        email_qs_stu = Student.objects.filter(email=mail)
        email_qs_parent = Parent.objects.filter(email=mail)
        email_qs_warden = Warden.objects.filter(email=mail)
        if email_qs_stu.exists() or email_qs_parent.exists() or email_qs_warden.exists():
            raise forms.ValidationError('Email already linked with another account')
        return mail

    def clean_phone_no(self):
        phone_num = self.cleaned_data['phone_no']
        phone_qs_stu = Student.objects.filter(phone_no=phone_num)
        phone_qs_parent = Parent.objects.filter(phone_no=phone_num)
        phone_qs_warden = Warden.objects.filter(phone_no=phone_num)
        if phone_qs_stu.exists() or phone_qs_parent.exists() or phone_qs_warden.exists():
            raise ValidationError('Number already linked with another account')
        return phone_num


class Hosteldetails(forms.ModelForm):
    Contact_no = forms.CharField(validators=[phone_no_validation])
    Email = forms.CharField(validators=[
        RegexValidator(regex='^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$', message='Not valid Email')])

    class Meta:
        model = Hostel
        fields = '__all__'


class FoodDetails(forms.ModelForm):
    class Meta:
        model = Food
        fields = '__all__'


class notification_details(forms.ModelForm):
    Posted_To = forms.DateField(widget=Date)
    Time = forms.TimeField(widget=Time)

    class Meta:
        model = Notifications
        fields = '__all__'


class warden_details(forms.ModelForm):
    phone_no = forms.CharField(validators=[phone_no_validation])
    email = forms.CharField(validators=[
        RegexValidator(regex='^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$', message='Not valid Email')])

    class Meta:
        model = Warden
        exclude = ('user',)

    def clean_email(self):
        mail = self.cleaned_data['email']
        email_qs_stu = Student.objects.filter(email=mail)
        email_qs_parent = Parent.objects.filter(email=mail)
        email_qs_warden = Warden.objects.filter(email=mail).exclude(user_id=self.instance.user_id)
        if email_qs_stu.exists() or email_qs_parent.exists() or email_qs_warden.exists():
            raise forms.ValidationError('Email already linked with another account')
        return mail

    def clean_phone_no(self):
        phone_num = self.cleaned_data['phone_no']
        phone_qs_stu = Student.objects.filter(phone_no=phone_num)
        phone_qs_parent = Parent.objects.filter(phone_no=phone_num)
        phone_qs_warden = Warden.objects.filter(phone_no=phone_num).exclude(user_id=self.instance.user_id)
        if phone_qs_stu.exists() or phone_qs_parent.exists() or phone_qs_warden.exists():
            raise ValidationError('Number already linked with another account')
        return phone_num


class review_form(forms.ModelForm):
    class Meta:
        model = Reviews
        exclude = ('student',)


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaints
        fields = ('complaint',)


class BookRoomForm(forms.ModelForm):
    booking_date = forms.DateField(widget=Date)

    class Meta:
        model = BookRoom
        fields = ('booking_date',)


attendance_status = (
    ('present', 'present'), ('absent', 'absent')
)


class AttendanceForm(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=Student.objects.filter(approval_status=True))
    attendance = forms.ChoiceField(choices=attendance_status, widget=forms.RadioSelect())

    class Meta:
        model = Attendance
        fields = ('student', 'attendance')


class ParentReviewsForm(forms.ModelForm):
    class Meta:
        model = ParentReviews
        fields = ('comments',)


class InOutForm(forms.ModelForm):
    out_time = forms.TimeField(widget=Time)

    class Meta:
        model = InOut
        exclude = ('status',)
        widgets = {
            'in_time': forms.TimeInput(attrs={'type': 'time'})
        }
        in_time = forms.TimeField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # call the parent class(forms.ModelForm) constructor
        self.fields['student'].empty_label = 'select the student'

        booking_students = BookRoom.objects.filter(status=1).values_list('student', flat=True).distinct()
        self.fields['student'].queryset = Student.objects.filter(pk__in=booking_students)

    def clean(self):
        cleaned_data = super().clean()
        in_time = cleaned_data.get('in_time')  # Assuming 'in_time' is a field in your form

        if in_time:
            cleaned_data['status'] = 1

        return cleaned_data


class PaymentForm(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=Student.objects.none())
    bill_start_date = forms.DateField(widget=Date)
    bill_end_date = forms.DateField(widget=Date)
    mess_bill = forms.FloatField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    amount = forms.IntegerField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Payment
        exclude = ('status', 'hostel', 'bill_no', 'bill_due_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add a default choice to the student field
        self.fields['student'].empty_label = "select the student"
        booking_students = BookRoom.objects.filter(status=1).values_list('student', flat=True).distinct()
        self.fields['student'].queryset = Student.objects.filter(pk__in=booking_students)

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        bill_end_date = cleaned_data.get('bill_end_date')
        bill_start_date = cleaned_data.get('bill_start_date')
        if bill_end_date.month == datetime.date.today().month:
            raise forms.ValidationError('Fee cannot be calculated for the current month')
        elif not Payment.objects.filter(student=student).exists():
            booking = BookRoom.objects.get(student=student, status=1)
            if bill_start_date != booking.booking_date:
                raise forms.ValidationError('Student joined this month')

