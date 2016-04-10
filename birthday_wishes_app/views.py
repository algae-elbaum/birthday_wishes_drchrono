from django.shortcuts import render, redirect
from django.http import HttpResponse
from urllib import urlencode
import requests, datetime, pytz
from globs import redirect_uri, client_id, client_secret, scopes
from models import Patient

def home(request):
    #TODO Account login
    if False: # if not logged in
        return redirect('login')
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
    Patient.check_for_new_patients()
    patient_list = Patient.objects.order_by('-birthday')
    context = {'patient_list': patient_list}
    return render(request, 'birthday_wishes.html', context)


def login(request):
    return render(request, 'login.html')

def authorize(request):
    params = {'redirect_uri': redirect_uri,
              'response_type': 'code',
              'client_id': client_id,
              'scope': scopes} 
    return redirect('https://drchrono.com/o/authorize/?' + urlencode(params)) 

def permissions_error(request):
    return render(request, 'permissions_error.html')
