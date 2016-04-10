from __future__ import unicode_literals

import requests, datetime, pytz
from django.db import models
from django.contrib.auth.models import User
from globs import max_msg_len, client_id, client_secret


# A user of this app. Doctors are bijected with Users in django's auth system
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=30, default='')
    refresh_token = models.CharField(max_length=30, default='')
    expires_timestamp = models.DateTimeField(default=datetime.datetime.now(pytz.utc))

    def __str__(self):
        return self.user.username  
    
    def get_complete_patient_list(self):
        if self.expires_timestamp < datetime.datetime.now(pytz.utc):
            self.refresh_authentication()
        # I'll trust the list of patients from the API not to have repeats
        headers={'Authorization': 'Bearer %s' % self.access_token}
        patients = []
        patients_url = 'https://drchrono.com/api/patients'
        #TODO figure out what's wrong with permissions here
        while patients_url:
            data = requests.get(patients_url, headers=headers).json()
            patients.extend(data['results'])
            patients_url = data['next'] # A JSON null on the last page
        #TODO Check against repeats/updates to patient data. Then add the
        # patients to this doctors set of patients
        print patients

    def refresh_authentication(self):
        response = requests.post('https://drchrono.com/o/token/', data={
                                 'refresh_token': self.refresh_token,
                                 'grant_type': 'refresh_token',
                                 'client_id': client_id,
                                 'client_secret': client_secret,
                                })
        response.raise_for_status()
        data = response.json()

        self.access_token = data['access_token']
        self.refresh_token = data['refresh_token']
        self.expires_timestamp = datetime.datetime.now(pytz.utc) \
                                    + datetime.timedelta(seconds=data['expires_in'])  
        doctor.save()


# Represents a single patient
# A single person may be a patient to multiple doctors, in which case for each
# doctor there will be a distinct Patient instance for that patient. This is to
# take advantage of a many-to-one structure and so that the mapping from  patients 
# to birthday messages is simple. If memory is an issue, it could be arranged for
# there to only be one Patient per real live patient.
# Patients are what will be listed out on the frontend and what will be modified
# by changes on the frontend
class Patient(models.Model):
    # The longest name in the world is something like 225 characters. Let's 
    # allow some leeway
    name = models.CharField(max_length = 256, default='')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, default=None)
    # ssn acts as a uid
    ssn = models.IntegerField(default=-1)
    birthday = models.DateField()
    birthday_msg = models.CharField(max_length = max_msg_len, default='')
    msg_active = models.BooleanField()
   
    def __str__(self): 
        return self.name

    def set_msg(self, new_msg):
        if new_msg > max_msg_len:
            return False
        else:
            self.birthday_msg = new_msg
            return True

   
