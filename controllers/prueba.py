# coding: utf8
# intente algo como

def index(): 
    session.saraza = 5678
    redirect(URL('prueba', args=['a', '123', 'bcd'], vars={'perro': 12, 'gato': 'xd'}))

    # arma la url: /prueba/a/123/bcd?gato=xd&perro=12

def prueba():
    primer_arg = request.args[0] # == 'a'
    segund_arg = request.args[1] # == '123'
    variable1 = request.vars['perro'] # == '12'
    variable2 = request.vars['gato'] # == 'xd'

    print session.saraza # imprime 5678
    
    return {'args': request.args,
            'vars': request.vars,
            'saraza': session.saraza,
            }
