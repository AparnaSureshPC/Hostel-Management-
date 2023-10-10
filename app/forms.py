import datetime
from datetime import date
from django import forms
from django.contrib.auth.forms import UserCreationForm

from app.models import User, Student, Parent, Hostel, Food, Notifications, Warden, Reviews, Complaints, BookRoom, \
    Attendance, ParentReviews, InOut, Payment


class Date(forms.DateInput):
    input_type = 'date'


class Time(forms.TimeInput):
    input_type = 'time'


class UserRegister(UserCreationForm):
    username = forms.CharField()
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class Studentreg(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ('user', 'approval_status')


class Parentreg(forms.ModelForm):
    class Meta:
        model = Parent
        exclude = ('user', "approval_status")


class Hosteldetails(forms.ModelForm):
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
    class Meta:
        model = Warden
        exclude = ('user',)


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

        def clean_date_joining(self):
            date = self.cleaned_data['booking_date']

            if date < datetime.date.today():
                raise forms.ValidationError('Invalid for')
            return date


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


class PaymentForm(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=Student.objects.filter(approval_status=1))
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

    def clean(self):
        cleaned_data = super().clean()
        bill_end_date = cleaned_data.get('bill_end_date')
        if bill_end_date.month == datetime.date.today().month:
            raise forms.ValidationError('Fee cannot be calculated for the current month')
