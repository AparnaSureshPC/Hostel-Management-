import calendar
import datetime
from datetime import date, timedelta
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from app.forms import Hosteldetails, FoodDetails, notification_details, UserRegister, warden_details, AttendanceForm, \
    PaymentForm
from app.models import Hostel, Food, Notifications, Warden, User, Student, Parent, Reviews, Complaints, BookRoom, \
    Attendance, ParentReviews, Payment


def admin_card(request):
    return render(request, 'admin/card.html')


def add_hosteldetails(request):
    h_form = Hosteldetails()
    if request.method == 'POST':
        h_form = Hosteldetails(request.POST, request.FILES)
        if h_form.is_valid():
            h_form.save()
            return redirect('admin_card')
    return render(request, 'admin/hosteldetails.html', {'h_form': h_form})


def view_hosteldetails(request):
    data = Hostel.objects.all()
    return render(request, 'admin/view_hosteldetails.html', {'data': data})


def update_hosteldetails(request, id):
    data = Hostel.objects.get(id=id)
    h_form = Hosteldetails(instance=data)
    if request.method == 'POST':
        h_form = Hosteldetails(request.POST, instance=data)
        if h_form.is_valid():
            h_form.save()
            messages.info(request, 'Updated Successfully')
            return redirect('view_hosteldetails')
    return render(request, 'admin/update_hosteldetails.html', {'h_form': h_form})


def delete_hosteldetails(request, id):
    Hostel.objects.get(id=id).delete()
    messages.info(request, 'Deleted Successfully')
    return redirect('view_hosteldetails')


def add_fooddetails(request):
    f_form = FoodDetails()
    if request.method == 'POST':
        f_form = FoodDetails(request.POST)
        if f_form.is_valid():
            f_form.save()
            return redirect('admin_card')
    return render(request, 'admin/add_fooddetails.html', {'f_form': f_form})


def view_fooddetails(request):
    data = Food.objects.all()
    return render(request, 'admin/view_fooddetails.html', {'data': data})


def update_fooddetails(request, id):
    data = Food.objects.get(id=id)
    f_form = FoodDetails(instance=data)
    if request.method == 'POST':
        f_form = FoodDetails(request.POST, instance=data)
        if f_form.is_valid():
            f_form.save()
            messages.info(request, 'Updated Successfully')
            return redirect('view_fooddetails')
    return render(request, 'admin/update_fooddetails.html', {'f_form': f_form})


def delete_fooddetails(request, id):
    Food.objects.get(id=id).delete()
    messages.info(request, 'Deleted Successfully')
    return redirect('view_fooddetails')


def add_notifications(request):
    n_form = notification_details()
    if request.method == 'POST':
        n_form = notification_details(request.POST)
        if n_form.is_valid():
            n_form.save()
            messages.info(request, 'Notification Added')
            return redirect('view_notifications')
    return render(request, 'admin/add_notifications.html', {'n_form': n_form})


def view_notifications(request):
    data = Notifications.objects.all()
    return render(request, 'admin/view_notifications.html', {'data': data})


def update_notifications(request, id):
    data = Notifications.objects.get(id=id)
    n_form = notification_details(instance=data)
    if request.method == 'POST':
        n_form = notification_details(request.POST, instance=data)
        if n_form.is_valid():
            n_form.save()
            messages.info(request, 'Updated Successfully')
            return redirect('view_notifications')
    return render(request, 'admin/update_notifications.html', {'n_form': n_form})


def delete_notifications(request, id):
    Notifications.objects.get(id=id).delete()
    messages.info(request, 'Notification Deleted')
    return redirect('view_notifications')


def add_warden(request):
    u_form = UserRegister()
    w_form = warden_details()
    if request.method == 'POST':
        u_form = UserRegister(request.POST)
        w_form = warden_details(request.POST, request.FILES)
        if u_form.is_valid and w_form.is_valid():
            user = u_form.save(commit=False)
            user.is_warden = True
            user.save()
            warden = w_form.save(commit=False)
            warden.user = user
            warden.save()
            messages.info(request, 'Registered Successfully')
            return redirect('view_warden')
    return render(request, 'admin/add_warden.html', {'u_form': u_form, 'w_form': w_form})


def view_warden(request):
    data = Warden.objects.all()
    return render(request, 'admin/view_warden.html', {'data': data})


def update_warden(request, id):
    data = Warden.objects.get(user_id=id)
    w_form = warden_details(instance=data)
    if request.method == 'POST':
        w_form = warden_details(request.POST, request.FILES, instance=data)
        if w_form.is_valid():
            w_form.save()
            messages.info(request, 'Updated Successfully')
            return redirect('view_warden')
    return render(request, 'admin/update_warden.html', {'w_form': w_form})


def delete_warden(request, id):
    data1 = Warden.objects.get(user_id=id)
    data = User.objects.get(warden=data1)
    data.delete()
    messages.info(request, 'Deleted Successfully')
    return redirect('view_warden')


def view_student_registration(request):
    student = Student.objects.all()
    return render(request, 'admin/view_student_registration.html', {'student': student})


def view_parent_registration(request):
    parent = Parent.objects.all()
    return render(request, 'admin/view_parent_registration.html', {'parent': parent})


def approve_student(request, id):
    student = Student.objects.get(user_id=id)
    student.approval_status = True
    student.save()
    messages.info(request, "Registered Successfully")
    return redirect('view_student_registration')


def reject_student(request, id):
    data1 = Student.objects.get(user_id=id)
    data = User.objects.get(student=data1)
    data.delete()
    messages.info(request, 'Deleted Successfully')
    return redirect('view_student_registration')


def approve_parent(request, id):
    parent = Parent.objects.get(user_id=id)
    parent.approval_status = True
    parent.save()
    messages.info(request, "Registered Successfully")
    return redirect('view_parent_registration')


def reject_parent(request, id):
    data1 = Parent.objects.get(user_id=id)
    data = User.objects.get(parent=data1)
    data.delete()
    messages.info(request, 'Deleted Successfully')
    return redirect('view_parent_registration')


def view_room_booked(request):
    return render(request, 'admin/view_room_booked.html')


def view_reviews(request):
    data = Reviews.objects.all()
    data2 = ParentReviews
    return render(request, 'admin/view_reviews.html', {'data': data})


def view_complaints(request):
    data = Complaints.objects.all()
    return render(request, 'admin/view_complaints.html', {'data': data})


def complaint_reply(request, id):
    data = Complaints.objects.get(id=id)
    if request.method == 'POST':
        r = request.POST.get('reply')
        data.reply = r
        data.save()
        messages.info(request, 'Complaint Reply send ')
        return redirect('view_complaints')
    return render(request, 'admin/complaint_reply.html', {'data': data})


def room_booked(request):
    data = BookRoom.objects.all()
    return render(request, 'admin/view_room_booked.html', {'data': data})


def confirm_room_booked(request, id):
    details_qs = Hostel.objects.all()
    if details_qs.exists():
        book = BookRoom.objects.get(id=id)
        book.status = 1
        book.save()
        hstl = Hostel.objects.all().last()  # validation ie the last
        Vacant_rooms = hstl.Vacant_rooms
        hstl.Vacant_rooms = int(Vacant_rooms) - 1
        hstl.save()
        messages.info(request, 'Room Booking Confirmed')
        return redirect('room_booked')

    else:
        messages.info(request,
                      'Please Update Hostel Details')  # if we didn't enter anything inside hosteldetails this msg appears
        return redirect('room_booked')


def reject_room_booked(request, id):
    book = BookRoom.objects.get(id=id)
    book.status = 2
    book.save()
    messages.info(request, 'Booking Rejected ')
    return redirect('room_booked')


def add_attendance(request):
    data = Student.objects.filter(approval_status=True)
    return render(request, 'admin/add_attendance.html', {'data': data})


now = datetime.datetime.now()


def mark_attendance(request, id):
    user = Student.objects.get(user_id=id)
    data = Attendance.objects.filter(student=user, date=datetime.date.today())
    if data.exists():
        messages.info(request, "Today's Attendance Already marked for this Student")
        return redirect('add_attendance')
    else:
        if request.method == 'POST':
            a = request.POST.get('attendance')
            if a is None:
                messages.info(request, 'Attendance must be marked')
            else:
                Attendance(student=user, date=datetime.date.today(), attendance=a, time=now.time()).save()
                messages.info(request, 'Attendance Added Successfully')
                return redirect('add_attendance')
    return render(request, 'admin/mark_attendance.html')


def view_attendance(request):
    date_list = Attendance.objects.values_list('date', flat=True).distinct()
    # attendances = {}
    # for i in date_list:
    #     attendances[i] = Attendance.objects.filter(date=i)
    return render(request, 'admin/view_attendance.html', {'date_list': date_list})


def day_attendance(request, date):
    attendance = Attendance.objects.filter(date=date)
    context = {
        "attendance": attendance,
        "date": date
    }
    return render(request, 'admin/day_attendance.html', context)


def add_payment(request):
    form = PaymentForm()
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_form = form.save(commit=False)
            payment_form.bill_no = payment_form.student.pk
            # print(payment_form.student)  # name is printed
            payment_qs = Payment.objects.filter(student=payment_form.student,
                                                bill_start_date=payment_form.bill_start_date,
                                                bill_end_date=payment_form.bill_end_date)
            payment_qs2 = Payment.objects.filter(student=payment_form.student, bill_end_date=payment_form.bill_end_date)
            booking = BookRoom.objects.get(student=payment_form.student, status=1)
            print(booking.status)
            if booking.status == 2:
                messages.info(request, 'Booking Rejected')
            elif payment_qs.exists():
                messages.info(request, 'Payment already added for this student in this duration')
            elif payment_qs2.exists():
                messages.info(request, 'Payment already added for this student in this duration')
            else:
                payment_form.save()
                messages.info(request, 'Payment added Successfully')
                return redirect('view_payment')
    return render(request, 'admin/add_payment.html', {'form': form})


def payment_load_to_form(request):
    selected_student_id = request.GET.get('studentId')
    student = Student.objects.get(user_id=selected_student_id)
    if not Payment.objects.filter(student=student).exists():
        booking = BookRoom.objects.get(student=student, status=1)
        bill_start_date = booking.booking_date
        current_month = bill_start_date.month
        last_day = calendar.monthrange(bill_start_date.year, current_month)[1]
        bill_end_date = bill_start_date.replace(day=last_day)

    else:
        current_date = datetime.date.today()
        last_date_previous_month = current_date.replace(day=1) - timedelta(days=1)
        bill_end_date = last_date_previous_month
        first_date_previous_month = last_date_previous_month.replace(day=1)
        bill_start_date = first_date_previous_month
    present_days = Attendance.objects.filter(student=student, date__range=[bill_start_date, bill_end_date]).count()
    mess_bill = present_days * 60
    hostel = Hostel.objects.all().last()
    hostel.Rent = ''.join(hostel.Rent[:-2])
    amount = int(hostel.Rent) + mess_bill
    data = {
        'bill_start_date': bill_start_date,
        'bill_end_date': bill_end_date,
        'mess_bill': mess_bill,
        'amount': amount,
    }
    return JsonResponse(data)


def view_payment(request):
    payments = Payment.objects.all()
    return render(request, 'admin/view_payment.html', {'payments': payments})


def payment_delete(request, id):
    Payment.objects.get(id=id).delete()
    return redirect('view_payment')


def admin_view_bill(request, id):
    payment = Payment.objects.get(id=id)
    hostel = Hostel.objects.all().last()
    student = Student.objects.get(name=payment.student)
    context = {
        'payment': payment,
        'hostel': hostel,
        'student': student
    }
    return render(request, 'student/view_bill.html', context)
