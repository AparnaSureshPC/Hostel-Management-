import datetime

from django.contrib import messages
from django.shortcuts import render, redirect

from app.forms import InOutForm
from app.models import Hostel, Parent, Student, Complaints, Reviews, ParentReviews, LeaveApplication, InOut


def warden_card(request):
    return render(request, 'warden/card.html')


def view_warden_hostel(request):
    data = Hostel.objects.all()
    return render(request, 'warden/view_hosteldetails.html', {'data': data})


def warden_view_parents(request):
    parents = Parent.objects.all()
    return render(request, 'warden/view_parents.html', {'parents': parents})


def warden_view_students(request):
    students = Student.objects.all()
    return render(request, 'warden/view_students.html', {'students': students})


def warden_view_complaints(request):
    complaints = Complaints.objects.all()
    return render(request, 'warden/view_complaints.html', {'complaints': complaints})


def warden_view_reviews(request):
    s_reviews = Reviews.objects.all()
    p_reviews = ParentReviews.objects.all()


def warden_view_leave_applications(request):
    leave_applications = LeaveApplication.objects.all()
    return render(request, 'warden/view_leave_applications.html', {'leave_applications': leave_applications})


def warden_approve_leave(request, id):
    leave_application = LeaveApplication.objects.get(id=id)
    leave_application.status = 1
    leave_application.save()
    messages.info(request, 'Leave Approved')
    return redirect('warden_view_leave_applications')


def warden_reject_leave(request, id):
    leave_application = LeaveApplication.objects.get(id=id)
    leave_application.status = 2
    leave_application.save()
    messages.info(request, 'Leave Rejected')
    return redirect('warden_view_leave_applications')


time_now = datetime.datetime.now()


def student_in_out(request):
    form = InOutForm()
    if request.method == 'POST':
        form = InOutForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_student_inout')
    return render(request, 'warden/student_in_out_register.html', {'form': form})


def view_student_inout(request):
    # inout = InOut.objects.all()
    # return render(request, 'warden/view_student_inout.html', {'inout': inout})
    dates = InOut.objects.values_list('date', flat=True).distinct()
    return render(request, 'warden/view_student_inout.html', {'dates': dates})


def date_based_inout(request, date):
    date_inout = InOut.objects.filter(date=date)
    context = {
        'date_inout': date_inout,
        'date': date
    }
    return render(request, 'warden/date_based_inout.html', context)


def update_student_inout(request, id):
    inout = InOut.objects.get(id=id)
    form = InOutForm(instance=inout)
    if request.method == 'POST':
        form = InOutForm(request.POST, instance=inout)
        if form.is_valid():
            form.instance.status = 1
            form.save()
            return redirect('view_student_inout')
    return render(request, 'warden/update_student_inout.html', {'form': form})
