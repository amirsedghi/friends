from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from . import models
from .models import User, Friend
from django.db.models import Q
import bcrypt
import datetime
import re
import unicodedata

val_regex =re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your views here.
def index(request):
    request.session['id'] = 0
    return render(request, 'friendship/index.html')

def register(request):
    request.session['message']=[]
    request.session['check'] = 1
    any_user = User.objects.filter(email = request.POST['email'])
    if len(request.POST['fullname'])<1:
        message = "Name cannot be empty"
        request.session['check'] = 0
        request.session['message'].insert(0, message)
    if not val_regex.match(request.POST['email']):
        message = "Please enter a valid email"
        request.session['check'] = 0
        request.session['message'].insert(0, message)
    if len(request.POST['alias'])<1:
        message = "Please choose and alias"
        request.session['check'] = 0
        request.session['message'].insert(0, message)
    if request.POST['password'] != request.POST['password_confirm']:
        message = "Password do not match"
        request.session['check'] = 0
        request.session['message'].insert(0, message)
    if len(request.POST['password'])<8:
        message = 'Password must be 8 characters or longer'
        request.session['message'].insert(0, message)
        request.session['check'] = 0
    if any_user:
        message = 'This email has already been used'
        request.session['message'].insert(0, message)
        request.session['check'] = 0
    if request.session['check'] == 1:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode('utf-8'), bcrypt.gensalt())
        User.objects.create(name = request.POST['fullname'], alias = request.POST['alias'], email = request.POST['email'], password = pw_hash, date_of_birth = request.POST['date'])
        the_user = User.objects.get(email = request.POST['email'])
        request.session['id'] = the_user.id
        return redirect('/friends')
    else:
        return redirect('/')


def login(request):
    request.session['message'] = []
    the_user = User.objects.filter(email = request.POST['email'])
    if the_user:
        if bcrypt.hashpw(request.POST['password'].encode('utf-8'), the_user[0].password.encode('utf-8')) == the_user[0].password:
            request.session['id'] = the_user[0].id
            return redirect('/friends')
        else:
            message = "Your input did not match our record"
            request.session['message'].insert(0, message)
            return redirect('/')
    else:
        message = "Your input did not match our record"
        request.session['message'].insert(0, message)
        return redirect('/')

def friends(request):
    the_user = User.objects.get(id = request.session['id'])
    print the_user.alias
    print '#############'
    friends = User.objects.filter(the_friend_of__friends__id = request.session['id'])
    test = User.objects.filter(the_friend_of__friends__alias = 'Amir')
    print '^^^^^^^^^^^^^^^^^^^^'
    print test
    the_rest = User.objects.filter(~Q(the_friend_of__friends__id = request.session['id'])).filter(~Q(id = request.session['id']))
    context = {'user' : the_user, 'friends': friends, 'rest': the_rest}
    return render(request, 'friendship/friends.html', context)

def add(request, id):
    the_user = User.objects.filter(id = request.session['id'])
    friend = User.objects.filter(id = id)
    Friend.objects.create(friends = friend[0], friend_of = the_user[0])
    Friend.objects.create(friends = the_user[0], friend_of = friend[0])
    return redirect('/friends')

def delete(request, id):
    not_friend= User.objects.get(id = id)
    Friend.objects.filter(friend_of__id = request.session['id'], friends = not_friend).delete()
    Friend.objects.filter(friend_of__id = id, friends = request.session['id']).delete()
    return redirect('/friends')

def user(request, id):
    user = User.objects.get(id = id)
    context = {'user': user}
    return render(request, 'friendship/user.html', context)
