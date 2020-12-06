from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
import datetime
from django.conf import settings
import os
import uuid


# Create your models here.
class Workshop(models.Model):
    Workshop_ID = models.AutoField('ID', primary_key= True)
    Workshop_EXTERNAL_ID = models.CharField('externe ID', max_length=10)
    Workshop_NAME = models.CharField('Name', max_length=50)
    Workshop_ADDRESS = models.CharField('Adresse', max_length=70)
    Workshop_ZIP = models.CharField('PLZ', max_length=10)
    Workshop_CITY = models.CharField('Stadt', max_length=50)
    Workshop_Email = models.EmailField('Email', blank=True)
    Workshop_PHONE = models.CharField('Telefon', max_length=30, blank=True)
    Workshop_DELETED = models.BooleanField('Gelöscht', default=False)
    
    def __str__(self):
        return str(self.Workshop_NAME)
    
    class Meta:
        app_label ="dfa_App"

class User(AbstractUser):
    Workshop = models.ForeignKey(Workshop,on_delete=models.CASCADE, null = True)
    pass

class Vehicle(models.Model):
    Vehicle_ID = models.AutoField('ID', primary_key= True)
    Vehicle_VIN = models.CharField('FIN', max_length=30)
    Vehicle_PLATE = models.CharField('Kennzeichen', max_length=10, blank=True, null = True)
    Vehicle_MAKE = models.CharField('Hersteller', max_length=30, blank=True, null = True)
    Vehicle_MODEL = models.CharField('Modell', max_length=30, blank=True, null = True)
    Vehicle_TYPE = models.CharField('Typ', max_length=60, blank=True, null = True)
    Vehicle_SERIES = models.CharField('Baureihe', max_length=30, blank=True, null = True)
    Vehicle_FIRST_REGISTRATION_DATE = models.DateField('Erstzulassungsdatum', blank=True, null = True)
    Vehicle_LAST_3_DIGGITS = models.CharField('Letzte 3 Ziffern der FIN', max_length=3)
    Vehicle_EXTERNAL_ID= models.CharField('Flottennummer', max_length=15, blank=True, null=True)
    Vehicle_LAST_MILEAGE= models.IntegerField('Letzter Kilometerstand', blank=True, null=True)
    Vehicle_DATE_LAST_MILEAGE = models.DateField('Datum letzter Kilometerstand', blank=True, null=True)
    Vehicle_WARRENTY_PERIOD = models.IntegerField('Gewährleistungszeitraum in Tagen ab Erstzulassung', blank= True, null=True)
    Vehicle_WARRENTY_END = models.DateField('Gewährleistungsende', blank=True, null=True)
    Vehicle_WARRENTOR = models.CharField('Gewährleistungsgeber', max_length=30, blank=True, null=True)
    Vehicle_WARRENTOR_PREFERED_CHANNEL = models.CharField('Bevorzugter Kommunikationskanal',max_length=50, blank=True, null=True)
    Vehicle_USER = models.CharField('Fahrzeugnutzer',max_length=30, blank=True, null=True)
    Vehicle_USER_CONTACT = models.CharField('Fahrzeugnutzer Ansprechpartner',max_length=30, blank=True, null=True)
    Vehicle_USER_CONTACT_PHONE = models.CharField('Fahrzeugnutzer Ansprechpartner Telefon',max_length=30, blank=True, null=True)
    Vehicle_USER_CONTACT_EMAIL = models.EmailField('Fahrzeugnutzer Ansprechpartner Email', blank=True, null=True)
    Vehicel_CURRENT = 1
    Vehicle_OUTDATED = 0
    Vehicle_CHOICES = (
        (Vehicel_CURRENT, 'aktuell'),
        (Vehicle_OUTDATED, 'nicht aktuell')
    )
    Vehicel_CURRENT_STATE = models.SmallIntegerField('Aktueller Importstatus', choices=Vehicle_CHOICES, default=Vehicel_CURRENT)
    Vehicle_DELETED = models.BooleanField('Gelöscht',default=False)

    def __str__(self):
        return str(self.Vehicle_VIN)
    
    class Meta:
        app_label ="dfa_App"

class Note(models.Model):
    Note_ID = models.AutoField('ID', primary_key= True)
    Vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Note_TEXT = models.CharField('Bemerkung',max_length=500)
    Note_DATE = models.DateTimeField('Zeitpunkt', auto_now_add=True)
    Note_ODOMETER = models.IntegerField('Kilometerstand', blank=True, null=True)

    def __str__(self):
        return str(self.Note_ID)

    class Meta:
        app_label ="dfa_App"
        ordering = ['Note_DATE']

class Recall(models.Model):
    Recall_ID = models.AutoField('ID', primary_key= True)
    Recall_CODE = models.CharField('Rückruf-Code',max_length=500, unique= True)
    Recall_NAME = models.CharField('Name',max_length=500)
    Recall_DESCRIPTION = models.CharField('Beschreibung',max_length=500)
    Recall_START_DATE = models.DateField('Startdatum', blank = True)
    Recall_PLANNED_COMPLETATION_DATE = models.DateField('Geplantes Fertigstellungsdatum', blank = True)
    Recall_CREATED = 0
    Recall_PLANNING = 1
    Recall_ONGOING = 2
    Recall_CANCELED = 4
    Recall_COMPLETED = 3
    Recall_CHOICES = (
        (Recall_CREATED, 'Erstellt'),
        (Recall_PLANNING, 'In Planung'),
        (Recall_ONGOING, 'In Bearbeitung'),
        (Recall_COMPLETED, 'Abgeschlossen'),
        (Recall_CANCELED, 'Abgebrochen')
    )
    Recall_STATUS = models.SmallIntegerField('Status', choices=Recall_CHOICES, default=Recall_CREATED)
    Recall_DATE_COMPLETED = models.DateField('Tatsächliches Fertigstellungsdatum', blank = True, null = True)

    def __str__(self):
        return str(self.Recall_CODE)

    class Meta:
        app_label ="dfa_App"

class Constraint(models.Model):
    Constraint_ID = models.AutoField('ID', primary_key= True)
    Constraint_equal = 0
    Constraint_unequal = 1
    Constraint_contains = 2
    Constraint_uncontains = 3
    Constraint_begins = 4
    Constraint_unbegins = 5
    Constraint_ends = 6
    Constraint_unends = 7
    Constraint_CHOICES = (
        (Constraint_equal, 'gleich'),
        (Constraint_unequal, 'nicht gleich'),
        (Constraint_contains, 'enthält'),
        (Constraint_uncontains, 'enthält nicht'),
        (Constraint_begins, 'beginnt mit'),
        (Constraint_unbegins, 'beginnt nicht mit'),
        (Constraint_ends, 'endet mit'),
        (Constraint_unends, 'endet nicht mit'),
    )
    Recall = models.ForeignKey(Recall, on_delete=models.CASCADE)
    Constraint_Vehicle_VIN_FROM = models.CharField('FIN von', max_length=30, blank=True, null=True)
    Constraint_Vehicle_VIN_TO = models.CharField('FIN bis', max_length=30, blank=True, null=True)
    Constraint_Vehicle_EXTERNAL_ID_FROM= models.CharField('Flottennummer von', max_length=15, blank=True, null=True)
    Constraint_Vehicle_EXTERNAL_ID_TO= models.CharField('Flottennummer bis', max_length=15, blank=True, null=True)
    Constraint_Vehicle_MAKE_CHOICES = models.SmallIntegerField('Beschränkung', choices=Constraint_CHOICES,default=Constraint_equal)
    Constraint_Vehicle_MAKE = models.CharField('Hersteller', max_length=30, blank=True, null = True)
    Constraint_Vehicle_MODEL_CHOICES = models.SmallIntegerField('Beschränkung', choices=Constraint_CHOICES,default=Constraint_equal)
    Constraint_Vehicle_MODEL = models.CharField('Modell', max_length=30, blank=True, null = True)
    Constraint_Vehicle_TYPE_CHOICES = models.SmallIntegerField('Beschränkung', choices=Constraint_CHOICES,default=Constraint_equal)
    Constraint_Vehicle_TYPE = models.CharField('Typ', max_length=60, blank=True, null = True)
    Constraint_Vehicle_SERIES_CHOICES = models.SmallIntegerField('Beschränkung', choices=Constraint_CHOICES,default=Constraint_equal)
    Constraint_Vehicle_SERIES = models.CharField('Baureihe', max_length=30, blank=True, null = True)
    Constraint_Vehicle_FIRST_REGISTRATION_DATE_FROM = models.DateField('Erstzulassungsdatum von', blank=True, null = True)
    Constraint_Vehicle_FIRST_REGISTRATION_DATE_TO = models.DateField('Erstzulassungsdatum bis', blank=True, null = True)
    Constraint_Vehicle_MILEAGE_FROM= models.IntegerField('Kilometerstand von', blank=True, null=True)
    Constraint_Vehicle_MILEAGE_TO= models.IntegerField('Kilometerstand bis', blank=True, null=True)
    Constraint_Vehicle_USER_CHOICES = models.SmallIntegerField('Beschränkung', choices=Constraint_CHOICES,default=Constraint_equal)
    Constraint_Vehicle_USER = models.CharField('Fahrzeugnutzer',max_length=30, blank=True, null=True)
    Constraint_PATH = models.FilePathField(path=os.path.join(settings.MEDIA_ROOT, 'constraints/'),default=None,null=True, blank=True)

    class Meta:
        app_label ="dfa_App"

def update_filename(instance, filename):
        ext = filename.split('.')[-1]
        path = os.path.join(settings.MEDIA_ROOT, 'uploads/documents/')
        basename = instance.get_Document_CLASS_display()
        random_id = str(uuid.uuid4())
        suffix = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        new_name= "_".join([basename, random_id, suffix]) + '.' + ext
        print(new_name)
        return os.path.join(path,new_name)

class Recall_Doc(models.Model):
    Document_ID = models.AutoField('ID', primary_key= True)
    Recall = models.ForeignKey(Recall, on_delete=models.CASCADE)
    Document_MANUAL = 0
    Document_TECHNICAL_INFORMATION = 1
    Document_LETTER = 2
    Document_OTHER = 3
    Document_CHOICES = (
        (Document_MANUAL, 'Anleitung'),
        (Document_TECHNICAL_INFORMATION, 'Technische Information'),
        (Document_LETTER, 'Anschreiben'),
        (Document_OTHER, 'Sonstiges'),
    )
    Document_CLASS = models.SmallIntegerField('Dokumententyp', choices=Document_CHOICES,default=Document_OTHER)
    Document_PATH = models.FileField('Upload Pfad', upload_to=update_filename, max_length=500, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    Document_UPLOAD_DATE = models.DateField('Uploaddatum', auto_now_add=True)
    Document_PUBLISH_DATE = models.DateField('Veröffentlichungsdatum', blank=True, null=True)

    def __str__(self):
        return str(self.Document_PATH)

    class Meta:
        app_label ="dfa_App"

class Vehicle_Recall(models.Model):
    Vehicle_Recall_ID = models.AutoField('ID', primary_key=True)
    Vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    Recall  = models.ForeignKey(Recall, on_delete=models.CASCADE)
    STATUS_PENDING = 0
    STATUS_PRESET = 1
    STATUS_COMPLETED = 2
    STATUS_CHOICES = (
        (STATUS_PENDING, 'Offen'),
        (STATUS_PRESET, 'Vorbelegt'),
        (STATUS_COMPLETED, 'Abgeschlossen')
    )
    VR_STATUS = models.SmallIntegerField('Status',choices=STATUS_CHOICES, default=STATUS_PENDING)
    VR_DATE_CREATED = models.DateField('Anlagedatum', auto_now_add=True)
    VR_LAST_UPDATE = models.DateTimeField('Letze Änderung', blank = True, null = True)
    VR_LAST_UPDATE_BY = models.ForeignKey(User,on_delete=models.CASCADE, blank =True, null =True)
    VR_LAST_UPDATE_WORKSHOP = models.ForeignKey(Workshop,on_delete=models.CASCADE, null = True, blank = True)
    VR_DATE_COMPLETED = models.DateField('Fertigstellungsdatum', blank=True, null=True)

    class Meta:
        app_label ="dfa_App"
        permissions = [
            ("CanChangeAnything", "Can patch all fields"),
        ]

class History(models.Model):
    History_ID = models.AutoField('ID', primary_key= True)
    History_EXTERNAL_ID = models.CharField('Externe ID',max_length=500, blank=True, null=True)
    History_DESCRIPTION = models.CharField('Beschreibung',max_length=500, blank=True, null=True)
    Workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    Vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    Recall = models.ForeignKey(Recall, on_delete=models.CASCADE)
    History_ODOMETER = models.IntegerField('Kilometerstand', blank=True, null=True)
    History_DATE = models.DateField('Datum', blank=True, null=True)
    History_CURRENT = 1
    History_OUTDATED = 0
    History_CHOICES = (
        (History_CURRENT, 'aktuell'),
        (History_OUTDATED, 'nicht aktuell')
    )
    History_CURRENT_STATE = models.SmallIntegerField('Aktueller Importstatus', choices=History_CHOICES, default=History_CURRENT)
    History_DELETED = models.BooleanField('Gelöscht',default=False)


    def __str__(self):
        return str(self.History_ID)

    class Meta:
        app_label ="dfa_App"
