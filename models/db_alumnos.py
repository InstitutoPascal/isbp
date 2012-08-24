# coding: utf8

TIPOS_DOCUMENTO = ['DNI', 'LE', 'LC', 'CI', 'PA']
SEXOS = ['M', 'F']

db.define_table('alumno',
    Field('user_id', db.auth_user, default=auth.user_id, 
          readable=False, writable=False),
    Field('fecha_alta', 'date', default=request.now.date,
          readable=True, writable=False),
    Field('foto', 'upload'),
    Field('legajo', 'integer'),
    # Datos personales
    Field('tipo_doc', 'string'),
    Field('nro_doc', 'string'),
    Field('fec_nac', 'date'),
    Field('sexo', 'string', requires=IS_IN_SET(SEXOS)),
    Field('nacionalidad', 'string'),
    # ...    
    # Otros Datos  
    Field('documentacion_ok', 'boolean',  
          readable=False, writable=False),
    Field('situacion_arancelaria_ok', 'boolean', 
          readable=False, writable=False),
    # Datos familiares generales
    Field('padres_viven_juntos', 'boolean'),
    Field('padres_estan_casados', 'boolean'),
    # Datos varios
    Field('autorizo_publicacion', 'boolean',
          comment='de trabajos de mi autoría, como así tambien mi foto ...'),
    )

db.alumno.tipo_doc.requires = IS_IN_SET(TIPOS_DOCUMENTO)

# Estudios de Nivel Medio:
db.define_table('estudios',
    Field('alumno_id', db.alumno),
    Field('nivel', 'string'),
    Field('titulo', 'string'),
    Field('egreso', 'date'),
    Field('cant_materias_adeuda', 'integer'),
    Field('nombre_establecimiento', 'string'),
    Field('cp', 'string'),
    Field('provincia', 'string'),
    Field('pais', 'string'),
    )

NIVELES_ESTUDIO = ['primario', 'secundario', 'terciario', 'universitario']
db.estudios.nivel.requires = IS_IN_SET(NIVELES_ESTUDIO)

# Actividad Laboral
db.define_table('actividad_laboral',
    Field('alumno_id', db.alumno),
    Field('ocupacion', 'string'),
    Field('empresa', 'string'),
    Field('cant_horas_semanales', 'integer'),
    # COMPLETAR POR LOS ESTUDIANT DEL ISBPL PARA EL JUEVES QUE VIENE...
    )

OCUPACIONES = ['Independiente', 'Empresario', 'Empleado', 'No Trabaja']
db.actividad_laboral.ocupacion.requires=IS_IN_SET(OCUPACIONES)

# Si el aspirante es menor de 18 años:
db.define_table('familiar',
    Field('alumno_id', db.alumno),
    Field('nombre'),
    Field('parentesco'),
    Field('tipo_doc'),
    Field('nro_doc'),
    Field('calle'),
    Field('direccion'),
    # ....
    )

PARENTESCOS = ['Responsable', 'Padre', 'Madre', 'Tutor', 'Encargado']
db.familiar.parentesco.requires = IS_IN_SET(PARENTESCOS)
db.familiar.tipo_doc.requires = IS_IN_SET(TIPOS_DOCUMENTO)
