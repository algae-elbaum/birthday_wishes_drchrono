from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from urllib import urlencode
import requests, datetime, pytz
from globs import redirect_uri, client_id, client_secret
from models import Patient, Doctor
from forms import UserForm

@login_required
def home(request):
    # Check if we have drchrono authorization for the user
    doctor = request.user.doctor
    if not doctor.access_token: 
        # Check if the user denied permissions in authorization
        if 'error' in request.GET:
            return redirect('permissions_error')
        # Check if we need to get an authorization code
        if 'code' not in request.GET:
            return redirect('authorize')
        else:
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

            doctor.access_token = data['access_token']
            doctor.refresh_token = data['refresh_token']
            doctor.expires_timestamp = datetime.datetime.now(pytz.utc) \
                                        + datetime.timedelta(seconds=data['expires_in'])  
            doctor.save()
     
    # Now user is logged in and has granted authorization
    # Get list of all the user's patients and send out the response 
    patient_list = doctor.get_local_patient_list()
    context = {'patient_list': patient_list}
    return render(request, 'birthday_wishes.html', context)

@login_required
def patient_page(request, uid):
    doctor = request.user.doctor
    # If it's a POST, set the patient's fields according to the form
    if request.method == 'POST':
        activated = request.POST.get('checkbox', False)
        msg = request.POST['msg']
        subj = request.POST['subj']
        doctor.patient_set.filter(uid=uid).update(msg_active = activated, message = msg, subject = subj)
        return redirect(home)
    # Otherwise send the user to the form
    else:
        patient = doctor.patient_set.get(uid=uid)
        return render(request, 'patient_page.html', {'patient': patient})

@login_required
def refresh_patients(request):
    # If by some hackery the user is logged in but still got to this page 
    # without authenticating:
    if not request.user.doctor.access_token:
        redirect('home')
    request.user.doctor.update_patient_list()
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
            
            #TODO Automatically log in new user
            
        # Registration done, let's get out of here.
        # (note: I'm not actually sure whether it'd be more appropriate to
        # have a new view for the result and redirect to it. That sort of thing
        # seems common, but this seems simpler)
        return render(request, 'registration_report.html', {'success': success})

    # Otherwise we diplay the form for them to fill out and post to us
    else:
        return render(request, 'register.html', {'user_form': UserForm()}) 
       

def manual_logout(request):
    return render(request, 'manual_logout.html')    

@login_required
def authorize(request):
    #TODO get scopes right
    scopes = 'patients' 
    params = {'redirect_uri': redirect_uri,
              'response_type': 'code',
              'client_id': client_id} 
    return redirect('https://drchrono.com/o/authorize/?' + urlencode(params)) 

def permissions_error(request):
    return render(request, 'permissions_error.html')
