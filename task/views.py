from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request,'home.html')


def register(request):

    if request.method == 'GET':

        return render(request,'register.html', {
            'form' : UserCreationForm
        } )   

    else: 
        if request.POST['password1'] == request.POST['password2']:

            try: 
                
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                
                login(request, user)
               
                return redirect('tasks')
                
            except:
                return render (request,'register.html', { 
                    'form' : UserCreationForm ,
                    "error": 'Usuário já existe'
                    
                    } ) 
           
        return render (request,'register.html', { 
                    'form' : UserCreationForm ,
                    "error": 'senhas são diferentes'
                    
                    } ) 

def login_view(request):

    if request.method == 'GET':
        return render(request,'login_view.html', {
        'form': AuthenticationForm
        })

    else:
        user = authenticate(

            request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'login_view.html', {
                    'form' : AuthenticationForm,
                    'error': 'Usuário ou senha está incorreto'
                })

        else:
                login(request, user)
                return redirect('tasks')    


@login_required   
def sair(request):
    logout (request)
    return redirect('home')

@login_required       
def tasks(request):
    return render(request,'tasks.html')