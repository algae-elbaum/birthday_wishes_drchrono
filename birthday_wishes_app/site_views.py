from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from globs import msg_max, subj_max

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
        return redirect('permissions_error')

def about(request):
    return render(request, 'about.html')

