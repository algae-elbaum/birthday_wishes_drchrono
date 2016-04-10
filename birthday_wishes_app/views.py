from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from urllib import urlencode
import requests, datetime, pytz
from globs import redirect_uri, client_id, client_secret, scopes
from models import Patient, Doctor
from forms import UserForm

@login_required
def home(request):
    #TODO check logged in account for authorization and get authorization if needed
    if False: # if not authorized
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

            #TODO store these in the user's account
            access_token = data['access_token']
            refresh_token = data['refresh_token']
            expires_timestamp = datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=data['expires_in'])  

    
    # Now user is logged in and has granted authorization
    # Get list of all Patients and send out the response 
    #TODO get patients list from user
    patient_list = []
#    user.check_for_new_patients()
#    patient_list = Patient.objects.order_by('-birthday')
    context = {'patient_list': patient_list}
    return render(request, 'birthday_wishes.html', context)


def register(request):
    #TODO if there's a user logged in, redirect to a logout page
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
            # Initialize non nullable expiration time to have already passed
            doctor.expires_timestamp = datetime.datetime.now()
            doctor.save()
            #TODO automatically log in new user
            success = True
            
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
    params = {'redirect_uri': redirect_uri,
              'response_type': 'code',
              'client_id': client_id,
              'scope': scopes} 
    return redirect('https://drchrono.com/o/authorize/?' + urlencode(params)) 

def permissions_error(request):
    return render(request, 'permissions_error.html')
