from django.contrib import admin
from.models import Paciente, Medico, Especialidad, CitaMedica, HistorialMedico, Receta, Notificacion,Reporte, FormularioSatisfaccion, Factura, Medicamento
# Register your models here.
admin.site.register(Paciente)

admin.site.register(Medico)
admin.site.register(Especialidad)
admin.site.register(CitaMedica)
admin.site.register(HistorialMedico)
admin.site.register(Receta)
admin.site.register(Notificacion)
admin.site.register(Reporte)
admin.site.register(FormularioSatisfaccion)
admin.site.register(Factura)
admin.site.register(Medicamento)
