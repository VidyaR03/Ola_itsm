from dataclasses import fields
from pyexpat import model
from telnetlib import STATUS
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
# from .models import Location, person, team,  Document, Software, Application_solution, New_organization, Delivery_model,\
#      Business_process, Newdb_server, Database_schema, New_middleware, Middleware_instance,Network_device,Other_software,\
#          Web_application, Web_server, Network_device, Server, Pc_software, User_request, New_change, Customer_contract, Providercontract,\
#             Servicefamilies, Service, Service_subcategory, Sla, Slt, Servicedelivery, Synchro_data_source, Oauth_google,\
#                  Oauth_mazure, Ldapuser, Externaluser, Itsmuser, Slacknoti, Micronoti, Webhook, Googlechat,\
#                     Rocketchat, Itsmwebhook
CHOICES=[
    ('active','Active'),
    ('Inactive','Inactive'),
]
TypeDoc=[
    ('draft','Draft'),
    ('obsolete','Obsolete'),
    ('published','Published'),
]
TypeChoices=[
    ('db server','DB server'),
    ('middleware','Middleware'),
    ('other software','Other Software'),
    ('pc software','PC Software'),
    ('web server','Web Server'),
]
class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']

class TeamForm(ModelForm):
    status=forms.CharField(label='Status', widget=forms.Select(choices=CHOICES))
    class Meta:
        model=cl_Team
        fields='__all__'

class PersonForm(ModelForm):
    class Meta:
        model=cl_Person
        fields='__all__'

class LocationForm(ModelForm):
    status=forms.CharField(label='Status', widget=forms.Select(choices=CHOICES))
    class Meta:
        model=cl_Location
        fields='__all__'

class DocumentForm(ModelForm):
    type=forms.CharField(label='Status', widget=forms.Select(choices=TypeDoc))
    class Meta:
        model=cl_Document
        fields='__all__'

class SoftwareForm(ModelForm):
    type=forms.CharField(label='Type', widget=forms.Select(choices=TypeChoices))
    class Meta:
        model=cl_Software
        fields='__all__'

class ApplicationsolutionForm(ModelForm):
    class Meta:
        model=cl_Application_solution
        fields='__all__'

class TassignForm(ModelForm):
    class Meta:
        model=tassign
        fields='__all__'

class NeworganizationForm(ModelForm):
    class Meta:
        model=cl_New_organization
        fields='__all__'

class DeliverymodelForm(ModelForm):
    class Meta:
        model=cl_Delivery_model
        fields='__all__'

class BusinessprocessForm(ModelForm):
    class Meta:
        model=cl_Business_process
        fields='__all__'

class NewdbserverForm(ModelForm):
    class Meta:
        model=cl_Newdb_server
        fields='__all__'

class DatabaseschemaForm(ModelForm):
    class Meta:
        model=cl_Database_schema
        fields='__all__'

class NewmiddlewareForm(ModelForm):
    class Meta:
        model=cl_Database_schema
        fields='__all__'

class MiddlewareinstanceForm(ModelForm):
    class Meta:
        model=cl_New_middleware
        fields='__all__'

class NetworkForm(ModelForm):
    class Meta:
        model=cl_Middleware_instance
        fields='__all__'

class OthersoftwareForm(ModelForm):
    class Meta:
        model=cl_Network_device
        fields='__all__'

class WebapplicationForm(ModelForm):
    class Meta:
        model=cl_Other_software
        fields='__all__'

class WebserverForm(ModelForm):
    class Meta:
        model=cl_Web_application
        fields='__all__'

class NetworkdeviceForm(ModelForm):
    class Meta:
        model=cl_Web_server
        fields='__all__'

class ServerForm(ModelForm):
    class Meta:
        model=cl_Server
        fields='__all__'

class PcsoftwareForm(ModelForm):
    class Meta:
        model=cl_Pc_software
        fields='__all__'

class UserrequestForm(ModelForm):
    class Meta:
        model=cl_User_request
        fields='__all__'

class NewchangeForm(ModelForm):
    class Meta:
        model=cl_New_change
        fields='__all__'

class CustomercontractForm(ModelForm):
    class Meta:
        model=cl_Customer_contract
        fields='__all__'

class ProvidercontractForm(ModelForm):
    class Meta:
        model=cl_Providercontract
        fields='__all__'

class ServicefamiliesForm(ModelForm):
    class Meta:
        model=cl_Servicefamilies
        fields='__all__'

class ServiceForm(ModelForm):
    class Meta:
        model=cl_Service
        fields='__all__'

class ServicesubcategoryForm(ModelForm):
    class Meta:
        model=cl_Service_subcategory
        fields='__all__'

class slaForm(ModelForm):
    class Meta:
        model=cl_Sla
        fields='__all__'

class sltForm(ModelForm):
    class Meta:
        model=cl_Slt
        fields='__all__'

class DeliverymodelForm(ModelForm):
    class Meta:
        model=cl_Servicedelivery
        fields='__all__'

class SyncrodataForm(ModelForm):
    class Meta:
        model=cl_Synchro_data_source
        fields='__all__'

class OauthgoogleForm(ModelForm):
    class Meta:
        model=cl_Oauth_google
        fields='__all__'

class OauthmazureeForm(ModelForm):
    class Meta:
        model=cl_Oauth_mazure
        fields='__all__'

class LdapuserForm(ModelForm):
    class Meta:
        model=cl_Ldapuser
        fields='__all__'

class ExternaluserForm(ModelForm):
    class Meta:
        model=cl_Externaluser
        fields='__all__'

class ItsmuserForm(ModelForm):
    class Meta:
        model=cl_ITSM_USER
        fields='__all__'

class SlacknotiForm(ModelForm):
    class Meta:
        model = cl_Slacknotification
        fields = '__all__'

class MicronotiForm(ModelForm):
    class Meta:
        model = cl_Microsoft_Teams_notification
        fields = '__all__'

class WebhookForm(ModelForm):
    class Meta:
        model = cl_Webhook
        fields = '__all__'

class GooglechatForm(ModelForm):
    class Meta:
        model = cl_Googlechat
        fields = '__all__'
        
class RocketchatForm(ModelForm):
    class Meta:
        model = cl_Rocketchat
        fields = '__all__'

class ItsmwebhookForm(ModelForm):
    class Meta:
        model = cl_Itsmwebhook
        fields = '__all__'







