from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.contrib.auth.decorators import login_required



# signup function .email consider username
def Signup(request): 
    if request.method == 'POST':
        username=request.POST.get('username')
        email=request.POST.get('username')
        pass1=request.POST.get('password')
        pass2=request.POST.get('conf_password')
        if pass1 != pass2:
            return render(request,'Sign_up.html',{'message':'password and confirm password does not match'})
        try:
                User.objects.create_user(username,email,pass1)
                return redirect('Login')
        except IntegrityError:
            return render(request,'Sign_up.html',{'message':'The User already exists'})   
        
    return render(request,'Sign_up.html')



# login function
def Loginpage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username = username,password = password)
        if user is not None:
            login(request,user)
            return redirect('account_home')
        else:
            return render(request,'login.html',{'message':'The User is not found!'})
    return render(request,'login.html')


# upload function it is used to upload audio file.after loging only able to upload file
@login_required(login_url="Login")
def Upload(request):
    emails_list=User.objects.all()
    if request.method == 'POST':
        Title=request.POST.get('title')
        File=request.FILES.get('file')
        Privacy=request.POST.get('mode')
        Uploader =User.objects.get(id=request.user.id)
        audio=MusicFile.objects.create(title=Title,file=File,privacy=Privacy,uploader=Uploader)
        emails=request.POST.getlist('emails')
        if Privacy == 'protected':
            for email in emails:
                user=User.objects.get(email=email)
                AllowedUser.objects.create(music_file=audio,user=user)

        return redirect('account_home')
    context={
            'email_list':emails_list,
        }
    return render(request,'upload_music.html' ,context)


# first page.withoutlogin it's work ,in this page list public audio file.
def home(request):
    musics=MusicFile.objects.filter(privacy='public')
    context={
            'musics':musics,
        }
    return render(request,'home.html',context)


# music player for public audio player
def public_musicplayer(request,id):
    music=MusicFile.objects.get(id=id)
    if music.privacy == 'public':
        return render(request,'music_player.html',{'music':music})


#music player for private and protect audio file  
@login_required(login_url="Login")
def musicplayer(request,id):
    music=MusicFile.objects.get(id=id)
    return render(request,'music_player.html',{'music':music})
        

#it's a account home page.here listed public audio file.after login only we will access the page
@login_required(login_url="Login")
def account_home(request):
    musics=MusicFile.objects.filter(privacy='public')
    context={
            'musics':musics,
        }
    return render(request,'account_public.html',context)


#it's is protect page ,here listed protected audio file.after login only we get access
@login_required(login_url="Login")
def account_protect(request):
    user=User.objects.get(id=request.user.id)
    allow_user=AllowedUser.objects.filter(user=user)
    context={
            'musics':allow_user,
        }
    return render(request,'account_protect.html',context)


#it's is private page ,here listed private audio file.after login only we get access
@login_required(login_url="Login")
def account_private(request):
    id=request.user.id
    user=User.objects.get(id=id)
    musics=MusicFile.objects.filter(privacy='private', uploader=user)
    context={
            'musics':musics,
        }
    return render(request,'account_private.html',context)


#it's is uploaded page ,here listed all uploade file by the current user.
@login_required(login_url="Login")
def account_upload(request):
    id=request.user.id
    user=User.objects.get(id=id)
    musics=MusicFile.objects.filter(uploader=user)
    context={
            'musics':musics,
        }
    return render(request,'account_upload.html',context)


def logout_page(request):
    logout(request)
    return redirect('home')
    

