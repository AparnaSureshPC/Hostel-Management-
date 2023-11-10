from django.contrib import auth, messages
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
# Create your views here.
from app.forms import UserRegister, Studentreg, Parentreg
from app.models import Reviews, Student, Hostel


def homepage(request):
    hostel = Hostel.objects.all().last()
    reviews = Reviews.objects.all()
    return render(request, 'index.html', {'reviews': reviews,'hostel': hostel})


def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # 'username' is the name of the input field
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_card')
        if user is not None and user.is_warden:
            login(request, user)
            return redirect('warden_card')
        elif user is not None and user.is_student:
            if user.student.approval_status == 1:
                login(request, user)
                return redirect('card')
            else:
                messages.info(request, 'You  Are Not Approved To Login in')
        elif user is not None and user.is_parent:
            if user.parent.approval_status == 1:
                login(request, user)
                return redirect('parent_card')
            else:
                messages.info(request, 'You  Are Not Approved To Login in')
        else:
            messages.info(request, 'Not Registered User')

    return render(request, 'login.html')


def student_reg(request):
    u_form = UserRegister()  # we have imported these forms
    s_form = Studentreg()
    if request.method == 'POST':
        u_form = UserRegister(request.POST)
        s_form = Studentreg(request.POST, request.FILES)
        if u_form.is_valid() and s_form.is_valid():
            user = u_form.save(commit=False)
            user.is_student = True
            user.save()
            student = s_form.save(commit=False)
            student.user = user
            student.save()
            messages.info(request, 'Registered Successfully')
            return redirect('loginpage')
    return render(request, 'student_reg.html', {'u_form': u_form, 's_form': s_form})


def parent_reg(request):
    u_form = UserRegister()
    p_form = Parentreg()
    if request.method == 'POST':
        u_form = UserRegister(request.POST)
        p_form = Parentreg(request.POST, request.FILES)
        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save(commit=False)
            user.is_parent = True
            user.save()
            parent = p_form.save(commit=False)
            parent.user = user
            parent.save()
            messages.info(request, 'Registered Successfully')
            return redirect('loginpage')
    return render(request, 'parent_reg.html', {'u_form': u_form, 'p_form': p_form})


def admin_page(request):
    return render(request, 'admin_page.html')


def parent_page(request):
    return render(request, 'parent_page.html')


def student_page(request):
    return render(request, 'student_page.html')


def warden_page(request):
    return render(request, 'warden_page.html')


def log_out(request):
    logout(request)
    return redirect('homepage')






