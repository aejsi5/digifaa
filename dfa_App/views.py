from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views import View
from django.db.models import Q
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.core.files import File
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import *
from .models import *
from .permissions import *
from .serializers import *
from .forms import *
from .vehicle import *
from .rule_engine import *
from .errors import Error as CustomError
from .emails import *
from business_rules import run_all
import requests
from datetime import datetime, timedelta
import json
import uuid
import csv
import io

# Create your views here.

@login_required(login_url='login/')
def index(request, *args, **kwargs):
    template_name ="index.html"
    return render(request, template_name)

@login_required(login_url='login/')
def tis(request, *args, **kwargs):
    template_name ="tis.html"
    return render(request, template_name)

@login_required(login_url='login/')
def run_RuleManager(request, pk, *args, **kwargs):
    if request.user.has_perm('dfa_App.view_vehicle_recall') and request.user.has_perm('dfa_App.add_vehicle_recall') and request.user.has_perm('dfa_App.change_vehicle_recall'):
        RM = RuleManager(pk)
        RM.iterate()
        RM.handle_vrs()
        return HttpResponse(status=200)
    return HttpResponse(status=403)

@login_required(login_url='login/')
def update_all(request, *args,**kwargs):
    if request.user.has_perm('dfa_App.view_vehicle_recall') and request.user.has_perm('dfa_App.add_vehicle_recall') and request.user.has_perm('dfa_App.change_vehicle_recall'):
        r = Recall.objects.filter(Recall_STATUS__in=[0,1,2])
        for i in r:
            RM = RuleManager(i.Recall_ID)
            RM.iterate()
            RM.handle_vrs()
        return HttpResponse(status=200)
    return HttpResponse(status=403)

def sample_vehicle_csv(request, *args, **kwargs):
    with open('sample_vehicle.csv', 'w') as f:
        writer = csv.DictReader(f, fieldnames=('Vehicle_VIN', 'Vehicle_PLATE', 'Vehicle_MAKE', 'Vehicle_MODEL', 'Vehicle_TYPE','Vehicle_SERIES','Vehicle_FIRST_REGISTRATION_DATE', 'Vehicle_EXTERNAL_ID','Vehicle_LAST_MILEAGE','Vehicle_DATE_LAST_MILEAGE', 'Vehicle_WARRENTY_PERIOD', 'Vehicle_WARRENTOR', 'Vehicle_WARRENTOR_PREFERED_CHANNEL', 'Vehicle_USER', 'Vehicle_USER_CONTACT', 'Vehicle_USER_CONTACT_PHONE', 'Vehicle_USER_CONTACT_EMAIL'),delimiter=";")
        writer.writeheader()
        return f

def import_csv(csvfile, filetype, save=True, *args, **kwargs):
    e = []
    ext = csvfile.name.split('.')[-1]
    allowed_ext = ['csv', 'CSV']
    if not ext in allowed_ext:
        e.append({
            'row': 0,
            'error': CustomError('UP_001')
        })
        return e
    content = []
    line = 0
    csvf = io.StringIO(csvfile.read().decode('utf-8'))
    if filetype == 'vehicle':
        reader = csv.DictReader(csvf, fieldnames=('Vehicle_VIN', 'Vehicle_PLATE', 'Vehicle_MAKE', 'Vehicle_MODEL', 'Vehicle_TYPE','Vehicle_SERIES','Vehicle_FIRST_REGISTRATION_DATE', 'Vehicle_EXTERNAL_ID','Vehicle_LAST_MILEAGE','Vehicle_DATE_LAST_MILEAGE', 'Vehicle_WARRENTY_PERIOD', 'Vehicle_WARRENTOR', 'Vehicle_WARRENTOR_PREFERED_CHANNEL', 'Vehicle_USER', 'Vehicle_USER_CONTACT', 'Vehicle_USER_CONTACT_PHONE', 'Vehicle_USER_CONTACT_EMAIL'),delimiter=";")
        v = Vehicle.objects.all().update(Vehicel_CURRENT_STATE=0)
        for row in reader:
            if not line == 0:
                content.append(dict(row))
            line += 1
        for idx, i in enumerate(content):
            try:
                if i['Vehicle_VIN']:
                    i['Vehicle_LAST_3_DIGGITS'] = i['Vehicle_VIN'][-3:]
                else:
                    e.append({
                        'row': idx +2,
                        'error': CustomError('UP_003')
                    })
                    continue
                if i['Vehicle_FIRST_REGISTRATION_DATE']:
                    i['Vehicle_FIRST_REGISTRATION_DATE'] = datetime.strptime(i['Vehicle_FIRST_REGISTRATION_DATE'], '%d.%m.%Y')
                else:
                    i['Vehicle_FIRST_REGISTRATION_DATE'] = None
                if i['Vehicle_DATE_LAST_MILEAGE']:
                    i['Vehicle_DATE_LAST_MILEAGE'] = datetime.strptime(i['Vehicle_DATE_LAST_MILEAGE'], '%d.%m.%Y')
                else:
                    i['Vehicle_DATE_LAST_MILEAGE'] = None
                if i['Vehicle_WARRENTY_PERIOD']:
                    i['Vehicle_WARRENTY_END'] = i['Vehicle_FIRST_REGISTRATION_DATE'] + timedelta(days=int(i['Vehicle_WARRENTY_PERIOD']))
                i['Vehicel_CURRENT_STATE'] = 1
                obj, created = Vehicle.objects.update_or_create(
                    Vehicle_VIN=i['Vehicle_VIN'],
                    defaults=i
                )
            except:
                e.append({
                    'row': idx +2,
                    'error': CustomError('UP_008')
                })
                continue
        if save == False:
            v = Vehicle.objects.filter(Vehicel_CURRENT_STATE=0).update(Vehicle_DELETED=True)
        return e
    if filetype == 'workshop':
        reader = csv.DictReader(csvf, fieldnames=('Workshop_EXTERNAL_ID', 'Workshop_NAME', 'Workshop_ADDRESS', 'Workshop_ZIP', 'Workshop_CITY','Workshop_Email','Workshop_PHONE'), delimiter=";")
        for row in reader:
            if not line == 0:
                content.append(dict(row))
            line += 1
        for idx, i in enumerate(content):
            try:
                if not i['Workshop_EXTERNAL_ID']:
                    e.append({
                        'row': idx +2,
                        'error': CustomError('UP_003')
                    })
                    continue
                obj, created = Workshop.objects.update_or_create(
                    Workshop_EXTERNAL_ID=i['Workshop_EXTERNAL_ID'],
                    defaults=i
                )
            except:
                e.append({
                    'row': idx +2,
                    'error': CustomError('UP_008')
                })
                continue
        return e
    if filetype == 'his':
        reader = csv.DictReader(csvf, fieldnames=('Vehicle_VIN', 'Recall_CODE', 'History_EXTERNAL_ID', 'History_DATE', 'History_ODOMETER','Workshop_EXTERNAL_ID','History_DESCRIPTION'), delimiter=";")
        h = History.objects.all().update(History_CURRENT_STATE=0)
        for row in reader:
            if not line == 0:
                content.append(dict(row))
            line += 1
        for idx, i in enumerate(content):
            try:
                if not i['Vehicle_VIN'] or not i['Recall_CODE'] or not i['Workshop_EXTERNAL_ID']:
                    e.append({
                        'row': idx +2,
                        'error': CustomError('UP_004')
                    })
                    continue
                if i['History_DATE']:
                    i['History_DATE'] = datetime.strptime(i['History_DATE'], '%d.%m.%Y')
                else:
                    i['History_DATE'] = None
                if i['History_ODOMETER']:
                    i['History_ODOMETER'] = int(i['History_ODOMETER'])
                else:
                    i['History_ODOMETER'] = None
                i['History_CURRENT_STATE'] = 1
                try:
                    v = Vehicle.objects.get(Vehicle_VIN=i['Vehicle_VIN'])
                except Vehicle.DoesNotExist:
                    e.append({
                        'row': idx +2,
                        'error': CustomError('UP_005')
                    })
                    continue
                try:
                    r = Recall.objects.get(Recall_CODE=i['Recall_CODE'])
                except Recall.DoesNotExist:
                    e.append({
                        'row': idx +2,
                        'error': CustomError('UP_006')
                    })
                    continue
                try:
                    w = Workshop.objects.get(Workshop_EXTERNAL_ID=i['Workshop_EXTERNAL_ID'])
                except Workshop.DoesNotExist:
                    e.append({
                        'row': idx +2,
                        'error': CustomError('UP_007')
                    })
                    continue
                try:
                    h = History.objects.get(Vehicle=v,Recall=r,Workshop=w)
                    h.History_EXTERNAL_ID = i['History_EXTERNAL_ID']
                    h.History_DESCRIPTION = i['History_DESCRIPTION']
                    h.History_ODOMETER = i['History_ODOMETER']
                    h.History_DATE = i['History_DATE']
                    h.History_CURRENT_STATE = i['History_CURRENT_STATE']
                    h.save()
                except History.DoesNotExist:
                    h = History.objects.create(Vehicle=v,Recall=r,Workshop=w,History_EXTERNAL_ID=i['History_EXTERNAL_ID'],History_DESCRIPTION=i['History_DESCRIPTION'],History_ODOMETER=i['History_ODOMETER'],History_DATE=i['History_DATE'],History_CURRENT_STATE=i['History_CURRENT_STATE'])
                    h.save()
                if save == False:
                    hall = History.objects.filter(History_CURRENT_STATE=0).update(History_DELETED=True)
                return e
            except:
                e.append({
                        'row': idx +2,
                        'error': CustomError('UP_005')
                    })
                continue
        return e

class RuleManager():
    def __init__(self, pk, *args, **kwargs):
        self.recall = Recall.objects.get(pk=pk)
        self.rules = self.collect()

    def collect(self, *args, **kwargs):
        constraints = Constraint.objects.filter(Recall=self.recall)
        rules = []
        for i in constraints:
            path = i.Constraint_PATH
            with open(path) as f:
                d = json.load(f)
                for j in d:
                    rules.append(j)
        return rules

    def iterate(self, *args, **kwargs):
        vehicles = Vehicle.objects.filter(Vehicle_DELETED=False)
        for i in vehicles:
            run_all(rule_list=self.rules,
            defined_variables=VehicleVariable(i),
            defined_actions=VehicleActions(i,self.recall),
            stop_on_first_trigger=False)

    def handle_vrs(self, *args, **kwargs):
        vehicles = Vehicle.objects.filter(Vehicle_DELETED=False)
        for i in vehicles:
            try:
                vr = Vehicle_Recall.objects.get(Vehicle=i,Recall=self.recall, VR_STATUS__in=[0,1])
            except Vehicle_Recall.DoesNotExist:
                continue
            try:
                h = History.objects.get(Vehicle=i, Recall= self.recall)
            except History.DoesNotExist:
                continue
            vr.VR_STATUS = 2
            vr.VR_LAST_UPDATE = datetime.today()
            vr.VR_LAST_UPDATE_BY = None
            vr.VR_LAST_UPDATE_WORKSHOP = None
            vr.VR_DATE_COMPLETED = h.History_DATE
            vr.save()

class Administration(View):
    template_name = "master_data.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if request.FILES:
            csv_file = request.FILES['import_file']
            import_type = request.POST['file_type']
            import_method = request.POST.get('Upload_Method', False)
            if import_method == 'save':
                im = True
            else: 
                im = False
            ext = request.FILES['import_file'].name.split('.')[-1]
            allowed_ext = ['csv', 'CSV']
            if not ext in allowed_ext:
                ctx = {}
                ctx['error'] =CustomError('UP_001')
                return render(request, self.template_name, ctx)
            result = import_csv(csv_file, import_type, im)
            send_error_report(settings.EMAIL_HOST_USER, [request.user.email], 'Datenimport wurde durchgeführt', datetime.now(), import_type, result)
        return render(request, self.template_name)

class RecallDetail(View):
    template_name = "recall_detail.html"

    def get(self, request, *args, **kwargs):
        if request.GET:
            q = request.GET
            q = q.dict()
            recall = find_recall_by_querystring(q)
            if recall:
                return self.render_recall_details(request, recall)
            else:
               return self.render_recall_details(request, None)
        return render(request, self.template_name)

    def render_recall_details(self, request, obj, *args, **kwargs):
        if obj == None:
            ctx = {
                'Recall_ID': 'new',
                'rec': RecallForm(),
                'docs': None,
                'doc_form': None,
                'constraints': None
            }
        else:
            ctx = {
                'Recall_ID': obj.Recall_ID,
                'rec': RecallForm(instance=obj),
                'docs': find_docs(obj, mode='all'),
                'doc_form': RecallDocForm(),
                'constraints': find_cons(obj)
            }
        if 'error' in kwargs:
            ctx['error'] = kwargs['error']
        if 'status' in kwargs:
            ctx['status'] = kwargs['status']
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        if request.POST['action'] == 'upload':
            if request.user.has_perm('dfa_App.add_recall_doc'):
                ext = request.FILES['Document_PATH'].name.split('.')[-1]
                allowed_ext = ['pdf']
                r = Recall.objects.get(pk=request.POST['Recall'])
                if not ext in allowed_ext:
                    return self.render_recall_details(request,r, error = CustomError('UP_001'))
                form = RecallDocForm(request.POST, request.FILES)
                if form.is_valid():
                    form.instance.Recall = r
                    form.save()
                    return self.render_recall_details(request, r, status = 'Upload succeed')          

class VehicleSearch(FormView):
    template_name = 'vehicle_search_template.html'
    ctx = {
        'Search_by_VIN': Search_by_VIN(),
        'Search_by_Plate': Search_by_Plate(),
        'header': "Fahrzeugsuche",
    }

    def get(self, request, *args, **kwargs):
        if request.GET:
            q = request.GET
            q = q.dict()
            v = find_vehicle(q)
            if v:
                detail = VehicleDetail()
                return detail.render_vehicle(request, v)               
            else:
                if q['type']:
                    self.ctx['error'] = 'Nicht gefunden'
                return render(request, self.template_name, self.ctx )
        return render(request, self.template_name, self.ctx )

class VehicleSearch_V2(FormView):
    template_name = 'vehicle_search_template_V2.html'
    ctx = {
        'Search_by_VIN': Search_by_VIN_V2(),
        'Search_by_Plate': Search_by_Plate_V2(),
        'header': "Fahrzeugsuche",
    }

    def get(self, request, *args, **kwargs):
        if request.GET:
            q = request.GET
            q = q.dict()
            v = find_vehicle_simple(q)
            if v:
                detail = VehicleDetail()
                return detail.render_vehicle(request, v)               
            else:
                if q['type']:
                    self.ctx['error'] = 'Nicht gefunden'
                return render(request, self.template_name, self.ctx )
        return render(request, self.template_name, self.ctx )

class VehicleDetail(View):
    template_name = 'vehicle_template.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def render_vehicle(self, request, obj, *args, **kwargs):
        ctx = {
            'vehicle': obj,
            'notes': find_notes(obj),
            'history': find_his(obj),
            'recalls': find_recalls(obj),
            'requestor': request.user.username
        }
        return render(request, self.template_name, ctx )

class Note_Api(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, pk, format=None):
        try:
            n = Note.objects.get(pk=pk)
        except Note.DoesNotExist:
            return HttpResponse(status = 404)
        serializer = NoteSerializer(n, many=False)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        rdata_im = request.data
        rdata = rdata_im.copy()
        rdata['User'] = request.user.id
        serializer = NoteSerializer(data=rdata)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            n = Note.objects.get(pk=pk)
        except Note.DoesNotExist:
            return HttpResponse(status = 404)
        self.check_object_permissions(request, n)
        n.delete()
        return HttpResponse(status=200)

class VehicleRecallList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        if request.user.has_perm('dfa_App.view_vehicle') and  request.user.has_perm('dfa_App.view_vehicle_recall'):
            try:
                r = Recall.objects.get(pk=pk)
                vr = Vehicle_Recall.objects.filter(Recall=pk).filter(Q(Vehicle__Vehicle_DELETED=False))
            except Recall.DoesNotExist:
                return HttpResponse(status = 404)
            except Vehicle_Recall.DoesNotExist:
                return HttpResponse(status = 404)
            r_serializer = FullRecallSerializer(r, many=False)
            vr_serializer = VehicleRecallListSerializer(vr, many=True)
            rtn = {
                'recall': r_serializer.data,
                'data': vr_serializer.data
            }
            return Response(rtn)  
        else:
            return Response(status=403)

class Recall_Constraint_Api(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        if request.user.has_perm('dfa_App.view_constraint'):
            try:
                constraint = Constraint.objects.filter(Recall=pk)
                recall = Recall.objects.get(pk=pk)
            except Constraint.DoesNotExist:
                return HttpResponse(status = 404)
            serializer = ConstraintSerializer(constraint, many=True)
            rtn = {
                'Recall': FullRecallSerializer(recall, many=False).data,
                'data': serializer.data
            }
            return Response(rtn)
        return Response(status=403)

    def put(self, request, pk, format=None):
        if request.user.has_perm('dfa_App.change_constraint'):
            rq_im = request.data
            rq = rq_im.copy()
            rdata = rq['data']
            errors = []
            for ind in rdata:
                if ind['Constraint_ID']:
                    try:
                        con = Constraint.objects.get(pk=ind['Constraint_ID'])
                        serializer = ConstraintSerializer(con, data=ind)
                        if serializer.is_valid():
                            inst = serializer.save()
                            run_RuleBuilder(inst.Constraint_ID)
                        else:
                            errors.append({
                                "Constraint_ID": ind['Constraint_ID'],
                                "Error": serializer.errors
                            })   
                    except:
                        errors.append({
                                "Constraint_ID": ind['Constraint_ID'],
                                "Error": serializer.errors
                            })
                        pass
                else:
                    if request.user.has_perm('dfa_App.add_constraint'):
                        try:
                            ind['Recall']= rq['Recall']['Recall_ID']
                            serializer = FullConstraintSerializer(data=ind)
                            if serializer.is_valid():
                                    inst = serializer.save()
                                    run_RuleBuilder(inst.Constraint_ID)
                            else:
                                errors.append({
                                    "Constraint_ID": ind['Constraint_ID'],
                                    "Error": serializer.errors
                                }) 
                        except:
                            errors.append({
                                    "Constraint_ID": ind['Constraint_ID'],
                                    "Error": serializer.errors
                                })
                    else:
                        errors.append({
                                    "Constraint_ID": ind['Constraint_ID'],
                                    "Error": 'Permission denied'
                                })
            return Response(errors, status=200)
        return Response(status=403)

    def post(self, request, pk, format=None):
        if request.user.has_perm('dfa_App.add_constraint'):
            try:
                rec = Recall.objects.get(pk=pk)
                constraint = Constraint.objects.create(Recall=rec)
                constraint.save()
                return Response(status=200)
            except:
                return HttpResponse(status = 404)
        return Response(status=403)

    def delete(self, request, pk, format=None):
        if request.user.has_perm('dfa_App.delete_constraint'):
            con_id = request.GET.get('Constraint_ID', None)
            if con_id is None:
                return HttpResponse(status=400)
            try:
                con_id = int(con_id)
                constraint = Constraint.objects.get(Constraint_ID=con_id)
                constraint.delete()
                return Response(status=200)
            except Constraint.DoesNotExist:
                return HttpResponse(status = 404)
            return Response(status=200)
        return Response(status=403)

class Vehicle_Recall_Api(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        try:
            vr = Vehicle_Recall.objects.get(pk=pk)
        except Vehicle_Recall.DoesNotExist:
            return HttpResponse(status = 404)
        serializer = Basic_Get_Vehicle_RecallSerializer(vr, many=False)
        return Response(serializer.data)

    def patch(self, request, pk):
        try:
            vr = Vehicle_Recall.objects.get(pk=pk)
        except Vehicle_Recall.DoesNotExist:
            return HttpResponse(status = 404)
        rdata = request.data
        rdata_m = rdata.copy()
        rdata_m['VR_LAST_UPDATE'] = datetime.now()
        rdata_m['VR_LAST_UPDATE_BY'] = request.user.id
        rdata_m['VR_LAST_UPDATE_WORKSHOP'] =  request.user.Workshop.Workshop_ID
        if request.user.has_perm('dfa_App.CanChangeAnything'):
            serializer = Full_Vehicle_RecallSerializer(vr, data=rdata_m, partial=True)
        else:
            if vr.VR_DATE_COMPLETED:
                try:
                    request.data.pop("VR_DATE_COMPLETED")
                except:
                    pass
            serializer = Basic_Vehicle_RecallSerializer(vr, data=rdata_m, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
        return HttpResponse(content= serializer.errors, status=400)

class VehicleList(APIView):
    permission_classes = [IsAuthenticated]    

    def get(self, request, format=None):
        if request.user.has_perm('dfa_App.view_vehicle'):
            try:
                vr = Vehicle.objects.all().filter(Vehicle_DELETED=False)
            except Vehicle.DoesNotExist:
                return HttpResponse(status = 404)
            serializer = BasicVehicleSerializer(vr, many=True)
            rtn = {
            'data': serializer.data
            }
            return Response(rtn)  
        else:
            return Response(status=403)

class VehicleAPI(APIView):
    permission_classes = [IsAuthenticated]    

    def get(self, request, pk, format=None):
        if request.user.has_perm('dfa_App.view_vehicle'):
            try:
                vr = Vehicle.objects.filter(Vehicle_DELETED=False).get(pk=pk)
            except Vehicle.DoesNotExist:
                return HttpResponse(status = 404)
            serializer = FullVehicleSerializer(vr, many=False)
            return Response(serializer.data)
        else:
            return Response(status=403)

class RecallListAPI(APIView):
    permission_classes = [IsAuthenticated]    

    def get(self, request, format=None):
        if request.user.has_perm('dfa_App.view_recall'):
            try:
                r = Recall.objects.all()
            except Recall.DoesNotExist:
                return HttpResponse(status = 404)
            serializer = FullRecallSerializer(r, many=True)
            rtn = {
            'data': serializer.data
            }
            return Response(rtn)   
        else:
            return Response(status=403)   

class RecallAPI(APIView):
    permission_classes = [IsAuthenticated]    

    def get(self, request, pk, format=None):
        if request.user.has_perm('dfa_App.view_recall'):
            try:
                r = Recall.objects.get(pk=pk)
            except Recall.DoesNotExist:
                return HttpResponse(status = 404)
            serializer = FullRecallSerializer(r, many=False)
            return Response(serializer.data)   
        else:
            return Response(status=403) 
    
    def put(self, request, pk, *args, **kwargs):
        if request.user.has_perm('dfa_App.change_recall'):
            try:
                r = Recall.objects.get(pk=pk)
            except Recall.DoesNotExist:
                return HttpResponse(status = 404)
            rdata_im = request.data
            rdata = rdata_im.copy()
            rdata['User'] = request.user.id
            serializer = FullRecallSerializer(r,data=rdata)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=403)

    def post(self, request, *args, **kwargs):
        if request.user.has_perm('dfa_App.add_recall'):
            try:
                rdata_im = request.data
                rdata = rdata_im.copy()
                rdata['User'] = request.user.id
                rdata['Recall_ID'] = None
                serializer = FullRecallSerializer(data=rdata)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return HttpResponse(status = 404)
        return Response(status=403)
   
class WorkshopList(APIView):
    permission_classes = [IsAuthenticated]    

    def get(self, request, format=None):
        if request.user.has_perm('dfa_App.view_workshop'):
            try:
                w = Workshop.objects.all().filter(Workshop_DELETED=False)
            except Workshop.DoesNotExist:
                return HttpResponse(status = 404)
            serializer = BasicWorkshopSerializer(w, many=True)
            rtn = {
            'data': serializer.data
            }
            return Response(rtn)  
        else:
            return Response(status=403)

class WorkshopAPI(APIView):
    permission_classes = [IsAuthenticated]    

    def get(self, request, pk, format=None):
        if request.user.has_perm('dfa_App.view_workshop'):
            try:
                w = Workshop.objects.filter(Workshop_DELETED=False).get(pk=pk)
            except Workshop.DoesNotExist:
                return HttpResponse(status = 404)
            serializer = FullWorkshopSerializer(w, many=False)
            return Response(serializer.data)
        else:
            return Response(status=403)

class RecallDocsListAPI(APIView):
    permission_classes = [IsAuthenticated]  
    
    def get(self, request, format=None):
        if request.user.has_perm('dfa_App.view_recall_doc'):
            try:
                doc = Recall_Doc.objects.filter(Document_PUBLISH_DATE__lte = datetime.today())
            except Recall_Doc.DoesNotExist:
                return HttpResponse(status = 404)
            serializer = FullRecallDocListSerializer(doc, many=True)
            rtn = {
            'data': serializer.data
            }
            return Response(rtn) 
        else:
            return Response(status=403)

class RecallDocsAPI(APIView):
    permission_classes = [IsAuthenticated]  
    parser_classes = (MultiPartParser, FormParser,)


    def get(self, request, pk, format=None):
        if request.user.has_perm('dfa_App.view_recall_doc'):
            try:
                doc = Recall_Doc.objects.get(Document_ID=pk)
            except Recall_Doc.DoesNotExist:
                return HttpResponse(status = 404)
            serializer = FullRecallDocSerializer(doc, many=False)
            return Response(serializer.data)
        else:
            return Response(status=403)
        
    def delete(self, request, pk, format=None):
        if request.user.has_perm('dfa_App.delete_recall_doc'):
            try:
                doc = Recall_Doc.objects.get(pk=pk)
            except Recall_Doc.DoesNotExist:
                return HttpResponse(status = 404)
            doc.delete()
            return HttpResponse(status=200)
    

