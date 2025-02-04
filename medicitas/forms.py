from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Paciente,Receta, Administrador, Perfil, Especialidad, Medicamento, HistorialMedico, Diagnostico, EstadoPaciente,Emergencia,  Medico, CitaMedica# Asegúrate de importar el modelo Paciente y administrador
from django.utils import timezone

#--------------Formulario de inicio de secion ----------#
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Nombre de usuario', max_length=150)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

#--------------Formulario de registro administrador y paciente----------#
class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirmar contraseña')
    tipo_perfil = forms.ChoiceField(choices=[
        ('paciente', 'Paciente'),
        ('administrador', 'Administrador')
    ], label='Tipo de perfil')
    codigo_secreto = forms.CharField(max_length=20, required=False, label='Código Secreto')
    
    # Campos adicionales para paciente y médico
    tipo_documento = forms.ChoiceField(choices=[
        ('cedula', 'Cédula'),
        ('pasaporte', 'Pasaporte')
    ], label='Tipo de Documento')
    
    num_documento = forms.CharField(max_length=20, label='Número de Documento')
    nombres = forms.CharField(max_length=100, label='Nombres')
    apellidos = forms.CharField(max_length=100, label='Apellidos')
    telefono = forms.CharField(max_length=20, label='Teléfono')
    direccion = forms.CharField(max_length=200, label='Dirección')
    email = forms.EmailField(label='Correo Electrónico')
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),  # Esto permite el selector de fecha
        label='Fecha de nacimiento'
    )
    sexo = forms.ChoiceField(choices=[
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
        ('otros', 'Otros')
    ], label='Sexo')
    foto_perfil = forms.ImageField(required=False, label='Foto de Perfil')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 
                  'tipo_perfil', 'codigo_secreto', 'tipo_documento', 
                  'num_documento', 'nombres', 'apellidos', 'telefono', 
                  'direccion', 'fecha_nacimiento', 'sexo', 'foto_perfil']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        
#--------------Formulario de registro administrador----------#
class RegistroAdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirmar contraseña')
    codigo_ingresado = forms.CharField(max_length=20, label='Código de Validación') 
    tipo_usuario = forms.ChoiceField(choices=Perfil.TIPO_USUARIO_CHOICES, label="Tipo de Usuario")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    tipo_documento = forms.ChoiceField(choices=Administrador.TIPO_DOCUMENTO_CHOICES, label="Tipo de Documento")
    num_documento = forms.CharField(max_length=20, label="Número de Documento")
    nombres = forms.CharField(max_length=100, label="Nombres")
    apellidos = forms.CharField(max_length=100, label="Apellidos")
    telefono = forms.CharField(max_length=15, label="Teléfono")
    direccion = forms.CharField(max_length=255, label="Dirección")
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),  # Esto permite el selector de fecha
        label='Fecha de nacimiento'
    )
    sexo = forms.ChoiceField(choices=Administrador.SEXO_CHOICES, label="Sexo")
    foto_perfil = forms.ImageField(required=False, label="Foto de Perfil")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Crear el perfil según el tipo de usuario seleccionado
            Perfil.objects.create(user=user, tipo_usuario=self.cleaned_data['tipo_usuario'])
            if self.cleaned_data['tipo_usuario'] == 'administrador':
                Administrador.objects.create(
                    perfil=user.perfil,
                    tipo_documento=self.cleaned_data['tipo_documento'],
                    num_documento=self.cleaned_data['num_documento'],
                    nombres=self.cleaned_data['nombres'],
                    apellidos=self.cleaned_data['apellidos'],
                    telefono=self.cleaned_data['telefono'],
                    direccion=self.cleaned_data['direccion'],
                    fecha_nacimiento=self.cleaned_data['fecha_nacimiento'],
                    sexo=self.cleaned_data['sexo'],
                    foto_perfil=self.cleaned_data['foto_perfil'],
                    codigo_secreto=self.cleaned_data['codigo_secreto'],
                )
        return user
    
    #--------------formulario de registro de especialidades----------
class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ['nombre', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            }
    #--------------fin de formulario de registro de especialidades----------
    #--------------Formulario de registro de medicos----------#
class RegistroMedicoForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirmar contraseña')
    tipo_perfil = forms.ChoiceField(choices=[
        ('medico', 'Médico'),
    ], label='Tipo de perfil')
    codigo_secreto = forms.CharField(max_length=20, required=False, label='Código Secreto')
    
    # Campos adicionales para paciente y médico
    tipo_documento = forms.ChoiceField(choices=[
        ('cedula', 'Cédula'),
        ('pasaporte', 'Pasaporte')
    ], label='Tipo de Documento')
    
    HORARIO_CHOICES = [
        ('08:00-12:00', '08:00 AM - 12:00 PM'),
        ('14:00-18:00', '02:00 PM - 06:00 PM'),
        ('08:00-18:00', '08:00 AM - 06:00 PM'),
        ('10:00-14:00', '10:00 AM - 02:00 PM'),
    ]
    
    horario_atencion = forms.ChoiceField(choices=HORARIO_CHOICES, label='Horario de atención')
    
    num_documento = forms.CharField(max_length=20, label='Número de Documento')
    nombres = forms.CharField(max_length=100, label='Nombres')
    apellidos = forms.CharField(max_length=100, label='Apellidos')
    telefono = forms.CharField(max_length=20, label='Teléfono')
    direccion = forms.CharField(max_length=200, label='Dirección')
    email = forms.EmailField(label='Correo Electrónico')
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Fecha de nacimiento'
    )
    sexo = forms.ChoiceField(choices=[
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
        ('otros', 'Otros')
    ], label='Sexo')
    foto_perfil = forms.ImageField(required=False, label='Foto de Perfil')
    
    # Campo para seleccionar especialidades
    especialidades = forms.ModelMultipleChoiceField(
        queryset=Especialidad.objects.all(),  # Obtén todas las especialidades
        widget=forms.CheckboxSelectMultiple,  # O puedes usar un SelectMultiple si prefieres
        label='Especialidades'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 
                  'tipo_perfil', 'codigo_secreto', 'tipo_documento', 
                  'num_documento', 'nombres', 'apellidos', 'telefono', 
                  'direccion', 'fecha_nacimiento', 'sexo', 'foto_perfil', 
                  'especialidades']  # Asegúrate de incluir 'especialidades'

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden.")
                    
class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['nombre', 'descripcion', 'dosis_recomendada']  # Ajusta según tus campos

    def __init__(self, *args, **kwargs):
        super(MedicamentoForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'campo-registro', 'placeholder': 'Nombre del Medicamento'})
        self.fields['descripcion'].widget.attrs.update({'class': 'campo-registro', 'placeholder': 'Descripción'})
        self.fields['dosis_recomendada'].widget.attrs.update({'class': 'campo-registro', 'placeholder': 'Dosis Recomendada'})

class HistorialMedicoForm(forms.ModelForm):
    class Meta:
        model = HistorialMedico
        fields = [
            'paciente',
            'citas',
            'unidad_estatura',
            'estatura',
            'unidad_peso',
            'peso',
            'diagnostico',
            'receta_medica',
            'fecha_diagnostico',
        ]
class NuevaRecetaForm(forms.ModelForm):
    paciente = forms.ModelChoiceField(queryset=Paciente.objects.all(), label="Paciente")
    class Meta:
        model = Receta
        fields = ['paciente','medicamento', 'dosis', 'frecuencia', 'fecha_inicio', 'fecha_fin', 'estado']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }
    #--------------Formulario de registro de diagnostico----------#
class DiagnosticoForm(forms.ModelForm):
    class Meta:
        model = Diagnostico
        fields = ['paciente', 'especialidad', 'descripcion']

    def __init__(self, *args, **kwargs):
        doctor = kwargs.pop('doctor', None)  # Recibimos el médico logueado
        super(DiagnosticoForm, self).__init__(*args, **kwargs)

        if doctor:
            # Filtramos las especialidades según el médico logueado
            self.fields['especialidad'].queryset = doctor.especialidades.all()     

class EstadoPacienteForm(forms.ModelForm):
    class Meta:
        model = EstadoPaciente
        fields = ['paciente', 'estatura', 'peso', 'tipo_sangre', 'ritmo_cardiaco', 'temperatura', 'presion_arterial', 'enfermedades', 'observaciones']

    def __init__(self, *args, **kwargs):
        super(EstadoPacienteForm, self).__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Paciente.objects.all()   

 #--------------Formulario de registro de emergencia ----------#

class EmergenciaForm(forms.ModelForm):
    NIVEL_CONCIENCIA_CHOICES = [
        (0, 'Alerta'),
        (1, 'Responde a voz'),
        (3, 'Responde al dolor'),
        (5, 'No responde'),
    ]

    frecuencia_cardiaca = forms.IntegerField(label='Frecuencia Cardíaca')
    frecuencia_respiratoria = forms.IntegerField(label='Frecuencia Respiratoria')
    presion_arterial = forms.IntegerField(label='Presión Arterial')
    saturacion_oxigeno = forms.IntegerField(label='Saturación de Oxígeno')
    nivel_conciencia = forms.ChoiceField(choices=NIVEL_CONCIENCIA_CHOICES, label='Nivel de Conciencia')
    especialidad = forms.ModelChoiceField(queryset=Especialidad.objects.all(), label='Especialidad')

    class Meta:
        model = Emergencia
        fields = ['frecuencia_cardiaca', 'frecuencia_respiratoria', 'presion_arterial', 'saturacion_oxigeno', 'nivel_conciencia', 'especialidad']