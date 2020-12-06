from business_rules.variables import *
from business_rules.actions import *
from business_rules.engine import *
from business_rules import run_all
from .models import *
from django.core.serializers.json import DjangoJSONEncoder
import datetime
import json
import uuid

def test_business_rules():
    print(business_rules.__version__)


def run_business():
    beispiel = Vehicle.objects.get(pk=1)
    rules = [
        {
            "conditions": {
                "all": [
                    {
                        "name": "first_registration_date_from",
                        "operator": "greater_than_or_equal_to",
                        "value": "2017-08-01"
                    },
                ]
            },
            "actions": [
                {
                    "name": "print_result",
                },
            ],
        }
    ]
    run_all(rule_list=rules,
            defined_variables=VehicleVariable(beispiel),
            defined_actions=VehicleActions(beispiel),
            stop_on_first_trigger=True
           )

def run_RuleBuilder(con_id):
    con = Constraint.objects.get(pk=con_id)
    myRules = RuleBuilder(con)
    with open(os.path.join(settings.MEDIA_ROOT, 'constraints/', myRules.json_file_name + '.json'), "w", encoding='utf-8') as f:
        f.write(myRules.json_data)
    con.Constraint_PATH = os.path.join(settings.MEDIA_ROOT, 'constraints/', myRules.json_file_name + '.json')
    con.save()

class RuleBuilder():
    def __init__(self, constraint):
        self.Constraint = constraint
        self.Rules = []
        self.build_rules()
        self.create_json()

    def print_rules(self, *args, **kwargs):
        print(self.Rules)

    def operator_translator(self, op, *args, **kwargs):
        if op == 0:
            return 'equal_to'
        if op == 2:
            return 'contains'
        if op == 4:
            return 'starts_with'
        if op == 6:
            return 'ends_with'

    def a_rule(self, val, *args, **kwargs):
        if len(self.Rules)==0:
            self.Rules.append({
                "conditions": {
                    "all": []
                },
                "actions": [
                    {
                        "name": "vehicle_recall",
                    },
                ]
            })
        for j in range(len(self.Rules)):
            for i in val:
                self.Rules[j]['conditions']['all'].append(i)

    def special_rule(self, val, *args, **kwargs):
        for rule in val:
            self.Rules.append({
                "conditions": {
                    "all": [rule]
                },
                "actions": [
                    {
                        "name": "vehicle_recall",
                    },
                ]
            })

    def build_rules(self, *args, **kwargs):
        if self.Constraint.Constraint_Vehicle_VIN_FROM:
            self.special_rule(self.fin(self))
        if self.Constraint.Constraint_Vehicle_EXTERNAL_ID_FROM:
            self.special_rule(self.fleet_number(self))
        if self.Constraint.Constraint_Vehicle_MAKE:
            self.a_rule(self.make(self.Constraint.Constraint_Vehicle_MAKE_CHOICES))
        if self.Constraint.Constraint_Vehicle_SERIES:
            self.a_rule(self.series(self.Constraint.Constraint_Vehicle_SERIES_CHOICES)) 
        if self.Constraint.Constraint_Vehicle_MODEL:
            self.a_rule(self.model(self.Constraint.Constraint_Vehicle_MODEL_CHOICES))
        if self.Constraint.Constraint_Vehicle_TYPE:
            self.a_rule(self.vtype(self.Constraint.Constraint_Vehicle_TYPE_CHOICES)) 
        if self.Constraint.Constraint_Vehicle_USER:
            self.a_rule(self.vuser(self.Constraint.Constraint_Vehicle_USER_CHOICES))
        if self.Constraint.Constraint_Vehicle_MILEAGE_FROM or self.Constraint.Constraint_Vehicle_MILEAGE_TO:
            self.a_rule(self.odometer(self))
        if self.Constraint.Constraint_Vehicle_FIRST_REGISTRATION_DATE_FROM or self.Constraint.Constraint_Vehicle_FIRST_REGISTRATION_DATE_TO:
            self.a_rule(self.reg(self))

    def create_json(self, *args, **kwargs):
        self.json_data = json.dumps(self.Rules, sort_keys=True, indent=1, cls=DjangoJSONEncoder)
        basename = 'constraint'
        random_id = str(uuid.uuid4())
        suffix = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.json_file_name = "_".join([basename, random_id, suffix])

    def fin(self, *args, **kwargs):
        if self.Constraint.Constraint_Vehicle_VIN_TO:
            fin_arr = []
            body = self.Constraint.Constraint_Vehicle_VIN_FROM[:8]
            start = int(self.Constraint.Constraint_Vehicle_VIN_FROM[-6:])
            end = int(self.Constraint.Constraint_Vehicle_VIN_TO[-6:])
            for i in range(start, end + 1):
                actual = str(i).zfill(6)
                rule = {
                    "name": "fin",
                    "operator": "equal_to",
                    "value": body + actual
                }
                fin_arr.append(rule)
            return fin_arr
        return [
                {
                    "name": "fin",
                    "operator": "equal_to",
                    "value": self.Constraint.Constraint_Vehicle_VIN_FROM
                }
            ]
    
    def fleet_number(self, *args, **kwargs):
        #has to be substituted if the customers fleet_number has a different format than default
        if self.Constraint.Constraint_Vehicle_EXTERNAL_ID_TO:
            fin_arr = []
            start = int(self.Constraint.Constraint_Vehicle_EXTERNAL_ID_FROM)
            end = int(self.Constraint.Constraint_Vehicle_EXTERNAL_ID_TO)
            for i in range(start, end+1):
                actual = str(i)
                rule = {
                    "name": "fleet",
                    "operator": "equal_to",
                    "value": actual
                }
                fin_arr.append(rule)
            return fin_arr
        return [{
                    "name": "fleet",
                    "operator": "equal_to",
                    "value": self.Constraint.Constraint_Vehicle_EXTERNAL_ID_FROM
                }]

    def make(self, operator, *args, **kwargs):
        return [{
                    "name": "make",
                    "operator": self.operator_translator(operator),
                    "value": self.Constraint.Constraint_Vehicle_MAKE
                }]

    def series(self, operator, *args, **kwargs):
        return [{
                    "name": "series",
                    "operator": self.operator_translator(operator),
                    "value": self.Constraint.Constraint_Vehicle_SERIES
                }]

    def model(self, operator, *args, **kwargs):
        return [{
                    "name": "model",
                    "operator": self.operator_translator(operator),
                    "value": self.Constraint.Constraint_Vehicle_MODEL
                }]

    def vtype(self, operator, *args, **kwargs):
        return [{
                    "name": "vtype",
                    "operator": self.operator_translator(operator),
                    "value": self.Constraint.Constraint_Vehicle_TYPE
                }]

    def vuser(self, operator, *args, **kwargs):
        return [{
                    "name": "vuser",
                    "operator": self.operator_translator(operator),
                    "value": self.Constraint.Constraint_Vehicle_USER
                }]

    def odometer(self, *args, **kwargs):
        if self.Constraint.Constraint_Vehicle_MILEAGE_FROM and self.Constraint.Constraint_Vehicle_MILEAGE_TO:
            rule_arr = [
                {
                    "name": "odometer_from",
                    "operator": "greater_than_or_equal_to",
                    "value": self.Constraint.Constraint_Vehicle_MILEAGE_FROM
                },
                {
                    "name": "odometer_until",
                    "operator": "less_than_or_equal_to",
                    "value": self.Constraint.Constraint_Vehicle_MILEAGE_TO
                }
            ]
            return rule_arr
        if self.Constraint.Constraint_Vehicle_MILEAGE_FROM:
            return [{
                    "name": "odometer_from",
                    "operator": "greater_than_or_equal_to",
                    "value": self.Constraint.Constraint_Vehicle_MILEAGE_FROM
                }]
        if self.Constraint.Constraint_Vehicle_MILEAGE_TO:
            return [{
                    "name": "odometer_until",
                    "operator": "less_than_or_equal_to",
                    "value": self.Constraint.Constraint_Vehicle_MILEAGE_TO
                }]
      
    def reg(self, *args, **kwargs):
        if self.Constraint.Constraint_Vehicle_FIRST_REGISTRATION_DATE_FROM and self.Constraint.Constraint_Vehicle_FIRST_REGISTRATION_DATE_TO:
            rule_arr = [
                {
                    "name": "first_registration_date_from",
                    "operator": "greater_than_or_equal_to",
                    "value": self.Constraint.Constraint_Vehicle_FIRST_REGISTRATION_DATE_FROM
                },
                {
                    "name": "first_registration_date_until",
                    "operator": "less_than_or_equal_to",
                    "value": self.Constraint.Constraint_Vehicle_FIRST_REGISTRATION_DATE_TO
                }
            ]
            return rule_arr
        if self.Constraint.Constraint_Vehicle_FIRST_REGISTRATION_DATE_FROM:
            return [{
                    "name": "first_registration_date_from",
                    "operator": "greater_than_or_equal_to",
                    "value": self.Constraint.Constraint_Vehicle_FIRST_REGISTRATION_DATE_FROM
                }]
        if self.Constraint.Constraint_Vehicle_FIRST_REGISTRATION_DATE_TO:
            return [{
                    "name": "first_registration_date_until",
                    "operator": "less_than_or_equal_to",
                    "value": self.Constraint.Constraint_Vehicle_FIRST_REGISTRATION_DATE_TO
                }]        


class VehicleVariable(BaseVariables):
    def __init__(self, Vehicle):
        self.Vehicle = Vehicle

    @string_rule_variable()
    def series(self):
        return self.Vehicle.Vehicle_SERIES
    
    @string_rule_variable()
    def make(self):
        return self.Vehicle.Vehicle_MAKE

    @string_rule_variable()
    def model(self):
        return self.Vehicle.Vehicle_MODEL

    @string_rule_variable()
    def vtype(self):
        return self.Vehicle.Vehicle_TYPE

    @string_rule_variable()
    def vuser(self):
        return self.Vehicle.Vehicle_USER

    @string_rule_variable()
    def fin(self):
        return self.Vehicle.Vehicle_VIN

    @string_rule_variable()
    def fleet(self):
        return self.Vehicle.Vehicle_EXTERNAL_ID
    
    @datetime_rule_variable()
    def first_registration_date_from(self):
        return self.Vehicle.Vehicle_FIRST_REGISTRATION_DATE
    
    @datetime_rule_variable()
    def first_registration_date_until(self):
        return self.Vehicle.Vehicle_FIRST_REGISTRATION_DATE

    @numeric_rule_variable()
    def odometer_from(self):
        return self.Vehicle.Vehicle_LAST_MILEAGE
    
    @numeric_rule_variable()
    def odometer_until(self):
        return self.Vehicle.Vehicle_LAST_MILEAGE

class VehicleActions(BaseActions):
    def __init__(self, Vehicle, Recall):
        self.Vehicle = Vehicle
        self.Recall = Recall

    @rule_action()
    def vehicle_recall(self):
        #Fahrzeug Vehicle ist betroffen
        #1.Suche ob Vehicle Recall für Fahrzeug besteht -> Wenn ja, fertig, wenn nein -> neu anlegen
        try:
            vr = Vehicle_Recall.objects.get(Vehicle=self.Vehicle, Recall=self.Recall)
        except Vehicle_Recall.DoesNotExist:
            new = Vehicle_Recall(Vehicle=self.Vehicle, Recall=self.Recall, VR_STATUS= 0)
            new.save()
            return


