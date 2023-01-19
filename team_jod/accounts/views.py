from django.shortcuts import render, redirect
from .models import UserAccount
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate



def register(request):
    if request.method == 'POST':
        Firstname = request.POST.get('FirstName')
        Surname = request.POST.get('Surname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        user_acc = User.objects.create_user(
                first_name = Firstname,
                last_name = Surname,
                email = email,
                username = username,
                password = password,
        )
        user_acc.save()

        request.session['uid']=str(user_acc.id)

        user_account = UserAccount.objects.create(firstname = Firstname, 
                                                    surname = Surname, 
                                                    username = username, 
                                                    email = email, 
                                                    phone = phone)
                                                    
        user_account.save()
        user = authenticate(username=username, password=password)
        login(request, user)

        return redirect ('/')
    
    else:
        return render(request,'register.html')


def login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username = username, password = password)
        uid = user.id
        request.session['uid'] = str(uid)
        if user is not None:
            auth.login(request,user)

            return redirect ('/')
        else:

            return render(request,'login.html')
    else:

        return render(request,'login.html')