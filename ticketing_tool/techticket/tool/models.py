from email.policy import default
from enum import unique
from operator import mod
from optparse import Option
from re import M
from xmlrpc.client import DateTime
from django.db import models
import uuid
from datetime import datetime
from django.db.models import Max


class cl_New_organization(models.Model):
    """Models which creates table for New Organization"""
    ch_name = models.CharField(max_length=100, null=True)
    ch_code = models.CharField(max_length=100, null=True)
    ch_status = models.CharField(max_length=50, null=True)
    ch_parent = models.CharField(max_length=100, null=True)
    ch_delivery_model = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.ch_name

    class Meta:
        db_table = 'cl_New_organization'


class cl_Web_server(models.Model):
    """Models which create the table for Web Server"""
    id = models.CharField(primary_key=True, editable=False, max_length=10)
    ch_name = models.CharField(max_length=100, null=True)
    ch_organization = models.ForeignKey(
        cl_New_organization, on_delete=models.CASCADE, null=True, blank=True)
    ch_status = models.CharField(max_length=100, null=True)
    ch_business_criticality = models.CharField(max_length=100, null=True)
    ch_system = models.CharField(max_length=100, null=True)
    ch_path = models.CharField(max_length=100, null=True)
    ch_software = models.CharField(max_length=100, null=True)
    ch_software_license = models.CharField(max_length=100, null=True)
    dt_move_to_production_date = models.DateTimeField(auto_now=True)
    txt_description = models.TextField()

    def __str__(self):
        return self.ch_name

    class Meta:
        db_table = 'cl_Web_server'


class cl_Brand(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=10)
    ch_brandname = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.ch_brandname

    class Meta:
        db_table = 'cl_Brand'


class cl_network_type(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=10)
    ch_nname = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.ch_nname

    class Meta:
        db_table = 'cl_network_type'


class cl_ios_version(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=10)
    ch_iosname = models.CharField(max_length=100, null=True)
    ch_brandname = models.ForeignKey(
        cl_Brand, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.ch_iosname

    class Meta:
        db_table = 'cl_ios_version'


class cl_model(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=10)
    ch_modelname = models.CharField(max_length=100, null=True)
    ch_brandname = models.ForeignKey(
        cl_Brand, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.ch_modelname

    class Meta:
        db_table = 'cl_model'


class cl_os_family(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=10)
    ch_fname = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.ch_fname

    class Meta:
        db_table = 'cl_os_family'


class cl_os_version(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=10)
    ch_osname = models.CharField(max_length=100, null=True)
    ch_fname = models.ForeignKey(
        cl_os_family, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.ch_osname

    class Meta:
        db_table = 'cl_os_version'

class cl_Servicefamilies(models.Model):
    """Models which create the table for Provider Contract"""
    id = models.CharField(primary_key=True, editable=False, max_length=10)

    ch_sname = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.ch_sname

    class Meta:
        db_table = 'cl_Servicefamilies'

# class cl_provider(models.Model):
#     id = models.CharField(primary_key=True, editable=False, max_length=10)


class cl_os_license(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=10)
    ch_name = models.CharField(max_length=100, null=True)
    ch_version = models.ForeignKey(
        cl_os_version, on_delete=models.CASCADE, null=True, blank=True)
    ch_organization = models.ForeignKey(
        cl_New_organization, on_delete=models.CASCADE, null=True, blank=True)
    ch_usage_limit = models.CharField(max_length=100, null=True)
    txt_description = models.TextField()
    ch_perpetual = models.CharField(max_length=100, null=True)
    dt_start_date = models.DateTimeField(auto_now=True)
    dt_end_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    ch_key = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.ch_name

    class Meta:
        db_table = 'cl_os_license'


class cl_Team(models.Model):
    """
    Models Which create a table for team
    """
    # id = models.AutoField(primary_key=True)
    id = models.CharField(primary_key=True, editable=False, max_length=10)

    def save(self, **kwargs):
        if not self.id:
            max = cl_Team.objects.aggregate(id_max=Max('id'))['id_max']
            self.id = "{}{:05s}".format('R', max if max is not None else 1)
        super().save(*kwargs)

    # print(id)

    # tid = models.CharField(max_length=17,unique=True, editable=False)
    ch_teamname = models.CharField(max_length=100, null=True)
    ch_teamstatus = models.CharField(max_length=100, null=True)
    # ch_organization = models.CharField(max_length=100,null=True)
    ch_organization = models.ForeignKey(
        cl_New_organization, on_delete=models.CASCADE, null=True, blank=True)
    e_team_emailfield = models.EmailField(null=True)
    i_team_phonenumber = models.CharField(max_length=200, null=True)
    b_team_notification = models.CharField(max_length=100, null=True)
    ch_team_function = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.ch_teamname

    class Meta:
        db_table = 'cl_Team'

    # return new_help_id

    # def inid():
    #     lid=cl_Team.objects.filter(id=id)
    #     print(lid)

    #     if not lid:
    #         return 'R-'+'0000'

    #     t_id=lid.tid
    #     hin=t_id[:5]
    #     n_int=int(hin)+1
    #     n_id='R-'+str(n_int).zfill(4)
    #     return n_id
    # print(inid)

    # def increment_helpdesk_number():
    #     last_helpdesk = cl_Team.objects.all().order_by('id').last()

    #     if not last_helpdesk:
    #         return 'R-'+'0000'

   # help_id = last_helpdesk.help_num
   # help_int = help_id[13:17]
    #new_help_int = int(help_int) + 1
    #new_help_id = 'HEL-' + str(datetime.now().strftime('%Y%m%d-')) + str(new_help_int).zfill(4)

    # return new_help_id
    # ticket_id = models.CharField(max_length=17, unique=True, default=increment_helpdesk_number, editable=False, blank=True)
    # id = models.AutoField(primary_key=True)
    # def build_id(self, id):
    #     Rid='R'+'-'+str(id)
    #     return (Rid)

    # ticket_id = models.CharField(max_length=15, default=(build_id(None, id)))

    # def save(self, **kwargs):
    #     if not self.id:
    #         max = cl_Team.objects.aggregate(id_max=Max('id'))['id_max']
    #         self.id = "{:05d}".format('R', max if max is not None else 1)
    #     super().save(*kwargs


class cl_Person(models.Model):
    """Models which create table for Person Information"""
    ch_person_firstname = models.CharField(max_length=100, null=True)
    ch_person_lastname = models.CharField(max_length=100, null=True)
    ch_organization = models.ForeignKey(
        cl_New_organization, on_delete=models.CASCADE, null=True, blank=True)
    ch_team = models.ForeignKey(
        cl_Team, on_delete=models.CASCADE, null=True, blank=True)
    ch_person_status = models.CharField(max_length=100, null=True)
    ch_person_location = models.CharField(max_length=100, null=True)
    ch_person_function = models.CharField(max_length=100, null=True)
    ch_manager = models.CharField(max_length=100, null=True)
    ch_employee_number = models.CharField(max_length=100, null=True)
    e_person_email = models.EmailField(null=True)
    ch_person_phone = models.CharField(max_length=100, null=True)
    ch_person_mobilenumber = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.ch_person_firstname

    class Meta:
        db_table = 'cl_Person'


class cl_Location(models.Model):
    """This model create table for details of location"""
    id = models.AutoField(primary_key=True, editable=False)

    ch_location_name = models.CharField(max_length=100, null=True)
    txt_address = models.TextField(null=True)
    ch_owner_organization = models.ForeignKey(
        cl_New_organization, on_delete=models.CASCADE, null=True, blank=True)
    ch_city = models.CharField(max_length=100, null=True)
    i_pincode = models.IntegerField()
    ch_country = models.CharField(max_length=100, null=True)
    ch_status = models.CharField(max_length=100, default='active')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cl_Location'


class tassign(models.Model):
    ch_teamname = models.ForeignKey(cl_Team, on_delete=models.CASCADE)
    ch_person_firstname = models.ForeignKey(
        cl_Person, on_delete=models.CASCADE)


class cl_Document(models.Model):
    """This model creates table for to insert information about documentation """
    id = models.AutoField(primary_key=True, editable=False)

    id = models.AutoField(primary_key=True, editable=False)
    ch_name = models.CharField(max_length=100, null=True)
    ch_organization = models.ForeignKey(
        cl_New_organization, on_delete=models.CASCADE, null=True, blank=True)
    ch_version = models.CharField(max_length=100, null=True)
    txt_description = models.TextField()
    """ Create here Disable Document type  """
    txt_text = models.TextField(null=True)
    url_URL = models.URLField(null=True)
    ch_File = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.ch_name

    class Meta:
        db_table = 'cl_Document'


class cl_Software(models.Model):
    """This models creates table for Software"""
    id = models.CharField(primary_key=True, editable=False, max_length=10)
    ch_name = models.CharField(max_length=100, null=True)
    ch_vendor = models.CharField(max_length=100, null=True)
    chversion = models.CharField(max_length=100, null=True)
    ch_type = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.ch_name

    class Meta:
        db_table = 'cl_Software'


class cl_Application_solution(models.Model):
    """Models which create table for Application Solution"""
    id = models.AutoField(primary_key=True, editable=False)

    ch_name = models.CharField(max_length=100, null=True)
    ch_organization = models.ForeignKey(
        cl_New_organization, on_delete=models.CASCADE, null=True, blank=True)
    ch_business_criticality = models.CharField(max_length=100, null=True)
    dt_move_to_production_date = models.DateTimeField(auto_now=True)
    txt_description = models.TextField()

    def __str__(self):
        return self.ch_name

    class Meta:
        db_table = 'cl_Application_solution'

class cl_Service(models.Model):
    """Models which create the table for Service"""
    id = models.CharField(primary_key=True, editable=False, max_length=10)

    ch_ssname = models.CharField(max_length=100, null=True)
    ch_sprovider = models.ForeignKey(
        cl_New_organization,  related_name='cl_new_organization_ch_sprovider', on_delete=models.CASCADE, null=True, blank=True)
    ch_service_family = models.ForeignKey(
        cl_Servicefamilies,  related_name='cl_servicefamilies_ch_service_family', on_delete=models.CASCADE, null=True, blank=True)
    ch_status = models.CharField(max_length=100, null=True)
    txt_description = models.TextField()

    def __str__(self):
        return self.ch_ssname

    class Meta:
        db_table = 'cl_Service'


class cl_Delivery_model(models.Model):
    """Models which create table for Delivery Model"""
    id = models.AutoField(primary_key=True, editable=False)

    ch_application_name = models.CharField(max_length=50, null=True)
    ch_oranization = models.ForeignKey(
        cl_New_organization, on_delete=models.CASCADE, null=True, blank=True)
    txt_description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cl_Delivery_model'


# class cl_Delivery_model(models.Model):
#     ch_name = models.CharField(max_length=50, null=True)
#     ch_organization = models.ForeignKey(
#         cl_New_organization, on_delete=models.CASCADE, null=True, blank=True)
#     ch_description = models.TextField()

#     def __str__(self):
#         return self.name

#     class Meta:
#         db_table = 'cl_Delivery_model'


class cl_Business_process(models.Model):
    """Models which creates table for Business Process"""
    id = models.AutoField(primary_key=True, editable=False)
    ch_business_name = models.CharField(max_length=100, null=True)
    ch_organization = models.ForeignKey(
        cl_New_organization, on_delete=models.CASCADE, null=True, blank=True)
    ch_status = models.CharField(max_length=50, null=True)
    ch_business_criticality = models.CharField(max_length=100, null=True)
    dt_move_to_production_date = models.DateTimeField(auto_now=True)
    txt_description = models.TextField()

    def __str__(self):
        return self.ch_business_name

    class Meta:
        db_table = 'cl_Business_process'


class cl_Newdb_server(models.Model):
    """ ivEdit which creates table for New db Server"""
    id = models.AutoField(primary_key=True, editable=False)
    ch_dbname = models.CharField(max_length=100, null=True)
    ch_organization = models.ForeignKey(
        cl_New_organization, on_delete=models.CASCADE, null=True, blank=True)
    ch_status = models.CharField(max_length=50, null=True)
    ch_business_criticality = models.CharField(max_length=100, null=True)
    dt_move_to_production_date = models.DateTimeField(auto_now=True)
    ch_software = models.CharField(max_length=100, null=True)
    ch_software_license = models.CharField(max_length=100, null=True)
    ch_system = models.CharField(max_length=100, null=True)
    ch_path = models.CharField(max_length=100, null=True)
    txt_description = models.TextField()

    def __str__(self):
        return self.ch_dbname

    class Meta:
        db_table = 'cl_Newdb_server'


class cl_Database_schema(models.Model):
    """Models which create the table for Database Schema """
    id = models.AutoField(primary_key=True, editable=False)
    ch_name = models.CharField(max_length=100, null=True)
    ch_organization = models.ForeignKey(
        cl_New_organization, on_delete=models.CASCADE, null=True, blank=True)
    ch_db_server = models.CharField(max_length=100, null=True)
    ch_business_criticality = models.CharField(max_length=100, null=True)
    dt_move_to_production_date = models.DateTimeField(auto_now=True)
    txt_description = models.TextField()

    def __str__(self):
        return self.ch_name

    class Meta:
        db_table = 'cl_Database_schema'


class cl_New_middleware(models.Model):
    """Models which create the table for New Middleware"""
    id = models.AutoField(primary_key=True, editable=False)
    ch_name = models.CharField(max_length=100, null=True)
    ch_organization = models.ForeignKey(
        cl_New_organization, on_delete=models.CASCADE, null=True, blank=True)
    ch_status = models.CharField(max_length=50, null=True)
    ch_system = models.CharField(max_length=100, null=True)
    ch_software = models.CharField(max_length=100, null=True)
    ch_software_license = models.CharField(max_length=100, null=True)
    ch_path = models.CharField(max_length=100, null=True)
    ch_business_criticality = models.CharField(max_length=100, null=True)
    dt_move_to_production_date = models.DateTimeField(auto_now=True)
    txt_description = models.TextField()

    def __str__(self):
        return self.ch_name

    class Meta:
        db_table = 'cl_New_middleware'


class cl_Middleware_instance(models.Model):
    """Models which creates the table for Middleware Instance """
    id = models.AutoField(primary_key=True, editable=False)
    ch_name = models.CharField(max_length=100, null=True)
    ch_organization = models.ForeignKey(
        cl_New_organization, on_delete=models.CASCADE, null=True, blank=True)
    ch_middleware = models.CharField(max_length=100, null=True)
    ch_business_criticality = models.CharField(max_length=100, null=True)
    dt_move_to_production_date = models.DateTimeField(auto_now=True)
    txt_description = models.TextField()

    def __str__(self):
        return self.ch_name

    class Meta:
        db_table = 'cl_Middleware_instance'


class cl_Network_device(models.Model):
    """Models which create table for Network Device"""
    id = models.AutoField(primary_key=True, editable=False)
    ch_name = models.CharField(max_length=100, null=True)
    ch_organization = models.ForeignKey(
        cl_New_organization, on_delete=models.CASCADE, null=True, blank=True)
    ch_status = models.CharField(max_length=100, null=True)
    ch_business_criticality = models.CharField(max_length=100, null=True)
    ch_location = models.CharField(max_length=100, null=True)
    ch_network_type = models.ForeignKey(
        cl_network_type, on_delete=models.CASCADE, null=True, blank=True)
    ch_brand = models.ForeignKey(
        cl_Brand, on_delete=models.CASCADE, null=True, blank=True)
    ch_model = models.ForeignKey(
        cl_model, on_delete=models.CASCADE, null=True, blank=True)
    i_os_version = models.ForeignKey(
        cl_ios_version, on_delete=models.CASCADE, null=True, blank=True)
    i_management_ip = models.IntegerField()
    ch_ram = models.CharField(max_length=100, null=True)
    i_rack_unit = models.IntegerField()
    i_serial_number = models.IntegerField()
    i_asset_number = models.IntegerField()
    dt_move_to_production_date = models.DateTimeField(auto_now=True)
    dt_purchase_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    dt_end_of_warranty = models.DateField(default=datetime)
    txt_description = models.TextField()

    def __str__(self):
        return self.ch_name

    class Meta:
        db_table = 'cl_Network_device'


class cl_Other_software(models.Model):
    """Modles which create the table for Other Software"""
    id = models.AutoField(primary_key=True, editable=False)
    ch_name = models.CharField(max_length=100, null=True)
    ch_organization = models.ForeignKey(
        cl_New_organization, on_delete=models.CASCADE, null=True, blank=True)
    ch_status = models.CharField(max_length=100, null=True)
    ch_business_criticality = models.CharField(max_length=100, null=True)
    ch_system = models.CharField(max_length=100, null=True)
    ch_path = models.CharField(max_length=100, null=True)
    ch_software = models.CharField(max_length=100, null=True)
    ch_software_license = models.CharField(max_length=100, null=True)
    dt_move_to_production_date = models.DateTimeField(auto_now=True)
    txt_description = models.TextField()

    def __str__(self):
        return self.ch_name

    class Meta:
        db_table = 'cl_Other_software'


class cl_Web_application(models.Model):
    """Models which create the table for Web Application """
    id = models.AutoField(primary_key=True, editable=False)
    ch_name = models.CharField(max_length=100, null=True)
    ch_organization = models.ForeignKey(
        cl_New_organization, on_delete=models.CASCADE, null=True, blank=True)
    ch_webserver = models.ForeignKey(
        cl_Web_server, on_delete=models.CASCADE, null=True, blank=True)
    url_website = models.URLField(max_length=200)
    ch_business_criticality = models.CharField(max_length=100, null=True)
    dt_move_to_production_date = models.DateTimeField(auto_now=True)
    txt_description = models.TextField()

    def __str__(self):
        return self.ch_name

    class Meta:
        db_table = 'cl_Web_application'


class cl_Server(models.Model):
    """ Models which create the table for Server"""
    id = models.AutoField(primary_key=True, editable=False)
    ch_name = models.CharField(max_length=100, null=True)
    ch_organization = models.ForeignKey(
        cl_New_organization, on_delete=models.CASCADE, null=True, blank=True)
    ch_status = models.CharField(max_length=100, null=True)
    ch_business_criticality = models.CharField(max_length=100, null=True)
    ch_location = models.CharField(max_length=100, null=True)
    ch_os_family = models.ForeignKey(
        cl_os_family, on_delete=models.CASCADE, null=True, blank=True)
    ch_brand = models.ForeignKey(
        cl_Brand, on_delete=models.CASCADE, null=True, blank=True)
    ch_model = models.ForeignKey(
        cl_model, on_delete=models.CASCADE, null=True, blank=True)
    i_os_version = models.ForeignKey(
        cl_os_version, on_delete=models.CASCADE, null=True, blank=True)
    i_management_ip = models.IntegerField()
    i_os_license = models.ForeignKey(
        cl_os_license, on_delete=models.CASCADE, null=True, blank=True)
    ch_ram = models.CharField(max_length=100, null=True)
    ch_cpu = models.CharField(max_length=100, null=True)
    i_rack_unit = models.IntegerField()
    i_serial_number = models.IntegerField()
    i_asset_number = models.IntegerField()
    dt_move_to_production_date = models.DateTimeField(auto_now=True)
    dt_purchase_date = models.DateTimeField(auto_now=True)
    dt_end_of_warranty = models.DateTimeField(
        auto_now=False, auto_now_add=False)
    txt_description = models.TextField()

    def __str__(self):
        return self.ch_name

    class Meta:
        db_table = 'cl_Server'


class cl_Pc_software(models.Model):
    """Models Which create the table for PC Software """
    id = models.AutoField(primary_key=True, editable=False)
    ch_name = models.CharField(max_length=100, null=True)
    ch_organization = models.ForeignKey(
        cl_New_organization, on_delete=models.CASCADE, null=True, blank=True)
    ch_status = models.CharField(max_length=100, null=True)
    ch_business_criticality = models.CharField(max_length=100, null=True)
    ch_system = models.CharField(max_length=100, null=True)
    ch_path = models.CharField(max_length=100, null=True)
    ch_software = models.CharField(max_length=100, null=True)
    ch_software_license = models.CharField(max_length=100, null=True)
    ch_path = models.CharField(max_length=100, null=True)
    dt_move_to_production_date = models.DateTimeField(auto_now=True)
    txt_description = models.TextField()

    def __str__(self):
        return self.ch_name

    class Meta:
        db_table = 'cl_Pc_software'


class cl_User_request(models.Model):
    """Models which create the table for User Request"""
    id = models.AutoField(primary_key=True, editable=False)
    fk_organization = models.ForeignKey(
        cl_New_organization, on_delete=models.CASCADE, null=True, blank=True)
    fk_caller = models.ForeignKey(
        cl_Person, on_delete=models.CASCADE, null=True, blank=True)
    ch_status = models.CharField(max_length=100, default='active')
    ch_origin = models.CharField(max_length=100, null=True)
    ch_title = models.CharField(max_length=100, null=True)
    ch_request_type = models.CharField(max_length=100, null=True)
    ch_impact = models.CharField(max_length=100, null=True)
    ch_urgency = models.CharField(max_length=100, null=True)
    ch_priority = models.CharField(max_length=100, null=True)
    dt_start_date = models.DateTimeField(auto_now=True)
    dt_end_date = models.DateTimeField(auto_now=True)
    dt_tto = models.CharField(max_length=10)
    dt_ttr = models.CharField(max_length=10)
    ch_service = models.CharField(max_length=100, null=True)
    ch_service_subcategory = models.CharField(max_length=100, null=True)
    ch_parent_request = models.CharField(max_length=100, null=True)
    ch_parent_change = models.CharField(max_length=100, null=True)
    txt_description = models.TextField()
    ch_agent = models.CharField(max_length=100, default='Deallocate')

    def __str__(self):
        return self.ch_status

    class Meta:
        db_table = 'cl_User_request'


class cl_New_change(models.Model):
    """Models which create the table for New Change"""
    ch_organization = models.ForeignKey(
        cl_New_organization, on_delete=models.CASCADE, null=True, blank=True)
    ch_caller = models.CharField(max_length=100, null=True)
    ch_status = models.CharField(max_length=100, default='new')
    ch_category = models.CharField(max_length=100, null=True)
    ch_title = models.CharField(max_length=100, null=True)
    dt_start_date = models.DateTimeField(default=datetime.now)
    dt_Updated_date = models.DateTimeField(default=datetime.now)
    ch_parent_change = models.CharField(max_length=100, null=True)
    txt_fallback_plan = models.CharField(max_length=100, null=True)
    txt_description = models.CharField(max_length=100, null=True)
    ch_assign_agent = models.CharField(max_length=100, null=True, default="Deallocated")

    def __str__(self):
        return self.ch_organization

    class Meta:
        db_table = 'cl_New_change'


class cl_Customer_contract(models.Model):
    """Models which create the table for User Request"""
    id = models.AutoField(primary_key=True, editable=False)
    ch_cname = models.CharField(max_length=100, null=True)
    ch_ccustomer = models.ForeignKey(
        cl_New_organization,  related_name='cl_new_organization_ch_ccustomer', on_delete=models.CASCADE, null=True, blank=True)
    ch_status = models.CharField(max_length=100, default='new')
    ch_contract_type = models.CharField(max_length=100, null=True)
    ch_pprovider = models.ForeignKey(
        cl_New_organization,  related_name='cl_new_organization_ch_pprovider', on_delete=models.CASCADE, null=True, blank=True)
    dt_start_date = models.DateTimeField(auto_now=True)
    dt_end_date = models.DateTimeField(auto_now=True)
    i_cost_unit = models.IntegerField()
    i_cost = models.IntegerField()
    i_cost_currency = models.IntegerField()
    i_billing_frequency = models.IntegerField()
    txt_description = models.TextField()

    def __str__(self):
        return self.ch_cname

    class Meta:
        db_table = 'cl_Customer_contract'


class cl_Providercontract(models.Model):
    """Models which create the table for Provider Contract"""
    id = models.AutoField(primary_key=True, editable=False)
    ch_pname = models.CharField(max_length=100, null=True)
    ch_customer = models.ForeignKey(
        cl_New_organization,  related_name='cl_new_organization_ch_customer', on_delete=models.CASCADE, null=True, blank=True)
    ch_status = models.CharField(max_length=100, default='new')
    ch_contract_type = models.CharField(max_length=100, null=True)
    ch_pcprovider = models.ForeignKey(
        cl_New_organization,  related_name='cl_new_organization_ch_pcprovider', on_delete=models.CASCADE, null=True, blank=True)

    dt_start_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    dt_end_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    i_cost_unit = models.IntegerField()
    i_cost = models.IntegerField()
    i_cost_currency = models.IntegerField()
    i_billing_frequency = models.IntegerField()
    txt_description = models.TextField()
    ch_sla = models.TextField()

    def __str__(self):
        return self.ch_pname

    class Meta:
        db_table = 'cl_Providercontract'








class cl_Service_subcategory(models.Model):
    """Models which create the table for Provider Contract"""
    id = models.AutoField(primary_key=True, editable=False)

    ch_subname = models.CharField(max_length=100, null=True)
    ch_sservice = models.ForeignKey(
        cl_Service, on_delete=models.CASCADE, null=True, blank=True)
    ch_status = models.CharField(max_length=100, null=True)
    ch_request_type = models.CharField(max_length=100, null=True)
    txt_description = models.TextField()

    def __str__(self):
        return self.ch_subname

    class Meta:
        db_table = 'cl_Service_subcategory'


class cl_Sla(models.Model):
    """Models which create the table for Provider Contract"""
    id = models.AutoField(primary_key=True, editable=False)

    ch_slname = models.CharField(max_length=100, null=True)
    ch_slaprovider = models.ForeignKey(
        cl_New_organization,  related_name='cl_new_organization_ch_slaprovider', on_delete=models.CASCADE, null=True, blank=True)
    txt_description = models.TextField()

    def __str__(self):
        return self.ch_slname

    class Meta:
        db_table = 'cl_Sla'


class cl_Slt(models.Model):
    """Models which create the table for SLT"""
    id = models.AutoField(primary_key=True, editable=False)

    ch_name = models.CharField(max_length=100, null=True)
    ch_priority = models.CharField(max_length=100, null=True)
    ch_request_type = models.CharField(max_length=100, null=True)
    ch_metric = models.CharField(max_length=100, null=True)
    ch_value = models.CharField(max_length=100, null=True)
    ch_unit = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.ch_name

    class Meta:
        db_table = 'cl_Slt'


class cl_Servicedelivery(models.Model):

    """Models which create the table for Service Delivery"""
    id = models.AutoField(primary_key=True, editable=False)
    ch_sdname = models.CharField(max_length=100, null=True)
    ch_organization = models.ForeignKey(
        cl_New_organization, related_name='cl_new_organization', on_delete=models.CASCADE, null=True, blank=True)
    txt_description = models.TextField()

    def __str__(self):
        return self.ch_sdname

    class Meta:
        db_table = 'cl_Servicedelivery'


class cl_Synchro_data_source(models.Model):

    """Models which create the table for Synchro Data Source"""
    id = models.AutoField(primary_key=True, editable=False)

    ch_name = models.CharField(max_length=100, null=True)
    ch_status = models.CharField(max_length=100, default='implementation')
    txt_description = models.TextField()
    ch_target_class = models.CharField(max_length=100, null=True)
    ch_user = models.CharField(max_length=100, null=True)
    ch_contact_notify = models.CharField(max_length=100, null=True)
    url_icon_hyperlink = models.URLField(max_length=200)
    url_Application_hyperlink = models.URLField(max_length=200)
    ch_data_table = models.CharField(max_length=100, null=True)
    ch_reconciliation_policy = models.CharField(max_length=100, null=True)
    ch_action_on_zero = models.CharField(max_length=100, null=True)
    ch_action_on_one = models.CharField(max_length=100, null=True)
    ch_action_on_many = models.CharField(max_length=100, null=True)
    ch_users_allowed = models.CharField(max_length=100, null=True)
    ch_update_rules = models.CharField(max_length=100, null=True)
    ch_delete_policy = models.CharField(max_length=100, null=True)
    dt_full_load_interval = models.DateTimeField(
        auto_now=False, auto_now_add=False)
    dt_retention_duration = models.DateTimeField(
        auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.ch_name

    class Meta:
        db_table = 'cl_Synchro_data_source'


class cl_Oauth_google(models.Model):
    """Models which create the table for Oauth Google"""
    id = models.AutoField(primary_key=True, editable=False)

    e_login = models.EmailField()
    ch_status = models.CharField(max_length=100, default='No Acess token')
    ch_provider = models.CharField(max_length=100, default='Google')
    txt_description = models.TextField()
    ch_client_id = models.CharField(max_length=100, null=True)
    ch_client_secret = models.CharField(max_length=100, null=True)
    ch_scope = models.CharField(max_length=100, default='SMTP')
    ch_advanced_scope = models.CharField(max_length=100, null=True)
    ch_used_smtp = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.ch_name

    class Meta:
        db_table = 'cl_Oauth_google'


class cl_Oauth_mazure(models.Model):
    """Models which create the table for Oauth Google"""
    id = models.AutoField(primary_key=True, editable=False)

    e_login = models.EmailField()
    ch_status = models.CharField(max_length=100, default='No Acess token')
    ch_provider = models.CharField(max_length=100, default='Azure')
    txt_description = models.TextField()
    ch_client_id = models.CharField(max_length=100, null=True)
    ch_client_secret = models.CharField(max_length=100, null=True)
    ch_scope = models.CharField(max_length=100, default='SMTP')
    ch_advanced_scope = models.CharField(max_length=100, null=True)
    ch_used_smtp = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.ch_name

    class Meta:
        db_table = 'cl_Oauth_mazure'


class cl_Ldapuser(models.Model):
    id = models.AutoField(primary_key=True, editable=False)

    ch_person = models.CharField(max_length=100, null=True)
    ch_ldapserver = models.CharField(max_length=100, null=True)
    e_email = models.EmailField()
    ch_login = models.CharField(max_length=100, null=True)
    ch_language = models.CharField(max_length=100, null=True)
    ch_status = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.ch_name

    class Meta:
        db_table = 'cl_Ldapuser'


class cl_Externaluser(models.Model):
    """Models which create the table for External User"""
    id = models.AutoField(primary_key=True, editable=False)

    ch_person = models.CharField(max_length=100, null=True)
    ch_first_name = models.CharField(max_length=100, null=True)
    e_email = models.EmailField()
    ch_login = models.CharField(max_length=100, null=True)
    ch_language = models.CharField(max_length=100, null=True)
    ch_status = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.ch_name

    class Meta:
        db_table = 'cl_Externaluser'


class ch_Itsmuser(models.Model):
    """Models which create the table for Itsmuser """
    id = models.AutoField(primary_key=True, editable=False)

    ch_person = models.CharField(max_length=100, null=True)
    ch_email = models.EmailField()
    ch_login = models.CharField(max_length=100, null=True)
    ch_language = models.CharField(max_length=100, null=True)
    ch_status = models.CharField(max_length=100, null=True)
    ch_person = models.CharField(max_length=100, null=True)
    ch_password = models.CharField(max_length=100, null=True)
    ch_password_expiration = models.CharField(max_length=100, null=True)
    dt_password_renewed_on = models.DateTimeField(
        auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.ch_name

    class Meta:
        db_table = 'ch_Itsmuser'


class cl_Slacknotification(models.Model):
    """Models which create the table for Slacknotification"""
    id = models.AutoField(primary_key=True, editable=False)

    ch_name = models.CharField(max_length=100, null=True)
    txt_description = models.TextField()
    ch_status = models.CharField(max_length=100, default='Inactive')
    ch_language = models.CharField(max_length=100, default='English')
    ch_Connection = models.CharField(max_length=100, null=True)
    ch_testconnection = models.CharField(max_length=100, null=True)
    txt_message = models.TextField()
    ch_Attributes_forms = models.CharField(max_length=100, null=True)
    ch_modify_button = models.CharField(max_length=100, null=True)
    b_delete_button = models.BooleanField()
    b_other_action = models.BooleanField()
    ch_other_action_code = models.CharField(max_length=100, null=True)
    b_user_info = models.BooleanField()
    ch_Prepare_payload_callback = models.CharField(max_length=100, null=True)
    ch_Process_response_callback = models.CharField(max_length=100, null=True)
    b_other_action = models.BooleanField()
    ch_other_action_code = models.CharField(max_length=100, null=True)
    b_user_info = models.BooleanField()

    def __str__(self):
        return self.ch_name

    class Meta:
        db_table = 'cl_Slacknotification'


class cl_Microsoft_Teams_notification(models.Model):
    """Models which create the table for Microsoft_Teams_notification"""
    id = models.AutoField(primary_key=True, editable=False)

    ch_name = models.CharField(max_length=100, null=True)
    txt_description = models.TextField()
    ch_status = models.CharField(max_length=100, default='Inactive')
    ch_language = models.CharField(max_length=100, default='English')
    ch_Connection = models.CharField(max_length=100, null=True)
    ch_testconnection = models.CharField(max_length=100, null=True)
    txt_message = models.TextField()
    ch_Attributes_forms = models.CharField(max_length=100, null=True)
    ch_modify_button = models.CharField(max_length=100, null=True)
    b_delete_button = models.BooleanField()
    ch_Prepare_payload_callback = models.CharField(max_length=100, null=True)
    ch_Process_response_callback = models.CharField(max_length=100, null=True)
    b_other_action = models.BooleanField()
    ch_other_action_code = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cl_Microsoft_Teams_notification'


class cl_Webhook(models.Model):
    """Models which create the table for WebHook"""
    id = models.AutoField(primary_key=True, editable=False)

    ch_name = models.CharField(max_length=100, null=True)
    txt_description = models.TextField()
    ch_status = models.CharField(max_length=100, default='Inactive')
    ch_language = models.CharField(max_length=100, default='English')
    ch_Connection = models.CharField(max_length=100, null=True)
    ch_testconnection = models.CharField(max_length=100, null=True)
    txt_message = models.TextField()
    ch_method = models.CharField(max_length=100, null=True)
    ch_headers = models.CharField(max_length=100, null=True)
    ch_payload = models.CharField(max_length=100, null=True)
    b_delete_button = models.BooleanField()
    ch_Prepare_payload_callback = models.CharField(max_length=100, null=True)
    ch_Process_response_callback = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.ch_name

    class Meta:
        db_table = 'cl_Webhook'


class cl_Googlechat(models.Model):
    """Models which create the table for GoogleChat"""
    ch_name = models.CharField(max_length=100, null=True)
    txt_description = models.TextField()
    ch_status = models.CharField(max_length=100, default='Inactive')
    ch_language = models.CharField(max_length=100, default='English')
    ch_Connection = models.CharField(max_length=100, null=True)
    ch_testconnection = models.CharField(max_length=100, null=True)
    txt_message = models.TextField()
    ch_Prepare_payload_callback = models.CharField(max_length=100, null=True)
    ch_Process_response_callback = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.ch_name

    class Meta:
        db_table = 'cl_Googlechat'


class cl_Rocketchat(models.Model):
    """Models which create the table for Rocketchat"""
    ch_name = models.CharField(max_length=100, null=True)
    txt_description = models.TextField()
    ch_status = models.CharField(max_length=100, default='Inactive')
    ch_language = models.CharField(max_length=100, default='English')
    ch_Connection = models.CharField(max_length=100, null=True)
    ch_testconnection = models.CharField(max_length=100, null=True)
    txt_message = models.TextField()
    ch_Prepare_payload_callback = models.CharField(max_length=100, null=True)
    ch_Process_response_callback = models.CharField(max_length=100, null=True)
    ch_Alias = models.CharField(max_length=100, null=True)
    ch_Image_avtar = models.CharField(max_length=100, null=True)
    Emoji_avtar = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cl_Rocketchat'


class cl_Itsmwebhook(models.Model):
    """Models which create the table for Itsmwebhook"""
    ch_name = models.CharField(max_length=100, null=True)
    txt_description = models.TextField()
    ch_status = models.CharField(max_length=100, default='Inactive')
    ch_language = models.CharField(max_length=100, default='English')
    ch_Connection = models.CharField(max_length=100, null=True)
    ch_testconnection = models.CharField(max_length=100, null=True)
    txt_headers = models.TextField()
    txt_json_data = models.TextField()
    Prepare_payload_callback = models.CharField(max_length=100, null=True)
    Process_response_callback = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cl_Itsmwebhook'