from .models import *
import datetime
from django.db.models import Q

def find_vehicle(q):
    if q["type"] == "by_vin":
        vin = q["vin"]
        frd = q["first_registration_date"]
        if not vin or not frd:
            return None
        try:
            v = Vehicle.objects.get(Vehicle_VIN=vin, Vehicle_FIRST_REGISTRATION_DATE=frd)
            return v
        except Vehicle.DoesNotExist:
            return None
    if q["type"] == "by_plate":
        plate = q["plate"]
        l3d = q["last_3_diggits"]
        if not plate or not l3d:
            return None
        try:
            v = Vehicle.objects.get(Vehicle_PLATE=plate, Vehicle_LAST_3_DIGGITS=l3d)
            return v
        except Vehicle.DoesNotExist:
            return None
        
def find_notes(v):
    try:
        notes = Note.objects.filter(Vehicle=v).order_by("Note_DATE")
        note_data = []
        for note in notes:
            arr_note = [
                note.Note_ID,
                NonetoStr(datestr(note.Note_DATE)),
                NonetoStr(note.Note_ODOMETER),
                note.Note_TEXT,
                note.User.username
            ]
            note_data.append(arr_note)
        return note_data
    except:
        return None

def find_his(v):
    try:
        his = History.objects.filter(Vehicle=v).order_by("-History_DATE")
        his_data = []
        for pos in his:
            arr_his = [
                pos.History_ID,
                pos.Recall.Recall_CODE,
                NonetoStr(datestr(pos.History_DATE)),
                NonetoStr(pos.History_ODOMETER),
                NonetoStr(pos.Workshop.Workshop_NAME) + ", " + NonetoStr(pos.Workshop.Workshop_CITY),
                pos.History_DESCRIPTION,
            ]
            his_data.append(arr_his)
        return his_data
    except:
        return None

def find_recalls(v):
    try:
        q1 = Q(Recall_STATUS=1)
        q2 = Q(Recall_STATUS=2)
        q3 = Q(Recall_START_DATE__lte=datetime.datetime.today())
        r = Recall.objects.filter(q3 & (q1 | q2))
        recalls = Vehicle_Recall.objects.filter(Vehicle=v, Recall__in = r).order_by("-VR_DATE_CREATED")
        recall_data = []
        for recall in recalls:
            arr_recall = { 
                        "Recall_Data": {
                            "Recall_ID": recall.Recall.Recall_ID,
                            "Recall_CODE": recall.Recall.Recall_CODE,
                            "Recall_NAME": recall.Recall.Recall_NAME,
                            "Recall_DESCRIPTION": recall.Recall.Recall_DESCRIPTION,
                            "Recall_START_DATE": datestr(recall.Recall.Recall_START_DATE),
                            "Recall_DOCS": find_docs(recall.Recall)
                        },
                        "Vehicle_Recall": {
                            "Vehicle_Recall_ID": recall.Vehicle_Recall_ID,
                            "Status": recall.VR_STATUS,
                            "Creation_Date": datestr(recall.VR_DATE_CREATED),
                            "Update": {
                                "Date_Update": datestr(recall.VR_LAST_UPDATE),
                                "Workshop": find_workshop(recall.VR_LAST_UPDATE_WORKSHOP)
                            },
                            "Completion_Date": datestr(recall.VR_DATE_COMPLETED)
                        }
                    }
            recall_data.append(arr_recall)
        return recall_data
    except:
        return None

def find_docs(r, *args, **kwargs):
    try:
        if 'mode' in kwargs:
            if kwargs['mode']=='all':
                docs = Recall_Doc.objects.filter(Recall=r)
        else:
            docs = Recall_Doc.objects.filter(Recall=r, Document_PUBLISH_DATE__lte = datetime.datetime.today())
        docs_data = []
        for doc in docs:
            media_url = os.path.basename(doc.Document_PATH.file.name)
            arr_doc = {
                "Document_ID": doc.Document_ID,
                "Document_CLASS": doc.Document_CLASS,
                "Document_PATH": media_url,
                "Document_PUBLISH_DATE": NonetoStr(doc.Document_PUBLISH_DATE),
                "Document_UPLOAD_DATE": doc.Document_UPLOAD_DATE
            }
            docs_data.append(arr_doc)
        return docs_data
    except:
        pass

def find_cons(r):
    try:
        cons = Constraint.objects.filter(Recall=r)
        cons_data = []
        for con in cons:
            arr_con = {
                "Constraint_ID": con.Constraint_ID,
                "Constraint_Vehicle_VIN_FROM": NonetoStr(con.Constraint_Vehicle_VIN_FROM),
                "Constraint_Vehicle_VIN_TO": NonetoStr(con.Constraint_Vehicle_VIN_TO),
                "Constraint_Vehicle_EXTERNAL_ID_FROM": NonetoStr(con.Constraint_Vehicle_EXTERNAL_ID_FROM),
                "Constraint_Vehicle_EXTERNAL_ID_TO": NonetoStr(con.Constraint_Vehicle_EXTERNAL_ID_TO),
                "Constraint_Vehicle_MAKE_CHOICES": con.Constraint_Vehicle_MAKE_CHOICES,
                "Constraint_Vehicle_MAKE": NonetoStr(con.Constraint_Vehicle_MAKE),
                "Constraint_Vehicle_MODEL_CHOICES":con.Constraint_Vehicle_MODEL_CHOICES,
                "Constraint_Vehicle_MODEL": NonetoStr(con.Constraint_Vehicle_MODEL),
                "Constraint_Vehicle_TYPE_CHOICES": con.Constraint_Vehicle_TYPE_CHOICES,
                "Constraint_Vehicle_TYPE": NonetoStr(con.Constraint_Vehicle_TYPE_CHOICES),
                "Constraint_Vehicle_SERIES_CHOICES": con.Constraint_Vehicle_SERIES_CHOICES,
                "Constraint_Vehicle_SERIES": NonetoStr(con.Constraint_Vehicle_SERIES),
                "Constraint_Vehicle_FIRST_REGISTRATION_DATE_FROM": datestr2(con.Constraint_Vehicle_FIRST_REGISTRATION_DATE_FROM),
                "Constraint_Vehicle_FIRST_REGISTRATION_DATE_TO":datestr2(con.Constraint_Vehicle_FIRST_REGISTRATION_DATE_TO),
                "Constraint_Vehicle_MILEAGE_FROM":NonetoStr(con.Constraint_Vehicle_MILEAGE_FROM),
                "Constraint_Vehicle_MILEAGE_TO":NonetoStr(con.Constraint_Vehicle_MILEAGE_TO),
                "Constraint_Vehicle_USER_CHOICES":con.Constraint_Vehicle_USER_CHOICES,
                "Constraint_Vehicle_USER": NonetoStr(con.Constraint_Vehicle_USER),
                "Constraint_PATH": con.Constraint_PATH
            }
            cons_data.append(arr_con)
        return cons_data
    except:
        return None

def find_workshop(r):
    try:
        ws = Workshop.objects.get(pk=r.Workshop_ID)
        ws_obj = {
            "Workshop_ID": ws.Workshop_ID,
            "Workshop_EXTERNAL_ID": ws.Workshop_EXTERNAL_ID,
            "Workshop_NAME": ws.Workshop_NAME,
            "Workshop_ADDRESS": ws.Workshop_ADDRESS,
            "Workshop_ZIP": ws.Workshop_ZIP,
            "Workshop_CITY": ws.Workshop_CITY,
            "Workshop_Email": ws.Workshop_Email,
            "Workshop_PHONE": ws.Workshop_PHONE
        }
        return ws_obj
    except:
        return None

def datestr(dateobj):
    if dateobj:
        return dateobj.strftime("%d.%m.%Y")
    else:
        return None

def datestr2(dateobj):
    if dateobj:
        return dateobj.strftime("%Y-%m-%d")
    else:
        return None

def NonetoStr(inp):
    if inp is None:
        return ""
    else:
        return inp

def find_recall_by_querystring(q):
    if q["recallid"]:
        rid = q["recallid"]
        if rid == 'new':
            return None
        try:
            r = Recall.objects.get(pk=rid)
            return r
        except Recall.DoesNotExist:
            return None
    else:
        return None
