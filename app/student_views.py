import datetime

from django.contrib import messages
from django.shortcuts import render, redirect

from app.forms import review_form, ComplaintForm, BookRoomForm
from app.models import Hostel, Food, Notifications, Reviews, Student, Complaints, BookRoom, Attendance, \
    LeaveApplication, Payment


def card(request):
    return render(request, 'student/card.html')


def view_student_hostel_details(request):
    data = Hostel.objects.all()
    return render(request, 'student/view_hostel_details.html', {'data': data})


def view_student_food_details(request):
    data = Food.objects.all()
    return render(request, 'student/view_food_details.html', {'data': data})


def view_student_notifications(request):
    data = Notifications.objects.all()
    return render(request, 'student/view_notifications.html', {'data': data})


def add_student_reviews(request):
    s = Student.objects.get(user=request.user)
    r_form = review_form()
    if request.method == 'POST':
        r_form = review_form(request.POST)
        f = r_form.save(commit=False)
        f.student = s  # student is relative name
        f.save()
        messages.info(request, 'Your Review Send Successfully')
        return redirect('view_student_reviews')
    return render(request, 'student/add_reviews.html', {'r_form': r_form})


def view_student_reviews(request):
    student = Student.objects.get(user=request.user)
    data = Reviews.objects.filter(student=student)
    return render(request, 'student/view_reviews.html', {'data': data})


def update_student_reviews(request, id):
    data = Reviews.objects.get(id=id)
    r_form = review_form(instance=data)
    if request.method == 'POST':
        r_form = review_form(request.POST, instance=data)
        if r_form.is_valid():
            r_form.save()
            return redirect('view_student_reviews')
    return render(request, 'student/update_reviews.html', {'r_form': r_form})


def delete_student_reviews(request, id):
    Reviews.objects.get(id=id).delete()
    return redirect('view_student_reviews')


def add_student_complaints(request):
    c_form = ComplaintForm()
    u = request.user
    if request.method == 'POST':
        c_form = ComplaintForm(request.POST)
        if c_form.is_valid():
            obj = c_form.save(commit=False)
            obj.user = u
            obj.save()
            messages.info(request, 'Complaint added successfully')
            return redirect('view_student_complaints')
    return render(request, 'student/add_complaints.html', {'c_form': c_form})


def view_student_complaints(request):
    data = Complaints.objects.filter(user=request.user)
    return render(request, "student/view_complaints.html", {'data': data})


def student_book_room(request):
    form = BookRoomForm()
    if request.method == 'POST':
        form = BookRoomForm(request.POST)
        if form.is_valid():
            book = form.save(
                commit=False)  # form only has the datefield so we have to call objects right to set the student and all
            book.student = Student.objects.get(
                user=request.user)  # user has all student details still we try to get it from student objects
            # book.student = request.user  # we are getting the name instead of username because of foreign key
            book.booking_date = form.cleaned_data.get('booking_date')
            book.booked_by = request.user
            student_qs = BookRoom.objects.filter(student=Student.objects.get(user=request.user))
            if student_qs.exists():
                messages.info(request, ' You Have Already Booked Room')
            else:
                book.save()
                messages.info(request, 'Successfully Booked Room')
                return redirect('card')
    return render(request, 'student/book_room.html', {'form': form})


def student_booking_status(request):
    student = Student.objects.get(user=request.user)  # that particular student who booked the room. its foreign key
    data = BookRoom.objects.filter(
        student=student)  # student is field in model bookroom .we can  give booked_by=request.user instead
    return render(request, 'student/booking_status.html', {'data': data})


def student_view_attendance(request):
    student = Student.objects.get(user=request.user)
    data = Attendance.objects.filter(student=student)
    return render(request, 'student/view_attendance.html', {'data': data})


now = datetime.datetime.now()


def student_leave_application(request):
    # student = Student.objects.filter(user=request.user)
    # data = LeaveApplication.objects.filter(user=student, current_date=datetime.date.today())
    if request.method == 'POST':
        leave_from = request.POST.get('leave_from')
        leave_to = request.POST.get('leave_to')
        reason = request.POST.get('reason')
        LeaveApplication(user=request.user, current_date=datetime.date.today(), leave_from=leave_from,
                         leave_to=leave_to,
                         reason=reason, current_time=now.time(), status=0).save()
        messages.info(request, 'Leave Application send Successfully')
        return redirect('card')
    return render(request, 'student/leave_application.html')


def student_view_leave_application(request):
    leave_application = LeaveApplication.objects.filter(user=request.user)
    return render(request, 'student/view_leave_application.html', {'leave_application': leave_application})


def student_view_fee(request):
    student = Student.objects.get(user=request.user)
    payments = Payment.objects.filter(student=student)
    return render(request, 'student/view_fees.html', {'payments': payments})


def student_view_bill(request, id):
    payment = Payment.objects.get(id=id)
    hostel = Hostel.objects.all().last()
    student = Student.objects.get(name=payment.student)
    context = {
        'payment': payment,
        'hostel': hostel,
        'student': student
    }
    return render(request, 'student/view_bill.html', context)
