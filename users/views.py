from courses.forms import AddCourseForm
from courses.models import Course
from .forms import *

from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect


def home(request):
    title = 'eLearning'

    context = {
        "title": title,
    }

    return render(request, "home.html", context)


def about(request):
    title = 'About'

    context = {
        "title": title,
    }

    return render(request, "users/about.html", context)


def contact(request):
    title = 'Contact'

    context = {
        "title": title,
    }

    return render(request, "users/contact.html", context)


@login_required
def profile(request):
    if request.user.is_site_admin:
        return redirect(reverse('admin'))

    elif request.user.is_professor:
        return redirect(reverse('professor'))

    return redirect(reverse('student'))


@user_passes_test(lambda user: user.is_site_admin)
def admin(request):
    title = 'Admin'
    add_user_form = AddUser(request.POST or None)
    queryset = UserProfile.objects.all()

    context = {
        "title": title,
        "add_user_form": add_user_form,
        "queryset": queryset,
    }

    if add_user_form.is_valid():
        instance = add_user_form.save(commit=False)
        passwd = add_user_form.cleaned_data.get("password")
        instance.password = make_password(password=passwd,
                                          salt='salt', )
        instance.save()
        reverse('profile')

    return render(request, "users/sysadmin_dashboard.html", context)


@user_passes_test(lambda user: user.is_professor)
def professor(request):
    title = 'Professor'
    add_course_form = AddCourseForm(request.POST or None)
    queryset_course = Course.objects.filter(user__username=request.user)

    context = {
        "title": title,
        "add_course_form": add_course_form,
        "queryset_course": queryset_course,
    }

    if add_course_form.is_valid():
        instance = add_course_form.save(commit=False)
        instance.user = request.user
        instance.save()
        return redirect(instance.get_absolute_url())

    return render(request, "users/professor_dashboard.html", context)


@login_required
def student(request):
    title = 'Student'

    context = {
        "title": title,
    }

    return render(request, "users/student_dashboard.html", context)


@user_passes_test(lambda user: user.is_site_admin)
def update_user(request, username):
    user = UserProfile.objects.get(username=username)
    data_dict = {'username': user.username, 'email': user.email}
    update_user_form = EditUser(initial=data_dict, instance=user)
    title = 'Edit users'

    context = {
        "title": title,
        "update_user_form": update_user_form,
    }

    if request.POST:
        user_form = EditUser(request.POST, instance=user)

        if user_form.is_valid():
            instance = user_form.save(commit=False)
            passwd = user_form.cleaned_data.get("password")

            if passwd:
                instance.password = make_password(password=passwd,
                                                  salt='salt', )
            instance.save()

            return redirect(reverse('profile'))

    return render(request, "users/edit_user.html", context)


@user_passes_test(lambda user: user.is_site_admin)
def delete_user(request, username):
    user = UserProfile.objects.get(username=username)
    user.delete()
    return redirect(reverse('profile'))