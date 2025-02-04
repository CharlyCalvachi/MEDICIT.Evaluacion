from django.urls import path, include
from  medicitas import views
from rest_framework import routers 
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.documentation import include_docs_urls
router=routers.DefaultRouter()
router.register(r'paciente', views.PacienteView,'paciente')
router.register(r'medico', views.MedicoView,'medico')
router.register(r'especialidad', views.EspecialidadView,'especialidad')
router.register(r'citaMedica', views.CitaMedicaView,'citaMedica')
router.register(r'historialMedico', views.HistorialMedicoView,'HistorialMedico')


urlpatterns = [
    path('iniciarSesion/', views.iniciarSesion),
    path('registro/', views.registro, name='registro'),
    path('registroFallido/', views.registroFallido),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('medico-dashboard/', views.medico_dashboard, name='medico_dashboard'),
    path('paciente-dashboard/', views.paciente_dashboard, name='paciente_dashboard'),
    path('api/v1/', include(router.urls)),

    #***************URLs de  medicos***********# 
    path('iniciomedico/', views.iniciomedico),
    path('citasprogramadas/', views.citasprogramadas),
    path('citasprogramadas/', views.citasprogramadas),
    path('actualizar_estado_cita/<int:cita_id>/', views.actualizar_estado_cita, name='actualizar_estado_cita'),
    path('historialesmedicos/', views.historialesmedicos),
    path('historial_medico/', views.historial_medico),
    path('crear_diagnostico/', views.crear_diagnostico),
    path('historial/', views.historial_unico),
    path('gestionar_estado_paciente/', views.gestionar_estado_paciente),
    path('editar_estado_paciente/<int:estado_id>/', views.editar_estado_paciente, name='editar_estado_paciente'),
    path('nueva_receta/', views.nueva_receta),
    path('perfilmedico/', views.perfilmedico),


    #*****************URLs Pacientes***********#
    path('citas/eliminar/<int:cita_id>/', views.eliminar_cita, name='eliminar_cita'),
    path('editarCita/', views.editarCita, name='editarCita'),
    path('principal/', views.principal),
    path('perfil/', views.perfil),
    path('inicio/', views.inicio),
    path('medicos/', views.medicos),
    path('agendarCita/', views.agendarCita),
    path('citasAgendadas/', views.citasAgendadas),
    path('registrar-cita/', views.registrarCita, name='registrar_cita'),
    path('api/medicos/<int:especialidad_id>/', views.cargarMedicos, name='cargar_medicos'),
    path('api/disponibilidad/<int:medico_id>/<str:fecha>/', views.cargarDisponibilidad, name='cargar_disponibilidad'),

    #*****************URLs administrador***********#
    path('perfiladministrador/', views.perfiladministrador),
    path('registrarEspecialidad/', views.registrarEspecialidad),
    path('registrarMedico/', views.registrarMedico),
    path('registrarMedicamento/', views.registrarMedicamento),
    path('editar-especialidad/<int:id>/', views.editarEspecialidad, name='editar_especialidad'),
    path('eliminar-especialidad/<int:id>/', views.eliminarEspecialidad, name='eliminar_especialidad'),
    path('editarMedico/<int:medico_id>/', views.editarMedico, name='editar_medico'),
    path('eliminarMedico/<int:medico_id>/', views.eliminarMedico, name='eliminar_medico'),
    path('editar-medicamento/<int:id>/', views.editarMedicamento, name='editar_medicamento'),
    path('eliminar-medicamento/<int:id>/', views.eliminarMedicamento, name='eliminar_medicamento'),
    path('reportesHospital/', views.reportesHospital),
    path('reporte/', views.generar_reporte),
   


    #path('docsapi/', include_docs_urls(title='Medicitas API')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
