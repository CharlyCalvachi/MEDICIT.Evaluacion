from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets
from .serializer import PacienteSerializer, MedicoSerializer, EspecialidadSerializer,CitaMedicaSerializer, HistorialMedicoSerializer
from .models import Paciente, Medico, Especialidad, CitaMedica, HistorialMedico, Perfil, Administrador, Medicamento, Receta,EstadoPaciente
from django.contrib.auth import login, authenticate
from .forms import CustomAuthenticationForm,NuevaRecetaForm, RegistroForm, RegistroAdminForm, EspecialidadForm,RegistroMedicoForm, MedicamentoForm, HistorialMedicoForm, DiagnosticoForm, EstadoPacienteForm
from datetime import datetime, timedelta,date
from django.utils import timezone
 

  #----------Vista de registro paciente y administrador ---------#
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])
             # Establecer el estado de personal si es un administrador
            tipo_perfil = form.cleaned_data['tipo_perfil']
            if tipo_perfil == 'administrador':
                usuario.is_staff = True  # Activar el estado de personal
                usuario.is_superuser = True  # Activar la opción de superusuario
            usuario.save()

            # Crear el perfil de usuario
            perfil = Perfil.objects.get(user=usuario)
            perfil.tipo_usuario = form.cleaned_data['tipo_perfil']
            perfil.save()

            # Guardar datos en el modelo correspondiente
            codigo_secreto = form.cleaned_data['codigo_secreto']

            if tipo_perfil == 'paciente':
                paciente = Paciente(
                    usuario=usuario,
                    tipo_documento=form.cleaned_data['tipo_documento'],
                    num_documento=form.cleaned_data['num_documento'],
                    nombres=form.cleaned_data['nombres'],
                    apellidos=form.cleaned_data['apellidos'],
                    telefono=form.cleaned_data['telefono'],
                    direccion=form.cleaned_data['direccion'],
                    email=form.cleaned_data['email'],
                    fecha_nacimiento=form.cleaned_data['fecha_nacimiento'],
                    sexo=form.cleaned_data['sexo'],
                    foto_perfil=form.cleaned_data['foto_perfil']
                )
                paciente.save()
                messages.success(request, "Registro de paciente exitoso. Ahora puedes iniciar sesión.")

            elif tipo_perfil == 'medico':
                if not codigo_secreto:
                    messages.error(request, "El código secreto es obligatorio para médicos.")
                    return render(request, 'registro.html', {'form': form})

                if codigo_secreto != settings.CODIGO_SECRETO_ADMIN:
                    messages.error(request, "El código secreto es incorrecto.")
                    return render(request, 'registro.html', {'form': form})

            elif tipo_perfil == 'administrador':
                if not codigo_secreto:
                    messages.error(request, "El código secreto es obligatorio para administradores.")
                    return render(request, 'registro.html', {'form': form})

                if codigo_secreto != settings.CODIGO_SECRETO_ADMIN:
                    messages.error(request, "El código secreto es incorrecto.")
                    return render(request, 'registro.html', {'form': form})

                administrador = Administrador(
                    usuario=usuario,
                    tipo_documento=form.cleaned_data['tipo_documento'],
                    num_documento=form.cleaned_data['num_documento'],
                    nombres=form.cleaned_data['nombres'],
                    apellidos=form.cleaned_data['apellidos'],
                    telefono=form.cleaned_data['telefono'],
                    direccion=form.cleaned_data['direccion'],
                    email=form.cleaned_data['email'],
                    fecha_nacimiento=form.cleaned_data['fecha_nacimiento'],
                    sexo=form.cleaned_data['sexo'],
                    foto_perfil=form.cleaned_data['foto_perfil']
                )
                administrador.save()
                messages.success(request, "Registro de administrador exitoso. Ahora puedes iniciar sesión.")

            return redirect('/iniciarSesion/')
    else:
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form})


 #----------Vista de inicio de secion paciente---------#


def admin_dashboard(request):
    return render(request, 'administrador/admin_dashboard.html')

def registrarEspecialidad(request):
    if request.method == 'POST':
        form = EspecialidadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Especialidad registrada exitosamente.")
            return redirect('/registrarEspecialidad')
    else:
        form = EspecialidadForm()

    # Obtener todas las especialidades registradas
    especialidades = Especialidad.objects.all()

    return render(request, 'administrador/registrarEspecialidad.html', {'form': form, 'especialidades': especialidades})

def editarEspecialidad(request, id):
    especialidad = get_object_or_404(Especialidad, id=id)

    if request.method == 'POST':
        form = EspecialidadForm(request.POST, instance=especialidad)
        if form.is_valid():
            form.save()
            messages.success(request, "Especialidad actualizada exitosamente.")
            return redirect('/registrarEspecialidad')
    else:
        form = EspecialidadForm(instance=especialidad)

    return render(request, 'administrador/registrarEspecialidad.html', {'form': form, 'especialidades': Especialidad.objects.all()})

def eliminarEspecialidad(request, id):
    especialidad = get_object_or_404(Especialidad, id=id)
    especialidad.delete()
    messages.success(request, "Especialidad eliminada exitosamente.")
    return redirect('/registrarEspecialidad')

def registrarMedico(request):
    if request.method == 'POST':
        form = RegistroMedicoForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()  # Asegúrate de guardar el usuario aquí

            # Crear el perfil de usuario
            perfil = Perfil.objects.get(user=usuario)
            perfil.tipo_usuario = form.cleaned_data['tipo_perfil']
            perfil.save()

            # Guardar datos en el modelo correspondiente
            codigo_secreto = form.cleaned_data['codigo_secreto']
            tipo_perfil = form.cleaned_data['tipo_perfil']

            if tipo_perfil == 'medico':
                if not codigo_secreto:
                    messages.error(request, "El código secreto es obligatorio para médicos.")
                    return render(request, 'registrarMedico.html', {'form': form})

                if codigo_secreto != settings.CODIGO_SECRETO_ADMIN:
                    messages.error(request, "El código secreto es incorrecto.")
                    return render(request, 'registrarMedico.html', {'form': form})

                # Crear el objeto Medico
                medico = Medico(
                    usuario=usuario,
                    tipo_documento=form.cleaned_data['tipo_documento'],
                    num_documento=form.cleaned_data['num_documento'],
                    nombres=form.cleaned_data['nombres'],
                    apellidos=form.cleaned_data['apellidos'],
                    telefono=form.cleaned_data['telefono'],
                    email=form.cleaned_data['email'],
                    horario_atencion=form.cleaned_data['horario_atencion'],
                    foto_perfil=form.cleaned_data['foto_perfil'],  
                )
                
                # Asignar especialidades
                medico.save()  # Guarda el objeto Medico antes de asignar especialidades
                medico.especialidades.set(form.cleaned_data['especialidades'])  # Asigna las especialidades después de guardar el objeto

                messages.success(request, "Registro de médico exitoso. Ahora puedes iniciar sesión.")
                return redirect('/registrarMedico/')  # Redirige después de un registro exitoso

    else:
        form = RegistroMedicoForm()
        # Obtener todos los médicos para mostrarlos en la tabla
    medicos = Medico.objects.all()
    return render(request, 'administrador/registrarMedico.html', {'form': form, 'medicos': medicos})

def editarMedico(request, medico_id):
    medico = get_object_or_404(Medico, id_medico=medico_id)
    if request.method == 'POST':
        form = RegistroMedicoForm(request.POST, request.FILES, instance=medico)
        if form.is_valid():
            form.save()
            messages.success(request, "Médico actualizado exitosamente.")
            return redirect('registrarMedico')
    else:
        form = RegistroMedicoForm(instance=medico)
    
    return render(request, 'administrador/editarMedico.html', {'form': form})

def eliminarMedico(request, medico_id):
    medico = get_object_or_404(Medico, id_medico=medico_id)

    # Eliminar el perfil de usuario
    user = medico.usuario
    user.delete()  # Esto eliminará el perfil

    # Eliminar el médico
    medico.delete()
    messages.success(request, "Médico y su perfil eliminados exitosamente.")
    return redirect('/registrarMedico/')

def perfiladministrador(request):
    # Supongamos que ya tienes un usuario autenticado
    administrador = Administrador.objects.get(usuario=request.user)
      # Obtén el paciente asociado al usuario
    return render(request, 'administrador/perfiladministrador.html', {'Administrador': administrador})
#return render(request,'perfil.html')

def registrarMedicamento(request):
    if request.method == 'POST':
        form = MedicamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/registrarMedicamento')  # Redirige después de guardar
    else:
        form = MedicamentoForm()

    medicamentos = Medicamento.objects.all().order_by('nombre')  # Obtener medicamentos ordenados

    return render(request, 'administrador/registrarMedicamento.html', {'form': form, 'medicamentos': medicamentos})

def editarMedicamento(request, id):
    medicamento = get_object_or_404(Medicamento, id=id)
    if request.method == 'POST':
        form = MedicamentoForm(request.POST, instance=medicamento)
        if form.is_valid():
            form.save()
            return redirect('/registrarMedicamento')  # Redirige después de editar
    else:
        form = MedicamentoForm(instance=medicamento)

    medicamentos = Medicamento.objects.all().order_by('nombre')  # Obtener medicamentos ordenados
    return render(request, 'administrador/registrarMedicamento.html', {'form': form, 'medicamentos': medicamentos, 'editando': True, 'medicamento': medicamento})

def eliminarMedicamento(request, id):
    medicamento = get_object_or_404(Medicamento, id=id)
    if request.method == 'POST':
        medicamento.delete()
        return redirect('/registrarMedicamento')  # Redirige después de eliminar
    medicamentos = Medicamento.objects.all().order_by('nombre')  # Obtener medicamentos ordenados
    return render(request, 'administrador/registrarMedicamento.html', {'medicamentos': medicamentos, 'medicamento': medicamento})

def reportesHospital(request):
    return render(request, 'administrador/reportesHospital.html')

def generar_reporte(request):
    # Obtener datos de citas médicas
    report_data = []

    especialidades = Especialidad.objects.all()
    for especialidad in especialidades:
        total_citas = CitaMedica.objects.filter(especialidad=especialidad).count()
        total_influenza = CitaMedica.objects.filter(especialidad=especialidad, es_influenza=True).count()
        total_covid = CitaMedica.objects.filter(especialidad=especialidad, es_covid=True).count()

        report_data.append({
            'especialidad': especialidad.nombre,
            'total_citas': total_citas,
            'total_influenza': total_influenza,
            'total_covid': total_covid,
        })

    context = {
        'report_data': report_data,
    }
    return render(request, 'administrador/reporte.html', context)
# -----------------vistas de paciente-------------------#

def paciente_dashboard(request):
    return render(request, 'paciente/paciente_dashboard.html')

def inicio(request):
    title='hola mundo'
    return render(request,'paciente/index.html')

def medicos(request):
    medicos = Medico.objects.all()  # Obtiene todos los médicos registrados
    return render(request, 'paciente/medicos.html', {'medicos': medicos})

def agendarCita(request):
    especialidades = Especialidad.objects.all()
    return render(request, 'paciente/agendarCita.html', {'especialidades': especialidades})

def registrarCita(request):
    if request.method == 'POST':
        paciente = request.user.paciente
        medico_id = request.POST['medico']
        especialidad_id = request.POST['especialidad']
        fecha = request.POST['fecha']
        hora = request.POST['hora']
        sintomas = request.POST['sintomas']
        enfermedad = request.POST['enfermedad']

        # Crear la cita
        cita = CitaMedica(
            paciente=paciente,
            medico_id=medico_id,
            especialidad_id=especialidad_id,
            fecha_hora=f"{fecha} {hora}",
            sintomas=sintomas,
            es_covid=(enfermedad == 'covid'),
            es_influenza=(enfermedad == 'influenza')
        )
        cita.save()
        return redirect('/citasAgendadas')  # Redirigir a la lista de citas agendadas

def cargarMedicos(request, especialidad_id):
    medicos = Medico.objects.filter(especialidades__id=especialidad_id)
    medicos_data = [{'id': medico.id_medico, 'nombre': f"{medico.nombres} {medico.apellidos}"} for medico in medicos]
    return JsonResponse(medicos_data, safe=False)

def cargarDisponibilidad(request, medico_id, fecha):
    # Convertir la fecha a un objeto datetime
    fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
    
    # Obtener todas las citas programadas para el médico en esa fecha
    citas = CitaMedica.objects.filter(medico_id=medico_id, fecha_hora__date=fecha_obj)

    # Crear un conjunto de horas ocupadas
    horas_ocupadas = set()
    for cita in citas:
        horas_ocupadas.add(cita.fecha_hora.strftime('%H:%M'))  # Formato HH:MM

    horas_disponibles = []
    for i in range(8, 18):  # Horas de 8 AM a 5 PM
        for j in [0, 30]:  # Intervalos de 0 y 30 minutos
            hora = f"{i}:{j:02d}"  # Formato HH:MM
            if hora not in horas_ocupadas:
                horas_disponibles.append(hora)

    return JsonResponse(horas_disponibles, safe=False)


@login_required
def citasAgendadas(request):
    paciente = get_object_or_404(Paciente, usuario=request.user)
    citas = CitaMedica.objects.filter(paciente=paciente).select_related('medico', 'especialidad')

    if request.method == 'POST':
        cita_id = request.POST.get('cita_id')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        sintomas = request.POST.get('sintomas')

        # Obtener la cita a editar
        cita = get_object_or_404(CitaMedica, id=cita_id, paciente=paciente)

        # Actualizar solo los campos permitidos
        cita.fecha_hora = f"{fecha} {hora}"
        cita.sintomas = sintomas
        cita.save()

        messages.success(request, "Cita actualizada exitosamente.")
        return redirect('/citasAgendadas')

    return render(request, 'paciente/citasAgendadas.html', {'citas': citas})


@login_required
def eliminar_cita(request, cita_id):
    paciente = get_object_or_404(Paciente, usuario=request.user)
    cita = CitaMedica.objects.filter(id=cita_id, paciente=paciente).first()  # Obtén la cita si pertenece al paciente

    if cita is None:
        messages.error(request, "No tienes permiso para eliminar esta cita.")
        return redirect('/citasAgendadas')  # Redirige si no hay permiso

    if request.method == 'POST':
        cita.delete()
        messages.success(request, "Cita eliminada exitosamente.")
        return redirect('/citasAgendadas')
    
@login_required
def editarCita(request, cita_id):
    cita = get_object_or_404(CitaMedica, id=cita_id, paciente=request.user)

    if request.method == 'POST':
        # Actualiza solo los campos permitidos
        cita.sintomas = request.POST.get('sintomas', cita.sintomas)
        fecha_hora = request.POST.get('fecha_hora', cita.fecha_hora.strftime('%Y-%m-%d %H:%M'))
        
        # Separa la fecha y la hora
        fecha, hora = fecha_hora.split(' ')
        cita.fecha_hora = f"{fecha} {hora}"  # Actualiza la fecha y hora

        cita.save()
        messages.success(request, "Cita actualizada exitosamente.")
        return redirect('citasAgendadas')

    return render(request, 'paciente/editarCita.html', {'cita': cita})


def about(request):
    return HttpResponse("<h2>About</h2>")

def perfil(request):
    # Supongamos que ya tienes un usuario autenticado
    paciente = Paciente.objects.get(usuario=request.user)
      # Obtén el paciente asociado al usuario
    return render(request, 'paciente/perfil.html', {'paciente': paciente})
#return render(request,'perfil.html')




#**********************vistas de medico**************************#
def medico_dashboard(request):
    return render(request, 'medico/medico_dashboard.html')

def citasprogramadas(request):
    medico = request.user.medico  # Obtén el médico logueado
    citas = CitaMedica.objects.filter(medico=medico)  # Filtra las citas por el médico

    # Filtrar las citas que aún no han pasado
    citas_futuras = citas.filter(fecha_hora__gte=datetime.now()).order_by('fecha_hora')

    return render(request, 'medico/citasprogramadas.html', {'citas': citas_futuras})

def actualizar_estado_cita(request, cita_id):
    if request.method == 'POST':
        estado = request.POST.get('estado')
        cita = CitaMedica.objects.get(id=cita_id)
        cita.estado = estado
        cita.save()
        return redirect('/citasprogramadas')  # Redirigir de vuelta a la lista de citas

def historialesmedicos(request):
    pacientes = Paciente.objects.all()  # Obtener todos los pacientes
    for paciente in pacientes:
        paciente.edad = (date.today() - paciente.fecha_nacimiento).days // 365  # Calcular la edad en años
    return render(request, 'medico/historialesmedicos.html', {'pacientes': pacientes})

def historial_medico(request):
    num_documento = None
    citas = []
    recetas = []  # Inicializamos la lista de recetas
    
    if request.method == 'POST':
        form = HistorialMedicoForm(request.POST)
        if form.is_valid():
            historial = form.save(commit=False)
            # Asignar el número de documento del paciente al historial
            historial.num_identificacion = form.cleaned_data['paciente'].num_documento
            historial.save()
            return redirect('/historial_medico')  # Redirigir después de guardar
    else:
        form = HistorialMedicoForm()

    # Obtener el paciente seleccionado
    paciente_id = request.GET.get('paciente')
    if paciente_id:
        paciente = get_object_or_404(Paciente, id=paciente_id)
        num_documento = paciente.num_documento
        citas = CitaMedica.objects.filter(paciente=paciente)  # Obtener solo las citas del paciente
        recetas = Receta.objects.filter(paciente=paciente)  # Obtener solo las recetas del paciente

    pacientes = Paciente.objects.all()  # Obtener todos los pacientes

    return render(request, 'medico/historial_medico.html', {
        'form': form,
        'pacientes': pacientes,
        'num_documento': num_documento,
        'citas': citas,
        'recetas': recetas,  # Pasar las recetas a la plantilla
    })

@login_required
def crear_diagnostico(request):
    doctor = Medico.objects.get(usuario=request.user)  # Obtener el médico logueado

    if request.method == 'POST':
        form = DiagnosticoForm(request.POST, doctor=doctor)  # Pasamos el médico logueado
        if form.is_valid():
            form.save()
            return redirect('/crear_diagnostico')  # Redirigir después de guardar
    else:
        form = DiagnosticoForm(doctor=doctor)  # Pasamos el médico logueado

    return render(request, 'medico/crear_diagnostico.html', {'form': form})

def gestionar_estado_paciente(request):
    estados = EstadoPaciente.objects.all()  # Obtener todos los estados de pacientes

    if request.method == 'POST':
        form = EstadoPacienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Estado del paciente registrado exitosamente.")
            return redirect('/gestionar_estado_paciente')  # Cambia por el nombre de la URL
    else:
        form = EstadoPacienteForm()

    return render(request, 'medico/gestionar_estado_paciente.html', {'form': form, 'estados': estados})

def editar_estado_paciente(request, estado_id):
    estado = get_object_or_404(EstadoPaciente, id=estado_id)

    if request.method == 'POST':
        form = EstadoPacienteForm(request.POST, instance=estado)
        if form.is_valid():
            form.save()
            messages.success(request, "Estado del paciente actualizado exitosamente.")
            return redirect('/gestionar_estado_paciente')  # Cambia por el nombre de la URL
    else:
        form = EstadoPacienteForm(instance=estado)

    return render(request, 'medico/editar_estado_paciente.html', {'form': form, 'paciente': estado.paciente})


def historial_unico(request):
    pacientes = Paciente.objects.all()
    paciente = None
    edad = None
    diagnosticos = []  # Inicializar la lista de diagnósticos

    if 'paciente_id' in request.GET and request.GET['paciente_id']:
        paciente_id = request.GET['paciente_id']
        paciente = get_object_or_404(Paciente, id_paciente=paciente_id)

        # Calcular la edad
        if paciente.fecha_nacimiento:
            today = timezone.now().date()
            edad = today.year - paciente.fecha_nacimiento.year - ((today.month, today.day) < (paciente.fecha_nacimiento.month, paciente.fecha_nacimiento.day))

        # Obtener diagnósticos del paciente
        diagnosticos = paciente.diagnosticos.all()  # Asegúrate de que la relación esté definida correctamente

    citas = paciente.citas.all() if paciente else []
    recetas = paciente.recetas.all() if paciente else []
    estado = EstadoPaciente.objects.filter(paciente=paciente).first() if paciente else None

    return render(request, 'medico/historial_unico.html', {
        'pacientes': pacientes,
        'paciente': paciente,
        'edad': edad,
        'diagnosticos': diagnosticos,  # Pasar diagnósticos al contexto
        'citas': citas,
        'recetas': recetas,
        'estado': estado,
    })



def nueva_receta(request):
    if request.method == 'POST':
        form = NuevaRecetaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Receta registrada correctamente.')
            return redirect('/nueva_receta')  # Redirige a la misma página para limpiar el formulario
        else:
             messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = NuevaRecetaForm()
    return render(request, 'medico/nueva_receta.html', {'form': form})

def perfilmedico(request):
    # Supongamos que ya tienes un usuario autenticado
    medicos = Medico.objects.get(usuario=request.user)
      # Obtén el paciente asociado al usuario
    return render(request, 'medico/perfilmedico.html', {'medicos': medicos})
#*******************************************************
def iniciomedico(request):
    return render(request,'medico/iniciomedico.html')

def principal(request):
    return render(request,'principal.html')



#-------------vistas de inicio y registro  de ususrios--------------#

def registroFallido(request):
    return render(request,'registroFallido.html')

def iniciarSesion(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login_input = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Intentar autenticar primero con nombre de usuario
            user = authenticate(request, username=login_input, password=password)

            # Si no se encontró un usuario, intentar autenticar con correo electrónico
            if user is None:
                try:
                    user = User.objects.get(email=login_input)
                    user = authenticate(request, username=user.username, password=password)
                except User.DoesNotExist:
                    user = None

            if user is not None:
                login(request, user)

                perfil = Perfil.objects.get(user=user)  # Obtener el perfil del usuario
                # Redirigir según el tipo de usuario
                if perfil.tipo_usuario == 'administrador':
                    return redirect('admin_dashboard')
                elif perfil.tipo_usuario == 'medico':
                    return redirect('medico_dashboard')
                elif perfil.tipo_usuario == 'paciente':
                    return redirect('paciente_dashboard')
                else:
                    return redirect('inicio')
            else:
                messages.error(request, "Nombre de usuario o contraseña incorrectos.")
    else:
        form = CustomAuthenticationForm()

    # Asegúrate de que siempre se devuelva un objeto HttpResponse
    return render(request, 'iniciarSesion.html', {'form': form})
        
    #return render(request,'iniciarSesion.html')
#




class PacienteView( viewsets.ModelViewSet):
    serializer_class = PacienteSerializer
    queryset = Paciente.objects.all()

class MedicoView( viewsets.ModelViewSet):
    serializer_class = MedicoSerializer
    queryset = Medico.objects.all()

class EspecialidadView( viewsets.ModelViewSet):
    serializer_class = EspecialidadSerializer
    queryset = Especialidad.objects.all()



class CitaMedicaView( viewsets.ModelViewSet):
    serializer_class = CitaMedicaSerializer
    queryset = CitaMedica.objects.all()

class HistorialMedicoView( viewsets.ModelViewSet):
    serializer_class = HistorialMedicoSerializer
    queryset = HistorialMedico.objects.all()