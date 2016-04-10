from __future__ import unicode_literals

import requests
from django.db import models
from globs import max_msg_len

# Represents a single patient
# These are what will be listed out on the frontend and what will be modified
# by changes on the frontend
class Patient(models.Model):
    # The longest name in the world is something like 225 characters. Let's 
    # allow some leeway
    name = models.CharField(max_length = 256, default='')
    # ssn acts as a uid
    ssn = models.IntegerField
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

    @staticmethod
    def check_for_new_patients():
        # I'll trust the list of patients from the API not to have repeats
        #TODO get the auth info of the user
#        r = requests.get('https://drchrono.com/api/patients', auth=auth)
        pass
