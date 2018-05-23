from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Trip, Agenda, Activity
import bcrypt, datetime
# from google.oauth2 import id_token
# from google.auth.transport import requests

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

def googleSignin(request):
    # (Receive token by HTTPS POST)
    id_token = request.POST['idtoken']
    print("my id token is: ", id_token)

    # try:
    #     # Specify the CLIENT_ID of the app that accesses the backend:
    #     idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
    #
    #     # Or, if multiple clients access the backend server:
    #     # idinfo = id_token.verify_oauth2_token(token, requests.Request())
    #     # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
    #     #     raise ValueError('Could not verify audience.')
    #
    #     if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
    #         raise ValueError('Wrong issuer.')
    #
    #     # If auth request is from a G Suite domain:
    #     # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
    #     #     raise ValueError('Wrong hosted domain.')
    #
    #     # ID token is valid. Get the user's Google Account ID from the decoded token.
    #     userid = idinfo['sub']
    # except ValueError:
    #     # Invalid token
    #     pass
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
        'trips_invited_to': Trip.objects.filter(invited=user),
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
        trip = Trip.objects.create(title=request.POST['title'], description=request.POST['description'], date_from=request.POST['date_from'], date_to=request.POST['date_to'], admin=user)
        trip.save()
        Agenda.objects.create(day=1, date=datetime.date.today(), trip=trip)
        return redirect('/profile')

def plan(request, tripID):
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=tripID)
    context = {
        'user': user,
        'trip': Trip.objects.get(id=tripID),
        'agendas': Agenda.objects.filter(trip=trip).exclude(day=1),
    }
    if user.id == trip.admin.id:
        return render(request, 'trips/plan_admin.html', context)
    return render(request, 'trips/plan.html', context)

def agenda(request, tripID):
    trip = Trip.objects.get(id=tripID)
    context = {
        'agendas': Agenda.objects.filter(trip=trip).exclude(day=1),
    }
    return render(request, 'trips/agenda.html', context)

def newAgenda(request, tripID):
    trip = Trip.objects.get(id=tripID)
    numAgenda = len(Agenda.objects.filter(trip=trip)) + 1
    agenda = Agenda.objects.create(day=numAgenda, date=datetime.date.today(), trip=trip)
    agenda.save()
    context = {
        'agendas': Agenda.objects.filter(trip=trip).exclude(day=1),
    }
    return render(request, 'trips/agenda_tabs.html', context)

def agendaContent(request, tripID):
    trip = Trip.objects.get(id=tripID)
    context = {
        'agendas': Agenda.objects.filter(trip=trip).exclude(day=1),
    }
    return render(request, 'trips/agenda_tabcontents.html', context)

def addTravelBuddy(request, tripID):
    trip = Trip.objects.get(id=tripID)
    user_signed_in = User.objects.get(id=request.session['user_id'])
    context = {
        'user_signed_in': user_signed_in,
        'users': User.objects.exclude(trips_invited_to=trip).exclude(id=request.session['user_id']).exclude(trips_attending=trip),
        'trip': trip,
        'invited': User.objects.filter(trips_invited_to=trip),
        'attended_by': User.objects.filter(trips_planned=trip) | User.objects.filter(trips_attending=trip),
    }
    if user_signed_in.id == trip.admin.id:
        return render(request, 'trips/addTravelBuddy_admin.html', context)
    return render(request, 'trips/addTravelBuddy.html', context)

def addTravelBuddy_process(request, tripID, userID):
    Trip.objects.get(id=tripID).invited.add(User.objects.get(id=userID))
    context = {
        'users': User.objects.all(),
        'trip': Trip.objects.get(id=tripID),
    }
    return redirect('/trips/plan/{}/add_travelbuddy'.format(tripID))

def joinTrip(request, tripID):
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=tripID)
    trip.attended_by.add(user)
    trip.invited.remove(user)
    return redirect('/profile')

def logout(request):
    request.session.clear()
    return redirect('/')

def tryIt(request):
    return render(request, 'trips/try.html')
