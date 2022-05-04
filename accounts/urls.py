from django.urls import path
from . import views

urlpatterns = [


    path('sign_in_admin', views.sign_in_admin , name='sign_in_admin'),
    path('gallery',views.gallery,name='gallerhy'),
    path('signup_patient', views.signup_patient, name="signup_patient"),
    path('sign_in_patient', views.sign_in_patient , name='sign_in_patient'),
    path('savepdata/<str:patientusername>', views.savepdata , name='savepdata'),
    path('contact',views.contact, name='contact'),
    


    path('sign_in_doctor', views.sign_in_doctor , name='sign_in_doctor'),
    path('saveddata/<str:doctorusername>', views.saveddata , name='saveddata'),

    path('logout', views.logout , name='logout'),
]