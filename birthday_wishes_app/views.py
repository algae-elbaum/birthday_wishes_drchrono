from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import logout as django_logout
from urllib import urlencode
import requests, datetime, pytz
from globs import redirect_uri, client_id, client_secret, msg_max, subj_max
from models import Patient, Doctor
from forms import UserForm

def home(request):
    context = {'logged_in': request.user.is_authenticated()}
    # Must be a doctor to be here (admins need to pretend to be doctors)
    if context['logged_in'] and not hasattr(request.user, 'doctor'):
        return redirect('logout')
    if context['logged_in']:
        # Get list of all the user's patients to send out in the response 
        patient_list = request.user.doctor.get_local_patient_list()
        context['patient_list'] = patient_list
    return render(request, 'birthday_wishes.html', context)

@login_required
def patient_page(request, uid):
    doctor = request.user.doctor
    # If it's a POST, set the patient's fields according to the form
    if request.method == 'POST':
        activated = request.POST.get('checkbox', False)
        msg = request.POST['msg']
        subj = request.POST['subj']
        time = request.POST['time']
        doctor.patient_set.filter(uid=uid).update(msg_active = activated, 
                                                  message = msg[:msg_max], 
                                                  subject = subj[:subj_max],
                                                  message_time = time)
        return redirect(home)
    # Otherwise send the user to the form
    else:
        patient = doctor.patient_set.get(uid=uid)
        context = {'patient': patient,
                   'msg_max': msg_max,
                   'subj_max': subj_max}
        return render(request, 'patient_page.html', context)

@login_required
def refresh_patients(request):
    # If by some hackery the user is logged in but still got to this page 
    # without authenticating:
    try:
        request.user.doctor.update_patient_list()
        return redirect('home')
    except:
        # We don't want to use it as a view, we just want its side effects
        return redirect ('authorize')
        request.user.doctor.update_patient_list()
        return redirect('home')

def about(request):
    return render(request, 'about.html')

def logout(request):
    # If the user was a properly logged in user with a username, remind them
    # to also log out with drchrono
    if hasattr(request.user, 'doctor') and request.user.doctor.username:
        username = request.user.doctor.username
        django_logout(request)
        return render(request, 'logout.html', {'username':username})
    # Otherwise just bring them home
    else:
        django_logout(request)
        return redirect('home')

def register(request):
    # If there's a user logged in, require them to log out
    if request.user.is_authenticated():
        return redirect('manual_logout')
    # If it's post, the user has sent us their info and we need to try to set them up
    if request.method == 'POST':
        success = False
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            # Save the user and associate it with a new Doctor
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            doctor = Doctor()
            doctor.user = user
            doctor.save()
            success = True
            
        # Registration done, let's get out of here.
        # (note: I'm not actually sure whether it'd be more appropriate to
        # have a new view for the result and redirect to it. That sort of thing
        # seems common, but this seems simpler)
        return render(request, 'registration_report.html', {'success': success, 'user_form': user_form})

    # Otherwise we diplay the form for them to fill out and post to us
    else:
        return render(request, 'register.html', {'user_form': UserForm()}) 
       

def manual_logout(request):
    return render(request, 'manual_logout.html')    

def authorize(request):
    # Must not be logged in here. After authorizing, users are prompted to log
    # in, and if a user is already logged in then there are multiple users
    # logged in at once and that's no good
    if request.user.is_authenticated():
        return redirect('manual_logout')
    
    params = {'redirect_uri': redirect_uri,
              'response_type': 'code',
              'client_id': client_id,}
              # TODO isn't this how scope is supposed to work?
              #'scope': 'patients'}
    return redirect('https://drchrono.com/o/authorize/?' + urlencode(params))

@login_required
def authorization_redirect(request):
    # Check if the user denied permissions in authorization
    if 'error' in request.GET:
        return redirect('permissions_error')
    elif 'code' in request.GET:
        # We have a valid code, use it to get our access token, refresh token
        # and authentication timeout
        response = requests.post('https://drchrono.com/o/token/', data={
                                 'code': request.GET['code'],
                                 'grant_type': 'authorization_code',
                                 'redirect_uri': redirect_uri,
                                 'client_id': client_id,
                                 'client_secret': client_secret})
        response.raise_for_status()
        data = response.json()
        # Fetch drchrono username
        response = requests.get('https://drchrono.com/api/users/current', headers={
                                'Authorization': 'Bearer %s' % data['access_token'],
                                 })
        response.raise_for_status()
        username = response.json()['username']

        doctor = request.user.doctor
        doctor.access_token = data['access_token']
        doctor.refresh_token = data['refresh_token']
        doctor.expires_timestamp = datetime.datetime.now(pytz.utc) \
                                    + datetime.timedelta(seconds=data['expires_in'])  
        doctor.username = username
        doctor.save()
        return redirect('home')
    else:
        return render(request, 'bad_authorization.html')


def permissions_error(request):
    return render(request, 'permissions_error.html')
