# coding: utf8
# try something like
def index():
    form = SQLFORM.factory(
        Field('comision_id', db.comision, 
              requires=IS_IN_DB(db, db.comision.id, lambda x: "%(nombre)s" % db.materia[x.materia_id]))
        )
    if form.accepts(request.vars, session):
        redirect(URL(f='listado', args=[form.vars.comision_id]))
    return dict(form=form)
    
def listado():
    # obtengo el primer parametro de la URL:
    comision_id = request.args[0]
    # busco los registros de comision y materia:
    comision = db.comision[comision_id]
    materia = db.materia[comision.materia_id]
    ##docente = db.docente[comision.docente_id]
    # busco los horarios
    horarios = db(db.horario.comision_id == comision_id).select()
    # busco los alumnos que cursan la materia
    q = db.cursa.comision_id == comision_id
    q &= db.alumno.id == db.cursa.alumno_id
    q &= db.auth_user.id == db.alumno.user_id
    filas_alumnos = db(q).select(db.cursa.alumno_id, 
                           db.auth_user.first_name, 
                           db.auth_user.last_name)
    # busco si hay registros de asistencia para hoy:
    q = db.asistencia.comision_id == comision_id
    q &= db.asistencia.fecha == request.now.date()
    filas_asistencia = db(q).select()
    # armo una lista para saber los alumnos que vinieron:
    listas_asistencia = [fila.alumno_id for fila in filas_asistencia]
    
    # procesamos el formulario si hay datos:
    if request.vars.completo == 'si':
        # borramos todas las asistencias para esta fecha
        q = db.asistencia.comision_id==comision_id
        q &= db.asistencia.fecha == request.now.date()
        db(q).delete()
        for clave, valor in request.vars.items():
            # en clave vamos a tener el nombre de cada casillero
            # ej "check_alumno_id.1"
            # y en valor, 'on' si fue seleccionado
            if '.' in clave:
                pos_punto = clave.index(".")
                alumno_id = clave[pos_punto+1:]
                if valor == 'on':
                    db.asistencia.insert(
                        alumno_id=alumno_id,
                        fecha=request.now.date(),
                        comision_id=comision_id,
                        )
    else:
        response.flash = "no tecleaste nada macho"
        
    return {'filas_alumnos': filas_alumnos, 
            'comision': comision, 
            'materia': materia,
            'listas_asistencia': listas_asistencia,
            ##'docente': docente,
            'horarios': horarios,
            }
            

def consulta():
   if request.args:
       # convierto la url (string) a un entero:
       nro_pagina = int(request.args[0])
   else:
       nro_pagina = 0
   registros_por_pagina = 2
   
   # creo el formulario de consulta:
   form = SQLFORM.factory(
        Field("alumno_id", db.alumno, 
              requires=IS_EMPTY_OR(IS_IN_DB(db, db.alumno, 
                  lambda x: "%(last_name)s, %(first_name)s" % db.auth_user[x.user_id]))),
        Field("fecha_desde", "date"),
        Field("fecha_hasta", "date"),
        Field("comision_id", db.comision , requires=IS_EMPTY_OR(IS_IN_DB(db, db.comision, 
                  lambda x: "%(nombre)s" % db.materia[x.materia_id]))),
        )
   # creo la consulta generica base
   q = db.alumno.id==db.asistencia.alumno_id
   q &= db.comision.id==db.asistencia.comision_id
   q &= db.materia.id==db.comision.materia_id
   q &= db.alumno.user_id==db.auth_user.id

   if form.accepts(request.vars, session):
       # guardo en la sesion los datos que ingreso el usuario
       # (para poder reusarlo en futuras requerimientos -cadavezquepedimosunapagian-)
       session.alumno_id = form.vars.alumno_id
       session.comision_id = form.vars.comision_id
       session.fecha_desde = form.vars.fecha_desde
       session.fecha_hasta = form.vars.fecha_hasta

   # agrego los filtros segun los datos que completo el usuario en el formulario antes mencionado:
   if session.alumno_id:
       q &= db.asistencia.alumno_id == session.alumno_id
   if session.comision_id:
       q &= db.asistencia.comision_id == session.comision_id
   if session.fecha_desde:
       q &= db.asistencia.fecha >= session.fecha_desde
   if session.fecha_hasta:
       q &= db.asistencia.fecha <= session.fecha_hasta
   
   # pagino los resultados:
   inicio = nro_pagina * registros_por_pagina
   fin = inicio + registros_por_pagina
   
   # obtengo la cantidad de paginas:
   cant_registros = db(q).count()
   cant_paginas = cant_registros / registros_por_pagina 
   
   # ejecutamos la consulta, obtengo los registros ordenados:
   registros = db(q).select(orderby=db.asistencia.id, 
                            limitby=(inicio, fin),
                            )

   return dict(form=form, 
               registros=registros, 
               nro_pagina=nro_pagina, 
               cant_paginas=cant_paginas)
