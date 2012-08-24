# coding: utf8

db.define_table('docente',
    Field('user_id', db.auth_user, default=auth.user_id, 
          readable=False, writable=False),
    Field('fecha_alta', 'date', default=request.now.date,
          readable=True, writable=False),
    Field('foto', 'upload'),
    )
