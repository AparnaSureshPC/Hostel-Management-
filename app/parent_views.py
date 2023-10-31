import stripe
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from app.forms import BookRoomForm, ComplaintForm, ParentReviewsForm
from app.models import Hostel, Attendance, Parent, BookRoom, Student, Warden, Complaints, ParentReviews, InOut, \
    Payment


def parent_card(request):
    return render(request, 'parent/card.html')


def view_hostel_details(request):
    hostel = Hostel.objects.all()
    return render(request, "parent/view_hostel_details.html", {'hostel': hostel})


def parent_view_attendance(request):
    parent = Parent.objects.get(user=request.user)
    attendance = Attendance.objects.filter(student=parent.student_name)
    return render(request, 'parent/view_attendance.html', {'attendance': attendance})


def parent_book_room(request):
    parent = Parent.objects.get(user=request.user)
    form = BookRoomForm()
    if request.method == 'POST':
        form = BookRoomForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.student = parent.student_name
            book.booked_by = request.user
            student_qs = BookRoom.objects.filter(student=parent.student_name)
            if student_qs.exists():
                messages.info(request, 'Already Booked')
            else:
                book.save()
                messages.info(request, 'Successfully Booked')
                return redirect('parent_card')
    return render(request, 'parent/book_room.html', {'form': form})


def parent_booking_status(request):
    data = BookRoom.objects.filter(booked_by=request.user)
    return render(request, 'parent/booking_status.html', {'data': data})


def parent_delete_account(request):
    user = request.user
    user.delete()
    messages.info(request, 'Your Account Deleted Successfully')
    return redirect('loginpage')


def parent_view_warden(request):
    data = Warden.objects.all()
    return render(request, 'parent/view_warden.html', {'data': data})


def parent_add_complaint(request):
    form = ComplaintForm()
    user = request.user
    if request.method == "POST":
        form = ComplaintForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = user
            obj.save()
            messages.info(request, 'Complaint added Successfully')
            return redirect('parent_complaint_view')
    return render(request, 'parent/add_complaint.html', {'form': form})


def parent_complaint_view(request):
    complaints = Complaints.objects.filter(user=request.user)
    return render(request, 'parent/complaint_view.html', {'complaints': complaints})


def parent_add_reviews(request):
    form = ParentReviewsForm()
    user = request.user
    if request.method == 'POST':
        form = ParentReviewsForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = user
            obj.save()
            messages.info(request, 'Review added Successfully')
            return redirect('parent_view_reviews')
    return render(request, 'parent/add_reviews.html', {'form': form})


def parent_view_reviews(request):
    reviews = ParentReviews.objects.filter(user=request.user)
    return render(request, 'parent/view_reviews.html', {'reviews': reviews})


def parent_review_update(request, id):
    reviews = ParentReviews.objects.get(id=id)
    form = ParentReviewsForm(instance=reviews)
    if request.method == 'POST':
        form = ParentReviewsForm(request.POST, instance=reviews)
        if form.is_valid():
            form.save()
            return redirect('parent_view_reviews')
    return render(request, 'parent/review_update.html', {'form': form})


def parent_reviews_delete(request, id):
    ParentReviews.objects.get(id=id).delete()
    return redirect('parent_view_reviews')


def parent_student_inout(request):
    parent = Parent.objects.get(user=request.user)
    student = parent.student_name
    inout = InOut.objects.filter(student=student)
    return render(request, 'parent/student_inout.html', {'inout': inout})


def parent_view_fee(request):
    parent = Parent.objects.get(user=request.user)
    payments = Payment.objects.filter(student=parent.student_name)
    return render(request, 'parent/view_fees.html', {'payments': payments})


def parent_view_bill(request, id):
    payment = Payment.objects.get(id=id)
    hostel = Hostel.objects.all().last()
    student = Student.objects.get(name=payment.student)
    context = {
        'payment': payment,
        'hostel': hostel,
        'student': student
    }
    return render(request, 'parent/view_bill.html', context)


stripe.api_key = 'sk_test_51NvD3cSAMEcakUFvLSLt5GjlZjGN1jQzJv72cU1k4e8TsAEBz2O5soSlZPnA5N8DDo7hhfIHY4F4xhWpSt1RHJ3w00rxo0NXB0'


def checkout_session(request, id):
    payment = Payment.objects.get(pk=id)
    stripe.api_key = stripe.api_key
    amount_in_cents = int(payment.amount * 100)
    parent = Parent.objects.get(user=request.user)
    parent_email = parent.email
    session = stripe.checkout.Session.create(
        success_url='http://127.0.0.1:8000/pay_success/?payment_id={}'.format(payment.id),
        cancel_url='http://127.0.0.1:8000/pay_cancelled',
        payment_method_types=['card'],
        mode='payment',
        line_items=[
            {
                'price_data': {
                    'currency': 'inr',
                    'unit_amount': amount_in_cents,
                    'product_data': {
                        'name': payment.student,
                    },
                },
                'quantity': 1,
            }
        ],
        customer_email=parent_email
    )
    return redirect(session.url, code=303)


def pay_success(request):
    # You might want to pass the payment ID as a query parameter in your success URL
    payment_id = request.GET.get('payment_id')
    # Retrieve the Payment object
    payment = get_object_or_404(Payment, pk=payment_id)
    payment.status = 1
    payment.save()
    return render(request, 'parent/payment_success.html')


def pay_cancelled(request):
    return render(request, 'parent/payment_failed.html')


def success_return(request):
    return redirect('parent_card')