from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# 1st task
# class users(models.Model):
#     # User         = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
#     users_Id     = models.AutoField(primary_key=True)
#     username     = models.CharField(max_length=20, default=None, blank=True, null=True)
#     password     = models.CharField(max_length=15, default=None, blank=True, null=True)
#     status       = models.IntegerField(default=None, blank=True, null=True)
    
#     def __str__(self):
#         #return self.region_txt,self.region_code,self.region_id
#         #return '%s %s'%(self.region_txt,self.region_code)
#         return '{} {} {} '.format(self.username,self.password,self.status)

class user_level(models.Model):
    level_id     = models.AutoField(primary_key=True)
    level_name     = models.CharField(max_length=20, default=None, blank=True, null=True)
   
    def __str__(self):
        # this code shows the outpot in the admin panel
        return '{} {} '.format(self.level_name,self.level_id)

class region(models.Model):
    region_id             = models.AutoField(primary_key=True)
    region_txt             = models.CharField(max_length=100, default=None, blank=True, null=True)
    region_code            = models.CharField(max_length=100, default=None, blank=True, null=True)
    priority           = models.IntegerField(default=None, blank=True, null=True)

    def __str__(self):
              # this code shows the outpot in the admin panel
        return '{} {} {} {} '.format(self.region_txt,self.region_id,self.region_code,self.priority)

class depot(models.Model):
    depot_id              = models.CharField(primary_key=True,max_length=10)
    depot_txt             = models.CharField(max_length=100, default=None, blank=True, null=True)
    deport_tel            = models.CharField(max_length=100, default=None, blank=True, null=True)
    deport_image          = models.CharField(max_length=500, default=None, blank=True, null=True)
    region_id             = models.ForeignKey(region, to_field='region_id', related_name="users_region_set" , on_delete=models.CASCADE)
    priority              = models.BooleanField(default=True)
    sortid                = models.BooleanField(default=True)

    def __str__(self):
              # this code shows the outpot in the admin panel
        return '{} {} {} {}  '.format(self.depot_txt,self.deport_tel,self.region_id,self.priority)

class region_auth(models.Model):
    
    region_auth_id       = models.AutoField(primary_key=True)
    region_id            = models.ForeignKey(region, to_field='region_id', related_name="region_id_set" , on_delete=models.CASCADE)
    deport_id            = models.ForeignKey(depot, to_field='depot_id', related_name="depot_id_set" , on_delete=models.CASCADE)
    user_level           = models.ForeignKey(user_level, to_field='level_id', related_name="level_id_set" , on_delete=models.CASCADE)
    # users_Id             = models.ForeignKey(users, to_field='users_Id', related_name="reg_id_set" , on_delete=models.CASCADE)
    # user_Id             = models.ForeignKey(User, to_field='id', related_name="auth_User_id_set" , on_delete=models.CASCADE)
    # user_Id             = models.ForeignKey(User, to_field='id', related_name="id_set" , on_delete=models.CASCADE)
    user_Id             = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)

    def __str__(self):
              # this code shows the outpot in the admin panel
        return '{} {} {} {} '.format(self.region_id,self.deport_id,self.user_level,self.users_Id)

class user_details(models.Model):
    # user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    users_Id         = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    # users_Id         = models.ForeignKey(users, to_field='users_Id', related_name="users_Idset" ,unique=True, on_delete=models.CASCADE, primary_key=True)
    first_name      = models.CharField(max_length=100, default=None, blank=True, null=True)
    last_name       = models.CharField(max_length=100, default=None, blank=True, null=True)
    gender          = models.CharField(max_length=100, default=None, blank=True, null=True)
    Address          = models.CharField(max_length=100, default=None, blank=True, null=True)
    created_time      = models.TimeField(max_length=100, default=None, blank=True, null=True)
    image_url        = models.CharField(max_length=100, default=None, blank=True, null=True)
    tel_no          = models.CharField(max_length=100, default=None, blank=True, null=True)

    def __str__(self):
              # this code shows the outpot in the admin panel
        return '{} {} {} {} '.format(self.first_name,self.last_name,self.gender,self.tel_no)

# 2nd task
class document(models.Model):
    document_id           = models.AutoField(primary_key=True)
    document_type         = models.CharField(max_length=3, default=None, blank=True, null=True)
    internal_doc_no       = models.CharField(max_length=500, default=None, blank=True, null=True)
    storage_location      = models.CharField(max_length=20, default=None, blank=True, null=True)
    document_date         = models.CharField(max_length=15, default=None, blank=True, null=True)
    case_no               = models.CharField(max_length=100, default=None, blank=True, null=True)
    court                 = models.CharField(max_length=500, default=None, blank=True, null=True)
    var_text1                 = models.CharField(max_length=50, default=None, blank=True, null=True)
    var_text2                 = models.CharField(max_length=50, default=None, blank=True, null=True)
    var_text3                 = models.CharField(max_length=50, default=None, blank=True, null=True)
    var_text4                 = models.CharField(max_length=50, default=None, blank=True, null=True)
    var_text5                 = models.CharField(max_length=50, default=None, blank=True, null=True)
    var_text6                 = models.CharField(max_length=50, default=None, blank=True, null=True)
    var_text7                 = models.CharField(max_length=100, default=None, blank=True, null=True)
    var_text8                 = models.CharField(max_length=100, default=None, blank=True, null=True)
    operation                 = models.CharField(max_length=100, default=None, blank=True, null=True)
    loadingCost               = models.DecimalField(max_digits=10,decimal_places=2, default=None, blank=True, null=True)
    packingCost               = models.DecimalField(max_digits=10,decimal_places=2, default=None, blank=True, null=True)
    landing_charge            = models.DecimalField(max_digits=10,decimal_places=2, default=None, blank=True, null=True)
    tax                       = models.DecimalField(max_digits=10,decimal_places=2, default=None, blank=True, null=True)
    other_fines               = models.DecimalField(max_digits=10,decimal_places=2, default=None, blank=True, null=True)
    totsale                   = models.DecimalField(max_digits=10,decimal_places=2, default=None, blank=True, null=True)
    time                      = models.TimeField( default=None, blank=True, null=True)
    user                      = models.CharField(max_length=15, default=None, blank=True, null=True)
    trasferPostDate           = models.DateTimeField( default=None, blank=True, null=True)
    trasferSavedDate          = models.DateTimeField( default=None, blank=True, null=True)
    printed                   = models.IntegerField(default=None, blank=True, null=True)
    # region_id             = models.ForeignKey(region, to_field='region_id', related_name="users_region_set" , on_delete=models.CASCADE)

    def __str__(self):
              # this code shows the outpot in the admin panel
        return '{} {} {} {}  '.format(self.document_type,self.document_date,self.totsale,self.case_no)

class master_data(models.Model):
    material_no           = models.AutoField(primary_key=True)
    length                = models.DecimalField(max_digits=10,decimal_places=2 ,default=None, blank=True, null=True)
    girth                 = models.DecimalField(max_digits=10,decimal_places=2 ,default=None, blank=True, null=True)
    volume                = models.DecimalField(max_digits=10,decimal_places=2 ,default=None, blank=True, null=True)
    reduced_volume        = models.DecimalField(max_digits=10,decimal_places=2 , default=None, blank=True, null=True)
    time                  = models.TimeField(default=None, blank=True, null=True)
    user                  = models.CharField(max_length=20, default=None, blank=True, null=True)
    visible_material_no   = models.CharField(max_length=100, default=None, blank=True, null=True)
    # QR_ID added 
    qr_id                 = models.CharField(max_length=12, default=None, blank=True, null=True)
    category              = models.CharField(max_length=100, default=None, blank=True, null=True)
    timber_class          = models.CharField(max_length=100, default=None, blank=True, null=True)
    specis                = models.CharField(max_length=100, default=None, blank=True, null=True)
    active                = models.IntegerField(default=None, blank=True, null=True)
    lot_no                = models.CharField(max_length=100, default=None, blank=True, null=True)
    sale_price            = models.DecimalField(max_digits=10,decimal_places=2 ,default=None, blank=True, null=True)
    value_grade           = models.CharField(max_length=10, default=None, blank=True, null=True)
    value_price           = models.DecimalField(max_digits=10,decimal_places=2 ,default=None, blank=True, null=True)
    transCost             = models.DecimalField(max_digits=10,decimal_places=2 ,default=None, blank=True, null=True)
    depot                 = models.CharField(max_length=5, default=None, blank=True, null=True)
    doc_date              = models.CharField(max_length=15, default=None, blank=True, null=True)
    gradeInCoupe          = models.CharField(max_length=5, default=None, blank=True, null=True)
    soldGrade             = models.CharField(max_length=5, default=None, blank=True, null=True)
    workingSheetNo        = models.CharField(max_length=100, default=None, blank=True, null=True)
    auctionLotSheetNo     = models.CharField(max_length=100, default=None, blank=True, null=True)
    percentage            = models.DecimalField(max_digits=10,max_length=10, decimal_places=2, default=None, blank=True, null=True)
    yiel_d                = models.DecimalField(max_digits=10,max_length=10, decimal_places=2, default=None, blank=True, null=True)
    logType               = models.CharField(max_length=100, default=None, blank=True, null=True)
    
    def __str__(self):
              # this code shows the outpot in the admin panel
        return '{} {} {} {}  '.format(self.material_no,self.volume,self.user,self.visible_material_no,self.qr_id,self.value_price)
    
class movement(models.Model):
    material_no           = models.IntegerField(primary_key=True)
    movement              = models.IntegerField(default=None, blank=True, null=True)
    old_ref_no            = models.CharField(max_length=20, default=None, blank=True, null=True)
    new_ref_no            = models.CharField(max_length=20, default=None, blank=True, null=True)
    bin                   = models.CharField(max_length=20, default=None, blank=True, null=True)
    time                  = models.TimeField(default=None, blank=True, null=True)
    user                  = models.CharField(max_length=20, default=None, blank=True, null=True)
    document_no           = models.CharField(max_length=20, default=None, blank=True, null=True)
    valueGrade            = models.CharField(max_length=20, default=None, blank=True, null=True)
    
    def __str__(self):
              # this code shows the outpot in the admin panel
        return '{} {} {} {} {} {}  '.format(self.material_no,self.movement,self.document_no,self.user,self.old_ref_no,self.new_ref_no)
