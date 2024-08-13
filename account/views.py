from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from rest_framework import viewsets

from .models import *
from .serializers import *
from .forms import CreateUserForm, MemberForm


def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            # одновременно с регистрацией пользователя создаем объект модели участника чата
            Member.objects.create(
                user=user,
                name=user.username,
            )

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')

    context = {'form': form}
    return render(request, 'register.html', context)


def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('../../chat/')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'login.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')


@login_required(login_url='/account/login/')
def personalSettings(request):
	member = request.user.member
	form = MemberForm(instance=member)

	if request.method == 'POST':
		form = MemberForm(request.POST, request.FILES, instance=member)
		if form.is_valid():
			form.save()

	context = {'form':form}
	return render(request, 'personal.html', context)


# сериалайзеры

class MemberViewset(viewsets.ModelViewSet):
   queryset = Member.objects.all()
   serializer_class = MemberSerializer