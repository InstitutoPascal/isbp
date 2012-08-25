# coding: utf8
# intente algo como

@auth.requires_login()
def index():
    response.view = "generic.html"
    # buscar si el usuario completo la ficha de alumno:
    q = db.alumno.user_id == auth.user_id
    alumno = db(q).select(db.alumno.id).first()
    if alumno is not None:
        # crear la ficha de alumno
        session.alumno_id = alumno.id
    redirect(URL('ficha_alumno'))

@auth.requires_login()
def ficha_alumno():
    response.view = "generic.html"
    # TODO: agregar seguridad (que el alumno solo pueda ver su ficha)
    if session.alumno_id:
        # si el alumno tiene creada ficha, la busco:
        alumno_id = session.alumno_id
        alumno = db(db.alumno.id==alumno_id).select().first()
    else:
        # creo nuevo registro en blanco:
        alumno = None

    form = SQLFORM(db.alumno, alumno)
    if form.accepts(request.vars, session):
        session.flash = "Ficha actualizada..."
        redirect(URL("ficha_estudios"))
    elif form.errors:
        response.flash = "Tiene errores!"
    else:
        response.flash = "Complete los datos"
    return {'form':form}

@auth.requires_login()
def ficha_estudios():
    response.view = "generic.html"
    alumno_id = session.alumno_id
    
    # comprobar si estamos agregando o editando una ficha de estudios:
    if request.args:
        # buscar el registro existente para editarlo
        estudio_id = request.args[0]
        estudio = db(db.estudios.id == estudio_id).select().first()
    else:
        # crear un nuevo registro
        estudio = None
    
    # asignamos el id de alumno y ocultamos ese campo
    db.estudios.alumno_id.default = alumno_id
    db.estudios.alumno_id.readable = False
    db.estudios.alumno_id.writable = False

    # creo el formulario:
    form = SQLFORM(db.estudios, estudio)
    if form.accepts(request.vars, session):
        session.flash = "Ficha actualizada..."
    elif form.errors:
        response.flash = "Tiene errores!"
    else:
        response.flash = "Complete los datos"
        
    # buscamos todos los estudios del alumno:
    # (despues de procesar el formulario porque puede haber registros nuevos)
    estudios = db(db.estudios.alumno_id==alumno_id).select()
    
    # armamos un listado con cada nivel de estudio y un link para editar
    items = [LI(A("%s: %s" % (estudio.nivel, estudio.titulo),
                  _href=URL('ficha_estudios', args=[estudio.id])))
             for estudio in estudios  ]
                
    lista = UL(*items)       

    return dict(lista=lista, form=form)

@auth.requires_login()
def ficha_laboral():
    response.view = "generic.html"
    alumno_id = session.alumno_id
    
    # comprobar si estamos agregando o editando una ficha laboral:
    if request.args:
        # buscar el registro existente para editarlo
        actividad_laboral_id = request.args[0]
        actividad_laboral = db(db.actividad_laboral.id == actividad_laboral_id).select().first()
    else:
        # crear un nuevo registro
        actividad_laboral = None
    
    # asignamos el id de alumno y ocultamos ese campo
    db.actividad_laboral.alumno_id.default = alumno_id
    db.actividad_laboral.alumno_id.readable = False
    db.actividad_laboral.alumno_id.writable = False

    # creo el formulario:
    form = SQLFORM(db.actividad_laboral, actividad_laboral)
    if form.accepts(request.vars, session):
        session.flash = "Ficha actualizada..."
    elif form.errors:
        response.flash = "Tiene errores!"
    else:
        response.flash = "Complete los datos"
        
    # buscamos todos los estudios del alumno:
    # (despues de procesar el formulario porque puede haber registros nuevos)
    actividades_laboral = db(db.actividad_laboral.alumno_id==alumno_id).select()
    
    # armamos un listado con cada nivel de estudio y un link para editar
    items = [LI(A("%s" % (actividad_laboral.ocupacion, ),
                  _href=URL('ficha_laboral', args=[actividad_laboral.id])))
             for actividad_laboral in actividades_laboral  ]
                
    lista = UL(*items)       

    return dict(lista=lista, form=form)
    
@auth.requires_login()
def ficha_familiares():
    response.view = "generic.html"
    alumno_id = session.alumno_id
    
    # comprobar si estamos agregando o editando una ficha de estudios:
    if request.args:
        # buscar el registro existente para editarlo
        familiar_id = request.args[0]
        familiar = db(db.familiar.id == familiar_id).select().first()
    else:
        # crear un nuevo registro
        familiar = None
    
    # asignamos el id de alumno y ocultamos ese campo
    db.familiar.alumno_id.default = alumno_id
    db.familiar.alumno_id.readable = False
    db.familiar.alumno_id.writable = False

    # creo el formulario:
    form = SQLFORM(db.familiar, familiar)
    if form.accepts(request.vars, session):
        session.flash = "Ficha actualizada..."
    elif form.errors:
        response.flash = "Tiene errores!"
    else:
        response.flash = "Complete los datos"
        
    # buscamos todos los estudios del alumno:
    # (despues de procesar el formulario porque puede haber registros nuevos)
    familiares = db(db.familiar.alumno_id==alumno_id).select()
    
    # armamos un listado con cada nivel de estudio y un link para editar
    items = [LI(A("%s: %s" % (familiar.parentesco, familiar.nombre),
                  _href=URL('ficha_familiares', args=[familiar.id])))
             for familiar in familiares  ]
                
    lista = UL(*items)       

    return dict(lista=lista, form=form)


def solicitud():
    response.view = "generic.html"
    "al finalizar, imprimo el formulario de matriculacion completo"
    
    alumno_id = session.alumno_id
    # busco el alumno
    alumno = db(db.alumno.id==alumno_id).select().first()
    # busco los estudios
    estudios = db(db.estudios.alumno_id == alumno_id).select()
    # busco la ocupación
    actividades_laboral = db(db.actividad_laboral.alumno_id==alumno_id).select()
    # busco los familiares
    familiares = db(db.familiar.alumno_id == alumno_id).select()
    
    return dict(
            alumno=alumno,
            estudios=estudios,
            actividades_laboral=actividades_laboral,
            familiares=familiares,
            img = IMG(_src=URL(c='default', f='download', args=alumno.foto))
            )
