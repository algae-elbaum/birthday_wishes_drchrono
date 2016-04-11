from __future__ import unicode_literals

import requests, datetime, pytz
from django.db import models
from django.contrib.auth.models import User
from globs import client_id, client_secret, msg_max, subj_max


# A user of this app. Doctors are bijected with Users in django's auth system
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, default='')
    access_token = models.CharField(max_length=30, default='')
    refresh_token = models.CharField(max_length=30, default='')
    expires_timestamp = models.DateTimeField(default=datetime.datetime.now(pytz.utc))

    def __str__(self):
        return self.user.username  
   
    def get_local_patient_list(self):
        return self.patient_set.order_by('name').all()

    # Update the set of patients associated with this doctor
    def update_patient_list(self):
        if self.expires_timestamp < datetime.datetime.now(pytz.utc):
            self.refresh_authentication()
        headers={'Authorization': 'Bearer %s' % self.access_token}
        patients = []
        patients_url = 'https://drchrono.com/api/patients'
        while patients_url:
            response = requests.get(patients_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            patients.extend(data['results'])
            patients_url = data['next'] # A JSON null on the last page
        for p in patients:
            # If the patient doesn't already exist, add it. If it does exist
            # make sure the patient info is up to date
            # But only if they have a birthday and email
            if p['date_of_birth'] and p['email']:
                names = [p['first_name'], p['middle_name'], p['last_name']]
                name = ' '.join(filter(None, names))
                if not self.patient_set.filter(uid = p['id']):
                    add_or_update_patient = self.patient_set.create
                else:
                    add_or_update_patient = self.patient_set.filter(uid=p['id']).update
                # There's something viscerally satisfying about passing
                # functions around like this
                add_or_update_patient(name=name,
                                      email=p['email'],
                                      doctor = self,
                                      uid = p['id'],
                                      birthday = p['date_of_birth'])


    # If the access token is expired, this refreshes authentication
    # I'm assuming that the access token does not need to be active
    # for this to work. If it does, I'll have to schedule a reauthentication
    # job
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
    email = models.CharField(max_length = 256, default='')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, default=None)
    uid = models.IntegerField(default=-1)
    birthday = models.DateField()
    subject = models.CharField(max_length = subj_max, default='')
    message = models.TextField(max_length = msg_max, default='')
    message_time = models.IntegerField(default=12)
    msg_active = models.BooleanField(default=False)
   
    def __str__(self): 
        return self.name

