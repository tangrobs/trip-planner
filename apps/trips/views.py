from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Trip, Agenda, Activity
import bcrypt

def index(request):
    return render(request, "trips/index.html")

def signin(request):
    errors = User.objects.validate_signin(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id
        return redirect('/profile')

def register(request):
    return render(request, "trips/register.html")

def register_process(request):
    errors = User.objects.validate_register(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register')
    else:
        hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hash)
        user.save()
        messages.success(request, "Account successfully registered")
        return redirect('/')

def profile(request):
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
        'trips': Trip.objects.filter(admin=user) | Trip.objects.filter(attended_by=user),
    }
    return render(request, 'trips/profile.html', context)

def newTrip(request):
    return render(request, 'trips/newTrip.html')

def newTrip_process(request):
    errors = User.objects.validate_trip(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/trips/new')
    else:
        user = User.objects.get(id=request.session['user_id'])
        Trip.objects.create(title=request.POST['title'], description=request.POST['description'], date_from=request.POST['date_from'], date_to=request.POST['date_to'], admin=user).save()
        return redirect('/profile')

def plan(request, tripID):
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
        'trip': Trip.objects.get(id=tripID),
    }
    return render(request, 'trips/plan.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

def tryIt(request):
    return render(request, 'trips/try.html')
