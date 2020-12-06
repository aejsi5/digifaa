from rest_framework import serializers
from .models import *
from datetime import datetime

class BasicWorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = ['Workshop_ID', 'Workshop_EXTERNAL_ID', 'Workshop_NAME', 'Workshop_PHONE']

class Basic_Get_Vehicle_RecallSerializer(serializers.ModelSerializer):
    VR_LAST_UPDATE_WORKSHOP = BasicWorkshopSerializer(many=False, read_only=True)

    class Meta:
            model = Vehicle_Recall
            fields = '__all__'
            read_only_fields = ['Vehicle_Recall_ID', 'Vehicle', 'Recall', 'VR_STATUS','VR_LAST_UPDATE', 'VR_LAST_UPDATE_BY','VR_LAST_UPDATE_WORKSHOP', 'VR_DATE_CREATED', 'VR_DATE_COMPLETED']

class Basic_Vehicle_RecallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle_Recall
        fields = '__all__'
        read_only_fields = ['Vehicle_Recall_ID', 'Vehicle', 'Recall', 'VR_DATE_CREATED']
    
    def validate(self, data):
        """
        Only allowed to set Status to preset or pending
        """
        if data['VR_STATUS'] == 2:
            raise serializers.ValidationError("PATCH Status not allowed")
        if data['VR_STATUS'] == 0:
            null = None
            data['VR_DATE_COMPLETED'] = null
        if data['VR_STATUS'] == 1:
            now = datetime.now()
            data['VR_DATE_COMPLETED'] = now.strftime("%Y-%m-%d")
        return data

class Full_Vehicle_RecallSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Vehicle_Recall
        fields = '__all__'

class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = '__all__'
        read_only_fields = ('user',)

class BasicVehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = ['Vehicle_ID', 'Vehicle_VIN', 'Vehicle_PLATE', 'Vehicle_MAKE', 'Vehicle_MODEL', 'Vehicle_FIRST_REGISTRATION_DATE']

class FullVehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = '__all__'

class FullRecallDocSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recall_Doc
        fields = '__all__'

class FullRecallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recall
        fields = '__all__'

class FullRecallDocListSerializer(serializers.ModelSerializer):
    Recall = FullRecallSerializer(many=False, read_only=True)
    Document_PATH = serializers.SerializerMethodField()
    
    def get_Document_PATH(self, obj):
        return os.path.basename(obj.Document_PATH.file.name)

    class Meta:
        model = Recall_Doc
        fields = '__all__'

class BasicWorkshopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workshop
        fields = ['Workshop_ID', 'Workshop_NAME', 'Workshop_ADDRESS', 'Workshop_ZIP', 'Workshop_CITY']

class FullWorkshopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workshop
        fields = '__all__'

class VehicleRecallListSerializer(serializers.ModelSerializer):
    Vehicle = BasicVehicleSerializer(many=False, read_only=True)
    
    class Meta:
        model = Vehicle_Recall
        fields = ['Vehicle_Recall_ID', 'VR_STATUS', 'VR_DATE_CREATED', 'VR_DATE_COMPLETED', 'Vehicle']

class ConstraintSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Constraint
        exclude = ['Recall']

class FullConstraintSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Constraint
        fields = '__all__'