# coding: utf8

db.define_table('carrera',
    Field('id', 'id'),
    Field('titulo', 'string'),
    Field('alcance', 'text'),
    )

db.define_table('plan_estudio',
    Field('carrera_id', db.carrera),
    Field('resolucion', 'string'),
    )

db.define_table('materia',
    Field('id', 'id'),
    Field('cplan_estudio_id', db.plan_estudio),
    Field('nombre', 'string'),
    Field('carga_horaria', 'integer'),
    Field('anio', 'integer'),
    Field('cuatrimestre', 'integer'),
    )

db.define_table('correlativa',
    Field('materia_id', db.materia),
    Field('materia_id_previa', db.materia),
    Field('tipo', 'string'), # A:aprobada, C: cursada
    )
    
db.define_table('comision',
    Field('id', 'id'),
    Field('materia_id', db.materia),
    Field('turno', 'string'), # M, T, N
    Field('anio', 'integer'), # 2012, 2013
    )

db.define_table('horario',
    Field('comision_id', db.comision),
    Field('dia_semana', 'integer'), # 0: dom, 1: lun, ...
    Field('hora', 'time'),
    )

db.define_table('dicta',
    Field('docente_id', db.docente),
    Field('comision_id', db.comision),
    )

db.define_table('cursa',
    Field('alumno_id', db.alumno),
    Field('comision_id', db.comision),
    Field('condicion', 'string'), # Libre, Regular
    )

db.define_table('examen',
    Field('materia_id', db.materia),
    Field('fecha', 'date'),
    Field('libro', 'integer'),
    Field('folio', 'integer'),
    Field('condicion', 'string'), # Libre, Regular
    )

db.define_table('XXYY',
    Field('docente_id', db.docente),
    Field('examen_id', db.examen),
    Field('cargo', 'string'), # Titular, Vocal, Suplente
    )

db.define_table('rinde',
    Field('alumno_id', db.alumno),
    Field('examen_id', db.examen),
    )
    
db.define_table('nota',
    Field('tipo', 'string'), # Parcial, Recuperatorio, Integrador, Final
    Field('periodo', 'integer'), # 1°q, 2°q
    Field('valor', 'double'),
    Field('fecha', 'date'),    
    )
