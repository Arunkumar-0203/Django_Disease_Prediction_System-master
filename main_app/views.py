from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import date

from django.contrib import messages
from django.contrib.auth.models import User , auth
# from sqlalchemy.testing.suite.test_reflection import users

from .models import patient , doctor , diseaseinfo , consultation ,rating_review, Hospitals, UserType
from chats.models import Chat,Feedback

# Create your views here.


#loading model
import joblib as jb
model = jb.load('trained_model')




def home(request):

  if request.method == 'GET':
      if request.user.is_authenticated:
            # doctors = doctor.objects.all()
            return render(request,'index.html')
      else :
        return render(request,'index.html')


def gallery(request):
    if request.method == 'GET':
       return render(request,'gallery.html')
   

       


def admin_ui(request):

    if request.method == 'GET':

      if request.user.is_authenticated:

        auser = request.user
        Feedbackobj = Feedback.objects.all()

        return render(request,'admin/admin_ui/admin_ui.html' , {"auser":auser,"Feedback":Feedbackobj})

      else :
        return redirect('home')



    if request.method == 'POST':

       return render(request,'patient/patient_ui/profile.html')





def patient_ui(request):

    if request.method == 'GET':

      if request.user.is_authenticated:

        patientusername = request.session['patientusername']
        puser = User.objects.get(username=patientusername)

        return render(request,'patient/patient_ui/profile.html' , {"puser":puser})

      else :
        return redirect('home')



    if request.method == 'POST':

       return render(request,'patient/patient_ui/profile.html')

       


def pviewprofile(request, patientusername):

    if request.method == 'GET':

          puser = User.objects.get(username=patientusername)

          return render(request,'patient/view_profile/view_profile.html', {"puser":puser})



def patientviewprofile(request, patientusername):

    if request.method == 'GET':

          puser = User.objects.get(username=patientusername)

          return render(request,'doctor/patient_profile.html', {"puser":puser})




def checkdisease(request):

  diseaselist=['Fungal infection','Allergy','GERD','Chronic cholestasis','Drug Reaction','Peptic ulcer diseae','AIDS','Diabetes ',
  'Gastroenteritis','Bronchial Asthma','Hypertension ','Migraine','Cervical spondylosis','Paralysis (brain hemorrhage)',
  'Jaundice','Malaria','Chicken pox','Dengue','Typhoid','hepatitis A', 'Hepatitis B', 'Hepatitis C', 'Hepatitis D',
  'Hepatitis E', 'Alcoholic hepatitis','Tuberculosis', 'Common Cold', 'Pneumonia', 'Dimorphic hemmorhoids(piles)',
  'Heart attack', 'Varicose veins','Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia', 'Osteoarthristis',
  'Arthritis', '(vertigo) Paroymsal  Positional Vertigo','Acne', 'Urinary tract infection', 'Psoriasis', 'Impetigo']


  symptomslist=['itching','skin_rash','nodal_skin_eruptions','continuous_sneezing','shivering','chills','joint_pain',
  'stomach_pain','acidity','ulcers_on_tongue','muscle_wasting','vomiting','burning_micturition','spotting_ urination',
  'fatigue','weight_gain','anxiety','cold_hands_and_feets','mood_swings','weight_loss','restlessness','lethargy',
  'patches_in_throat','irregular_sugar_level','cough','high_fever','sunken_eyes','breathlessness','sweating',
  'dehydration','indigestion','headache','yellowish_skin','dark_urine','nausea','loss_of_appetite','pain_behind_the_eyes',
  'back_pain','constipation','abdominal_pain','diarrhoea','mild_fever','yellow_urine',
  'yellowing_of_eyes','acute_liver_failure','fluid_overload','swelling_of_stomach',
  'swelled_lymph_nodes','malaise','blurred_and_distorted_vision','phlegm','throat_irritation',
  'redness_of_eyes','sinus_pressure','runny_nose','congestion','chest_pain','weakness_in_limbs',
  'fast_heart_rate','pain_during_bowel_movements','pain_in_anal_region','bloody_stool',
  'irritation_in_anus','neck_pain','dizziness','cramps','bruising','obesity','swollen_legs',
  'swollen_blood_vessels','puffy_face_and_eyes','enlarged_thyroid','brittle_nails',
  'swollen_extremeties','excessive_hunger','extra_marital_contacts','drying_and_tingling_lips',
  'slurred_speech','knee_pain','hip_joint_pain','muscle_weakness','stiff_neck','swelling_joints',
  'movement_stiffness','spinning_movements','loss_of_balance','unsteadiness',
  'weakness_of_one_body_side','loss_of_smell','bladder_discomfort','foul_smell_of urine',
  'continuous_feel_of_urine','passage_of_gases','internal_itching','toxic_look_(typhos)',
  'depression','irritability','muscle_pain','altered_sensorium','red_spots_over_body','belly_pain',
  'abnormal_menstruation','dischromic _patches','watering_from_eyes','increased_appetite','polyuria','family_history','mucoid_sputum',
  'rusty_sputum','lack_of_concentration','visual_disturbances','receiving_blood_transfusion',
  'receiving_unsterile_injections','coma','stomach_bleeding','distention_of_abdomen',
  'history_of_alcohol_consumption','fluid_overload','blood_in_sputum','prominent_veins_on_calf',
  'palpitations','painful_walking','pus_filled_pimples','blackheads','scurring','skin_peeling',
  'silver_like_dusting','small_dents_in_nails','inflammatory_nails','blister','red_sore_around_nose',
  'yellow_crust_ooze']

  alphabaticsymptomslist = sorted(symptomslist)

  


  if request.method == 'GET':
    
     return render(request,'patient/checkdisease/checkdisease.html', {"list2":alphabaticsymptomslist})




  elif request.method == 'POST':
       
      ## access you data by playing around with the request.POST object
      
      inputno = int(request.POST["noofsym"])
      print(inputno)
      if (inputno == 0 ) :
          return JsonResponse({'predicteddisease': "none",'confidencescore': 0 })
  
      else :

        psymptoms = []
        psymptoms = request.POST.getlist("symptoms[]")
       
        print(psymptoms)

      
        """      #main code start from here...
        """
      

      
        testingsymptoms = []
        #append zero in all coloumn fields...
        for x in range(0, len(symptomslist)):
          testingsymptoms.append(0)


        #update 1 where symptoms gets matched...
        for k in range(0, len(symptomslist)):

          for z in psymptoms:
              if (z == symptomslist[k]):
                  testingsymptoms[k] = 1


        inputtest = [testingsymptoms]

        print(inputtest)
      

        predicted = model.predict(inputtest)
        print("predicted disease is : ")
        print(predicted)

        y_pred_2 = model.predict_proba(inputtest)
        confidencescore=y_pred_2.max() * 100
        print(" confidence score of : = {0} ".format(confidencescore))

        confidencescore = format(confidencescore, '.0f')
        predicted_disease = predicted[0]

        

        #consult_doctor codes----------

        #   doctor_specialization = ["Rheumatologist","Cardiologist","ENT specialist","Orthopedist","Neurologist",
        #                             "Allergist/Immunologist","Urologist","Dermatologist","Gastroenterologist"]
        

        Rheumatologist = [  'Osteoarthristis','Arthritis']
       
        Cardiologist = [ 'Heart attack','Bronchial Asthma','Hypertension ']
       
        ENT_specialist = ['(vertigo) Paroymsal  Positional Vertigo','Hypothyroidism' ]

        Orthopedist = []

        Neurologist = ['Varicose veins','Paralysis (brain hemorrhage)','Migraine','Cervical spondylosis']

        Allergist_Immunologist = ['Allergy','Pneumonia',
        'AIDS','Common Cold','Tuberculosis','Malaria','Dengue','Typhoid']

        Urologist = [ 'Urinary tract infection',
         'Dimorphic hemmorhoids(piles)']

        Dermatologist = [  'Acne','Chicken pox','Fungal infection','Psoriasis','Impetigo']

        Gastroenterologist = ['Peptic ulcer diseae', 'GERD','Chronic cholestasis','Drug Reaction','Gastroenteritis','Hepatitis E',
        'Alcoholic hepatitis','Jaundice','hepatitis A',
         'Hepatitis B', 'Hepatitis C', 'Hepatitis D','Diabetes ','Hypoglycemia']
         
        if predicted_disease in Rheumatologist :
           consultdoctor = "Rheumatologist"
           
        if predicted_disease in Cardiologist :
           consultdoctor = "Cardiologist"
           

        elif predicted_disease in ENT_specialist :
           consultdoctor = "ENT specialist"
     
        elif predicted_disease in Orthopedist :
           consultdoctor = "Orthopedist"
     
        elif predicted_disease in Neurologist :
           consultdoctor = "Neurologist"
     
        elif predicted_disease in Allergist_Immunologist :
           consultdoctor = "Allergist/Immunologist"
     
        elif predicted_disease in Urologist :
           consultdoctor = "Urologist"
     
        elif predicted_disease in Dermatologist :
           consultdoctor = "Dermatologist"
     
        elif predicted_disease in Gastroenterologist :
           consultdoctor = "Gastroenterologist"
     
        else :
           consultdoctor = "other"


        request.session['doctortype'] = consultdoctor 

        patientusername = request.session['patientusername']
        puser = User.objects.get(username=patientusername)
     

        #saving to database.....................

        patient = puser.patient
        diseasename = predicted_disease
        no_of_symp = inputno
        symptomsname = psymptoms
        confidence = confidencescore

        diseaseinfo_new = diseaseinfo(patient=patient,diseasename=diseasename,no_of_symp=no_of_symp,symptomsname=symptomsname,confidence=confidence,consultdoctor=consultdoctor)
        diseaseinfo_new.save()
        

        request.session['diseaseinfo_id'] = diseaseinfo_new.id

        print("disease record saved sucessfully.............................")

        return JsonResponse({'predicteddisease': predicted_disease ,'confidencescore':confidencescore , "consultdoctor": consultdoctor})
   


   
    



   





def pconsultation_history(request):

    if request.method == 'GET':

      patientusername = request.session['patientusername']
      puser = User.objects.get(username=patientusername)
      patient_obj = puser.patient
        
      consultationnew = consultation.objects.filter(patient = patient_obj)
      
    
      return render(request,'patient/consultation_history/consultation_history.html',{"consultation":consultationnew})


def dconsultation_history(request):

    if request.method == 'GET':

      doctorusername = request.session['doctorusername']
      duser = User.objects.get(username=doctorusername)
      doctor_obj = duser.doctor
        
      consultationnew = consultation.objects.filter(doctor = doctor_obj)
      
    
      return render(request,'doctor/consultation_history/consultation_history.html',{"consultation":consultationnew})



def doctor_ui(request):

    if request.method == 'GET':

      doctorid = request.session['doctorusername']
      duser = User.objects.get(username=doctorid)

    
      return render(request,'doctor/doctor_ui/profile.html',{"duser":duser})



      


def dviewprofile(request, doctorusername):

    if request.method == 'GET':

         
         duser = User.objects.get(username=doctorusername)
         r = rating_review.objects.filter(doctor=duser.doctor)
       
         return render(request,'doctor/view_profile/view_profile.html', {"duser":duser, "rate":r} )








       
def  consult_a_doctor(request):


    if request.method == 'GET':

        
        doctortype = request.session['doctortype']
        print(doctortype)
        dobj = doctor.objects.all()
        #dobj = doctor.objects.filter(specialization=doctortype)


        return render(request,'patient/consult_a_doctor/consult_a_doctor.html',{"dobj":dobj})

   


def  make_consultation(request, doctorusername):

    if request.method == 'POST':
       

        patientusername = request.session['patientusername']
        puser = User.objects.get(username=patientusername)
        patient_obj = puser.patient
        
        
        #doctorusername = request.session['doctorusername']
        duser = User.objects.get(username=doctorusername)
        doctor_obj = duser.doctor
        request.session['doctorusername'] = doctorusername


        diseaseinfo_id = request.session['diseaseinfo_id']
        diseaseinfo_obj = diseaseinfo.objects.get(id=diseaseinfo_id)

        consultation_date = date.today()
        status = "active"
        
        consultation_new = consultation( patient=patient_obj, doctor=doctor_obj, diseaseinfo=diseaseinfo_obj, consultation_date=consultation_date,status=status)
        consultation_new.save()

        request.session['consultation_id'] = consultation_new.id

        print("consultation record is saved sucessfully.............................")

         
        return redirect('consultationview',consultation_new.id)



def  consultationview(request,consultation_id):
   
    if request.method == 'GET':

   
      request.session['consultation_id'] = consultation_id
      consultation_obj = consultation.objects.get(id=consultation_id)

      return render(request,'consultation/consultation.html', {"consultation":consultation_obj })

   #  if request.method == 'POST':
   #    return render(request,'consultation/consultation.html' )





def rate_review(request,consultation_id):
   if request.method == "POST":
         
         consultation_obj = consultation.objects.get(id=consultation_id)
         patient = consultation_obj.patient
         doctor1 = consultation_obj.doctor
         rating = request.POST.get('rating')
         review = request.POST.get('review')

         rating_obj = rating_review(patient=patient,doctor=doctor1,rating=rating,review=review)
         rating_obj.save()

         rate = int(rating_obj.rating_is)
         doctor.objects.filter(pk=doctor1).update(rating=rate)
         

         return redirect('consultationview',consultation_id)





def close_consultation(request,consultation_id):
   if request.method == "POST":
         
         consultation.objects.filter(pk=consultation_id).update(status="closed")
         
         return redirect('home')






#-----------------------------chatting system ---------------------------------------------------


def post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)

        consultation_id = request.session['consultation_id'] 
        consultation_obj = consultation.objects.get(id=consultation_id)

        c = Chat(consultation_id=consultation_obj,sender=request.user, message=msg)

        #msg = c.user.username+": "+msg

        if msg != '':            
            c.save()
            print("msg saved"+ msg )
            return JsonResponse({ 'msg': msg })
    else:
        return HttpResponse('Request must be POST.')



def chat_messages(request):
   if request.method == "GET":

         consultation_id = request.session['consultation_id'] 

         c = Chat.objects.filter(consultation_id=consultation_id)
         return render(request, 'consultation/chat_body.html', {'chat': c})


#-----------------------------chatting system ---------------------------------------------------
#---------------------------------------------------admin---------------------------------------------------------------------
def view_users(request):
    if request.method == 'GET':
        users=patient.objects.filter(status='notapprove')
        print(users)
        return render(request,'admin/admin_ui/view_users.html',{'users':users})

def approve_users(request,id):
    if request.method == 'GET':
      try:
        approve=patient.objects.get(status='notapprove',user_id=id)
        user=User.objects.get(id=id)
        user.last_name=1
        user.save()
        approve.status='approve'
        approve.save()
        messages.info(request,'user approved')
        return redirect('view_users')
      except:
        messages.info(request,'user approved')
        return redirect('approve_users')
    else:
        return render(request,'admin/admin_ui/view_users.html')

def remove_users(request,id):
    if request.method == 'GET':
      try:
        approve=patient.objects.get(status='notapprove',user_id=id)
        user=User.objects.get(id=id)
        user.last_name=0
        user.save()
        approve.status='reject'
        approve.save()
        messages.info(request,'user rejected')
        return redirect('view_users')
      except:
        messages.info(request,'user approved')
        return redirect('approve_users')
    else:
        return render(request,'admin/admin_ui/view_users.html')

def approved_users(request):
    if request.method == 'GET':
        users=patient.objects.filter(status='approve')
        print(users)
        return render(request,'admin/admin_ui/approved_users.html',{'users':users})

def signup_doctor(request):

    if request.method == 'GET':
        hospitals=Hospitals.objects.filter(status='approved')

        return render(request,'doctor/signup_Form/signup.html',{'hospitals':hospitals})


    if request.method == 'POST':

      if request.POST['username'] and request.POST['email'] and  request.POST['name'] and request.POST['dob'] and request.POST['gender'] and request.POST['address']and request.POST['mobile'] and request.POST['password']and request.POST['password1']  and  request.POST['registration_no'] and  request.POST['year_of_registration'] and  request.POST['qualification'] and  request.POST['State_Medical_Council'] and  request.POST['specialization'] :

          username =  request.POST['username']
          email =  request.POST['email']
          Hospita=request.POST['hospital_id']
          name =  request.POST['name']
          dob =  request.POST['dob']
          gender =  request.POST['gender']
          address =  request.POST['address']
          mobile_no = request.POST['mobile']
          registration_no =  request.POST['registration_no']
          year_of_registration =  request.POST['year_of_registration']
          qualification =  request.POST['qualification']
          State_Medical_Council =  request.POST['State_Medical_Council']
          specialization =  request.POST['specialization']

          password =  request.POST.get('password')
          password1 =  request.POST.get('password1')

          if password == password1:
              if User.objects.filter(username = username).exists():
                messages.info(request,'username already taken')
                return redirect('signup_doctor')

              elif User.objects.filter(email = email).exists():
                messages.info(request,'email already taken')
                return redirect('signup_doctor')

              else :
                user = User.objects.create_user(username=username,password=password,email=email,last_name='1')
                user.save()

                doctornew = doctor( user=user,hospital_id=Hospita, name=name, dob=dob, gender=gender, address=address, mobile_no=mobile_no, registration_no=registration_no, year_of_registration=year_of_registration, qualification=qualification, State_Medical_Council=State_Medical_Council, specialization=specialization )
                doctornew.save()
                usertype=UserType()
                usertype.user=user
                usertype.type='doctor'
                usertype.save()
                messages.info(request,'user created sucessfully')
                print("doctorcreated")

              return redirect('signup_doctor')

          else:
            messages.info(request,'password not matching, please try again')
            return redirect('signup_doctor')

      else :
        messages.info(request,'Please make sure all required fields are filled out correctly')
        return redirect('signup_doctor')

def hospital_add(request):
    if request.method=='POST':
        name=request.POST['name']
        phone=request.POST['phone']
        Place=request.POST['place']
        image = request.FILES['Image']
        f=FileSystemStorage()
        IMAGE=f.save(image.name,image)
        address=request.POST['address']
        Password=request.POST['password']
        try:
            user = User.objects._create_user(username=name,password=Password,first_name=name,email='',is_staff='0',last_name='1')
            user.save()
            register = Hospitals()
            register.user = user
            register.place=Place
            register.name=name
            register.status='approved'
            register.phone=phone
            register.Address=address
            register.password=Password
            register.image=IMAGE
            register.save()
            usertype = UserType()
            usertype.user = user
            usertype.type = "hospital"
            usertype.save()
            messages.info(request,'add sucessfully')
            return redirect('hospital_add')
        except:
            messages.info(request,'invalid data')
            return redirect('hospital_add')

    return render(request,'admin/admin_ui/hospital_registration.html')

def view_hospitals(request):
    if request.method == 'GET':
        HOSPITALS=Hospitals.objects.filter(status='approved')
        return render(request,'admin/admin_ui/view_hospital.html',{'hospitals':HOSPITALS})


def admin_gallery(request):
    if request.method == 'GET':
       return render(request,'admin/admin_ui/gallery.html')

def remove_hospitals(request,id):
    if request.method == 'GET':
      try:
        HOSPITALS=Hospitals.objects.get(status='approved',id=id)
        HOSPITALS.status='reject'
        HOSPITALS.save()
        messages.info(request,'hospital removed')
        return redirect('view_hospitals')
      except:
        messages.info(request,'hospital removed')
        return redirect('view_hospitals')
    else:
        return render(request,'admin/admin_ui/gallery.html')


def view_doctors(request):
    if request.method=='GET':
        Doctor=doctor.objects.filter(status=1)
        return render(request,'admin/admin_ui/view_doctors.html',{'DOCTOR':Doctor})

def contact(request):
    if request.method == 'GET':
       return render(request,'contact.html')

def doctorhospital(request):
    if request.method=='GET':
         HOSPITALS=Hospitals.objects.filter(status='approved')
         return render(request,'doctor/view_hospital.html',{'hospitals':HOSPITALS})

def view_feedback(request):
    if request.method=='GET':
        feed=Feedback.objects.all()
        return render(request,'admin/admin_ui/view_feedback.html',{'feedback':feed})

def patientview_hospital(request):
    if request.method=='GET':
         HOSPITALS=Hospitals.objects.filter(status='approved')
         return render(request,'patient/patientview_hospital.html',{'hospitals':HOSPITALS})


def patientview_doctor(request):
    if request.method=='GET':
        Doctor=doctor.objects.filter(status=1)
        return render(request,'patient/patientview_doctor.html',{'DOCTOR':Doctor})