from rest_framework import serializers
from .models import Paciente, Medico, Especialidad, CitaMedica,HistorialMedico


class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        #fields: ( 'nombre', 'apellido'......) se importara solo los valores que se eligan 
        fields= '__all__'

class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields= '__all__'

class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields= '__all__'



class CitaMedicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitaMedica
        fields= '__all__'

class HistorialMedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialMedico
        fields= '__all__'                
