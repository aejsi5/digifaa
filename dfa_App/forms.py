from django import forms
from django.utils.translation import gettext_lazy as _
from .models import User
from .models import *

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, request, *args, **kwargs):
        # simply do not pass 'request' to the parent
        super().__init__(*args, **kwargs)

class Search_by_VIN_V2(forms.Form):
    vin = forms.CharField(
        max_length=17, 
        required= True, 
        label='Fahrgestellnummer',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'W0L000051T2123456',
                'class': 'form-control'
            }
        ))

class Search_by_Plate_V2(forms.Form):
    plate = forms.CharField(
        max_length=9,
        required= True, 
        label='Kennzeichen',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'BN-P1234E',
                'class': 'form-control'
            }
        ))

class Search_by_VIN(forms.Form):
    vin = forms.CharField(
        max_length=17, 
        required= True, 
        label='Fahrgestellnummer',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'W0L000051T2123456',
                'class': 'form-control'
            }
        ))
    first_registration_date = forms.DateField(
        required= True,
        label='Erstzulassungsdatum',
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'placeholder': '01.01.2020',
                'class': 'form-control'
            }
        ))

class Search_by_Plate(forms.Form):
    plate = forms.CharField(
        max_length=9,
        required= True, 
        label='Kennzeichen',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'BN-P1234E',
                'class': 'form-control'
            }
        ))
    last_3_diggits= forms.CharField(
        max_length=3,
        required= True, 
        label='Letzte 3 Ziffern der Fahrgestellnummer',
        widget=forms.TextInput(
            attrs={
                'placeholder': '456',
                'class': 'form-control'
            }
        ))

class RecallForm(forms.ModelForm):
    class Meta:
        model = Recall
        fields = ('Recall_CODE', 'Recall_NAME', 'Recall_DESCRIPTION', 'Recall_START_DATE', 'Recall_PLANNED_COMPLETATION_DATE', 'Recall_DATE_COMPLETED', 'Recall_STATUS')
        labels = {
            'Recall_CODE': _('Code'),
            'Recall_NAME': _('Name'),
            'Recall_DESCRIPTION': _('Beschreibung'),
            'Recall_START_DATE': _('Startdatum'),
            'Recall_PLANNED_COMPLETATION_DATE': _('Abschlussdatum Soll'),
            'Recall_DATE_COMPLETED': _('Abschlussdatum Ist'),
            'Recall_STATUS': _('Status')
        }
        widgets = {
            'Recall_CODE': forms.TextInput(attrs={'maxlength': 10, 'id': 'id_Recall_CODE', 'required':True, 'class': 'form-control margin-btm-05'}),
            'Recall_NAME': forms.TextInput(attrs={'maxlength': 30, 'id': 'id_Recall_NAME', 'required':True, 'class': 'form-control margin-btm-05'}),
            'Recall_DESCRIPTION': forms.Textarea(attrs={'maxlength': 150, 'rows': 2, 'id': 'id_Recall_DESCRIPTION', 'required':True, 'class': 'form-control margin-btm-05'}),
            'Recall_START_DATE': forms.DateInput(format=('%Y-%m-%d'), attrs={'id': 'id_Recall_START_DATE', 'class': 'form-control', 'required':True, 'type': 'date'}),
            'Recall_PLANNED_COMPLETATION_DATE': forms.DateInput(format=('%Y-%m-%d'),attrs={'id': 'id_Recall_PLANNED_COMPLETATION_DATE','required':True, 'class': 'form-control margin-btm-05', 'type': 'date'}),
            'Recall_DATE_COMPLETED': forms.DateInput(format=('%Y-%m-%d'),attrs={'id': 'id_Recall_DATE_COMPLETED', 'class': 'form-control margin-btm-05', 'type': 'date'}),
            'Recall_STATUS': forms.Select(attrs={'id': 'id_Recall_STATUS','required':True, 'class': 'form-control margin-btm-05'}),
        }

class RecallDocForm(forms.ModelForm):
    class Meta:
        model = Recall_Doc
        fields = ('Document_CLASS', 'Document_PATH','Document_PUBLISH_DATE')

        labels = {
            'Document_CLASS': _('Dokumententyp'),
            'Document_PATH': _('Datei'),
            'Document_PUBLISH_DATE': _('Veröffentlichungsdatum'),
        }

        widgets = {
            'Document_CLASS': forms.Select(attrs={'id': 'id_Recall_Doc_Class', 'required':True, 'class': 'form-control margin-btm-05'}),
            'Document_PATH': forms.FileInput(attrs={'id': 'id_Recall_Upload_Path', 'required':True, 'class': 'form-control margin-btm-05'}),
            'Document_PUBLISH_DATE': forms.DateInput(format=('%Y-%m-%d'), attrs={'id': 'id_Recall_Doc_Publish_Date', 'class': 'form-control margin-btm-05', 'required':True, 'type': 'date'}),
        }
        




