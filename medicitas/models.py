from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models  # Importa el módulo de modelos de Django
from django.contrib.auth.models import User  # Importa el modelo de usuario de Django
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator  # Importa validadores
from django.utils import timezone  # Importa funciones relacionadas con el tiempo
from datetime import timedelta  # Importa timedelta para manejar duraciones


# para migrar cambiar el estado de paciente en reseta no olvidar

#para crear  perfiles a cada usuario

@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        # Crear perfil con tipo de usuario por defecto
        Perfil.objects.create(user=instance, tipo_usuario='paciente')

class Perfil(models.Model):
    TIPO_USUARIO_CHOICES = [
        ('paciente', 'Paciente'),
        ('medico', 'Médico'),
        ('administrador', 'Administrador'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.tipo_usuario}"

class Administrador(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('cedula', 'Cédula'),
        ('pasaporte', 'Pasaporte'),
    ]
    
    SEXO_CHOICES = [
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
        ('otros', 'Otros'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    tipo_documento = models.CharField(max_length=10, choices=TIPO_DOCUMENTO_CHOICES)
    num_documento = models.CharField(max_length=20)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=255)
    email = models.EmailField(unique=True, default='default@example.com')
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class Especialidad(models.Model):  # Define el modelo para Especialidad
    nombre = models.CharField(max_length=100, unique=True)  # Nombre de la especialidad, único
    descripcion = models.TextField(default='')  # Descripción de la especialidad, por defecto vacío

    def __str__(self):  # Método para representar la especialidad como cadena
        return self.nombre  # Retorna el nombre de la especialidad

class Paciente(models.Model):  # Define el modelo para Paciente
    TIPO_DOCUMENTO_CHOICES = [  # Opciones para tipo de documento
        ('cedula', 'Cédula'),  # Opción de cédula
        ('pasaporte', 'Pasaporte'),  # Opción de pasaporte
    ]
    SEXO_CHOICES = [  # Opciones para sexo
        ('masculino', 'Masculino'),  # Opción masculino
        ('femenino', 'Femenino'),  # Opción femenino
        ('otros', 'Otros'),  # Opción otros
    ]

    id_paciente = models.AutoField(primary_key=True)  # ID único del paciente, autoincremental
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Relación uno a uno con el modelo User
    tipo_documento = models.CharField(max_length=10, choices=TIPO_DOCUMENTO_CHOICES, default='cedula')  # Tipo de documento con opciones
    num_documento = models.CharField(  # Número de documento
        max_length=20, 
        unique=True,  # Debe ser único
        validators=[  # Validadores para el formato
            RegexValidator(
                regex=r'^\d+$',  # Solo permite números
                message='Solo se permiten números en el número de documento'
            )
        ]
    )
    nombres = models.CharField(max_length=100)  # Nombres del paciente
    apellidos = models.CharField(max_length=100)  # Apellidos del paciente
    telefono = models.CharField(  # Teléfono del paciente
        max_length=20,
        validators=[  # Validadores para el formato de teléfono
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',  # Formato válido para teléfono
                message='Número de teléfono inválido'
            )
        ]
    )
    direccion = models.CharField(max_length=200)  # Dirección del paciente
    email = models.EmailField(unique=True)  # Correo electrónico único
    fecha_nacimiento = models.DateField()  # Fecha de nacimiento del paciente
    foto_perfil = models.ImageField(upload_to='fotos_perfil', null=True, blank=True)  # Foto de perfil opcional
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES, default='masculino')  # Sexo del paciente

    def __str__(self):  # Método para representar el paciente como cadena
        return f"{self.nombres} {self.apellidos}"  # Retorna el nombre completo del paciente

class Medico(models.Model):  # Define el modelo para Médico
    TIPO_DOCUMENTO_CHOICES = [  # Opciones para tipo de documento
        ('cedula', 'Cédula'),  # Opción de cédula
        ('pasaporte', 'Pasaporte'),  # Opción de pasaporte
    ]
    SEXO_CHOICES = [  # Opciones para sexo
        ('masculino', 'Masculino'),  # Opción masculino
        ('femenino', 'Femenino'),  # Opción femenino
        ('otros', 'Otros'),  # Opción otros
    ]
    HORARIO_CHOICES = [  # Opciones para horarios de atención
        ('08:00-12:00', '08:00 AM - 12:00 PM'),  # Horario de mañana
        ('14:00-18:00', '02:00 PM - 06:00 PM'),  # Horario de tarde
        ('08:00-18:00', '08:00 AM - 06:00 PM'),  # Horario completo
        ('10:00-14:00', '10:00 AM - 02:00 PM'),  # Otro horario
    ]

    id_medico = models.AutoField(primary_key=True)  # ID único del médico, autoincremental
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Relación uno a uno con el modelo User
    tipo_documento = models.CharField(max_length=10, choices=TIPO_DOCUMENTO_CHOICES, default='cedula')  # Tipo de documento con opciones
    num_documento = models.CharField(  # Número de documento
        max_length=20, 
        unique=True,  # Debe ser único
        validators=[  # Validadores para el formato
            RegexValidator(
                regex=r'^\d+$',  # Solo permite números
                message='Solo se permiten números en el número de documento'
            )
        ]
    )
    nombres = models.CharField(max_length=100)  # Nombres del médico
    apellidos = models.CharField(max_length=100)  # Apellidos del médico
    telefono = models.CharField(  # Teléfono del médico
        max_length=20,
        validators=[  # Validadores para el formato de teléfono
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',  # Formato válido para teléfono
                message='Número de teléfono inválido'
            )
        ]
    )
    email = models.EmailField(unique=True)  # Correo electrónico único
    especialidades = models.ManyToManyField(Especialidad, related_name='medicos')  # Relación muchos a muchos con Especialidad
    foto_perfil = models.ImageField(upload_to='fotos_perfil', null=True, blank=True)  # Foto de perfil opcional
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES, default='masculino')  # Sexo del médico
    horario_atencion = models.CharField(  # Campo de selección para horario de atención
        max_length=20, 
        choices=HORARIO_CHOICES,  # Opciones de horarios
        default='08:00-12:00'  # Horario por defecto
    )

    def __str__(self):  # Método para representar el médico como cadena
        return f"{self.nombres} {self.apellidos}"  # Retorna el nombre completo del médico
   


class CitaMedica(models.Model):  # Define el modelo para Cita Médica
    ESTADO_CHOICES = [  # Opciones para el estado de la cita
        ('programada', 'Programada'),  # Cita programada
        ('confirmada', 'Confirmada'),  # Cita confirmada
        ('realizada', 'Realizada'),  # Cita realizada
        ('cancelada', 'Cancelada')  # Cita cancelada
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='citas')  # Relación muchos a uno con Paciente
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='citas')  # Relación muchos a uno con Médico
    especialidad = models.ForeignKey(Especialidad, on_delete=models.SET_NULL, null=True)  # Relación muchos a uno con Especialidad, permite nulo
    fecha_hora = models.DateTimeField()  # Fecha y hora de la cita
    sintomas = models.TextField()  # Síntomas del paciente
    calificacion = models.IntegerField(  # Calificación de la cita
        null=True, 
        blank=True, 
        validators=[MinValueValidator(1), MaxValueValidator(5)]  # Validadores para la calificación
    )
    duracion = models.DurationField(default=timedelta(minutes=30))  # Duración de la cita, por defecto 30 minutos
    estado = models.CharField(  # Estado de la cita
        max_length=20, 
        choices=ESTADO_CHOICES,  # Opciones de estado
        default='programada'  # Estado por defecto
    )
    es_covid = models.BooleanField(default=False)  # Indica si la cita es por COVID-19
    es_influenza = models.BooleanField(default=False)  # Indica si la cita es por Influenza

    def save(self, *args, **kwargs):
        # Verifica si se está creando una nueva cita (no tiene ID)
        if not self.pk:  # Solo verificar si es una nueva cita
            if CitaMedica.objects.filter(medico=self.medico, fecha_hora=self.fecha_hora).exists():
                raise ValueError("Este horario ya está ocupado por otra cita.")
        super().save(*args, **kwargs)  # Llama al método de guardado original
   

    def __str__(self):  # Método para representar la cita como cadena
        return f"Cita de {self.paciente} con {self.medico} el {self.fecha_hora}"  # Retorna información sobre la cita

class Diagnostico(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='diagnosticos')
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)  # Relación con Especialidad
    descripcion = models.TextField()
    fecha_diagnostico = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Diagnóstico de {self.paciente} - {self.especialidad}"
class Medicamento(models.Model):  # Define el modelo para Medicamento
    nombre = models.CharField(max_length=200, unique=True)  # Nombre del medicamento, único
    descripcion = models.TextField()  # Descripción del medicamento
    dosis_recomendada = models.CharField(max_length=100)  # Dosis recomendada
    efectos_secundarios = models.TextField(blank=True, null=True)  # Efectos secundarios opcionales

    def __str__(self):  # Método para representar el medicamento como cadena
        return self.nombre  # Retorna el nombre del medicamento
    
class Receta(models.Model):
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada')
    ]

    #paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='recetas')  # Relación directa con Paciente
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='recetas', null=True)  # Permitir nulos
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)  # Relación con Medicamento
    dosis = models.CharField(max_length=100)
    frecuencia = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES,
          default='activa'
    )

    def __str__(self):
        return f"Receta de {self.medicamento} para {self.paciente}"

class EstadoPaciente(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    estatura = models.FloatField()
    peso = models.FloatField()
    tipo_sangre = models.CharField(max_length=3)
    ritmo_cardiaco = models.IntegerField()
    temperatura = models.FloatField()  # Nuevo campo
    presion_arterial = models.CharField(max_length=7)  # Nuevo campo (ejemplo: "120/80")
    enfermedades = models.TextField(blank=True)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Estado de {self.paciente.nombre}"
    
class HistorialMedico(models.Model):  # Define el modelo para Historial Médico
    TIPO_ESTATURA = [  # Opciones para unidad de estatura
        ('metros', 'Metros'),  # Opción metros
        ('pulgadas', 'Pulgadas'),  # Opción pulgadas
    ]
    TIPO_PESO = [  # Opciones para unidad de peso
        ('libras', 'Libras'),  # Opción libras
        ('kilos', 'Kilos'),  # Opción kilos
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='historiales')  # Relación muchos a uno con Paciente
    num_identificacion = models.CharField(max_length=20)  # Número de identificación del historial
    citas = models.ManyToManyField(  # Relación muchos a muchos con CitaMedica
        CitaMedica, 
        related_name='historial_medico',  # Nombre relacionado para acceder a los historiales desde CitaMedica
        limit_choices_to={'paciente': models.F('paciente')}  # Limita las opciones a citas del mismo paciente
    )
    unidad_estatura = models.CharField(max_length=10, choices=TIPO_ESTATURA, default='metros')  # Unidad de estatura
    estatura = models.FloatField(null=True, blank=True)  # Estatura del paciente
    unidad_peso = models.CharField(max_length=10, choices=TIPO_PESO, default='libras')  # Unidad de peso
    peso = models.FloatField(null=True, blank=True)  # Peso del paciente
    diagnostico = models.TextField()  # Diagnóstico del paciente
    receta_medica = models.TextField()  # Receta médica del paciente
    fecha_diagnostico = models.DateTimeField(default=timezone.now)  # Fecha del diagnóstico

    def __str__(self):  # Método para representar el historial como cadena
        return f"Historial médico de {self.paciente}"  # Retorna información sobre el historial
    
class Notificacion(models.Model):  # Define el modelo para Notificación
    TIPO_CHOICES = [  # Opciones para tipo de notificación
        ('cita', 'Cita'),  # Notificación de cita
        ('examen', 'Examen'),  # Notificación de examen
        ('recordatorio', 'Recordatorio'),  # Notificación de recordatorio
        ('otro', 'Otro')  # Otro tipo de notificación
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones')  # Relación muchos a uno con User
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)  # Tipo de notificación
    mensaje = models.TextField()  # Mensaje de la notificación
    fecha = models.DateTimeField(auto_now_add=True)  # Fecha de creación de la notificación
    leida = models.BooleanField(default=False)  # Indica si la notificación ha sido leída

    def __str__(self):  # Método para representar la notificación como cadena
        return f"Notificación {self.tipo} - {self.fecha}"  # Retorna información sobre la notificación

class FormularioSatisfaccion(models.Model):  # Define el modelo para Formulario de Satisfacción
    cita = models.OneToOneField(CitaMedica, on_delete=models.CASCADE)  # Relación uno a uno con CitaMedica
    calificacion_general = models.IntegerField(  # Calificación general del servicio
        validators=[MinValueValidator(1), MaxValueValidator(5)]  # Validadores para la calificación
    )
    comentarios = models.TextField(blank=True, null=True)  # Comentarios opcionales
    fecha_completado = models.DateTimeField(auto_now_add=True)  # Fecha de completado del formulario

    def __str__(self):  # Método para representar el formulario como cadena
        return f"Formulario de satisfacción para cita {self.cita}"  # Retorna información sobre el formulario

class Reporte(models.Model):  # Define el modelo para Reporte
    TIPO_CHOICES = [  # Opciones para tipo de reporte
        ('estadistico', 'Estadístico'),  # Reporte estadístico
        ('enfermedades', 'Enfermedades Comunes'),  # Reporte de enfermedades comunes
        ('desempeño_medico', 'Desempeño Médico')  # Reporte de desempeño médico
    ]

    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)  # Tipo de reporte
    fecha_generacion = models.DateTimeField(auto_now_add=True)  # Fecha de generación del reporte
    datos = models.JSONField()  # Datos del reporte en formato JSON
    archivo = models.FileField(upload_to='reportes/', blank=True, null=True)  # Archivo adjunto opcional

    def __str__(self):  # Método para representar el reporte como cadena
        return f"Reporte {self.tipo} - {self.fecha_generacion}"  # Retorna información sobre el reporte
 
class Factura(models.Model):  # Define el modelo para Factura
    cita = models.OneToOneField(CitaMedica, on_delete=models.CASCADE)  # Relación uno a uno con CitaMedica
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)  # Monto total de la factura
    fecha_generacion = models.DateTimeField(auto_now_add=True)  # Fecha de generación de la factura
    estado = models.CharField(  # Estado de la factura
        max_length=20, 
        choices=[  # Opciones para el estado
            ('PENDIENTE', 'Pendiente'),  # Factura pendiente
            ('PAGADA', 'Pagada'),  # Factura pagada
            ('CANCELADA', 'Cancelada')  # Factura cancelada
        ], 
        default='PENDIENTE'  # Estado por defecto
    )
    
    def __str__(self):  # Método para representar la factura como cadena
        return f"Factura de {self.cita.paciente} - {self.monto_total}"  # Retorna información sobre la factura
    