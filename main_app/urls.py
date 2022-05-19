from django.urls import path , re_path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path('admin_ui', views.admin_ui , name='admin_ui'),
    path('gallery',views.gallery,name='gallerhy'),
    path('contact',views.contact, name='contact'),
    path('patient_ui', views.patient_ui , name='patient_ui'),
    path('checkdisease', views.checkdisease, name="checkdisease"),
    path('pviewprofile/<str:patientusername>', views.pviewprofile , name='pviewprofile'),

    path('pconsultation_history', views.pconsultation_history , name='pconsultation_history'),
    path('consult_a_doctor', views.consult_a_doctor , name='consult_a_doctor'),
    path('make_consultation/<str:doctorusername>', views.make_consultation , name='make_consultation'),
    path('rate_review/<int:consultation_id>', views.rate_review , name='rate_review'),


    path('dconsultation_history', views.dconsultation_history , name='dconsultation_history'),
    path('dviewprofile/<str:doctorusername>', views.dviewprofile , name='dviewprofile'),
    path('doctor_ui', views.doctor_ui , name='doctor_ui'),
    
    
    
    path('consultationview/<int:consultation_id>', views.consultationview , name='consultationview'),
    path('close_consultation/<int:consultation_id>', views.close_consultation , name='close_consultation'),

    
    path('post', views.post, name='post'),
    path('chat_messages', views.chat_messages, name='chat_messages'),

    #---------------------------------admin---------------------------------------
    path('view_users',views.view_users, name='view_users'),
    path('approve_users/<int:id>',views.approve_users, name='approve_users'),
    path('remove_users/<int:id>',views.remove_users, name='remove_users'),
    path('approved_users', views.approved_users, name='approved_users'),
    path('signup_doctor', views.signup_doctor , name="signup_doctor"),
    path('hospital_add',views.hospital_add, name='hospital_add'),
    path('view_hospitals',views.view_hospitals, name='view_hospitals'),
    path('admin_gallery', views.admin_gallery, name='admin_gallery'),
    path('remove_hospitals/<int:id>', views.remove_hospitals, name='remove_hospitals'),
    path('view_doctors', views.view_doctors,name='view_doctors'),
    path('patientviewprofile',views.patientviewprofile, name='patientviewprofile'),
    path('doctorhospital',views.doctorhospital,name='doctorhospital'),
    path('view_feedback',views.view_feedback,name='view_feedback'),
    path('patientview_doctor', views.patientview_doctor,name='patientview_doctor'),
    path('patientview_hospital', views.patientview_hospital,name='patientview_hospital'),

    path('report_view',views.reportr,name='report_view'),
    path('view_reportr',views.view_reportr,name='view_reportr')




]  
