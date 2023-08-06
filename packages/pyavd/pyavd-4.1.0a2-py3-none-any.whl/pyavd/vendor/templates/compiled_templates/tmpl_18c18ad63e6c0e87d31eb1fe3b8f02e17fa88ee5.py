from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/ntp.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_ntp = resolve('ntp')
    l_0_ntp_int_cli = resolve('ntp_int_cli')
    try:
        t_1 = environment.filters['arista.avd.hide_passwords']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.hide_passwords' found.")
    try:
        t_2 = environment.filters['arista.avd.natural_sort']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.natural_sort' found.")
    try:
        t_3 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_3((undefined(name='ntp') if l_0_ntp is missing else l_0_ntp)):
        pass
        yield '!\n'
        for l_1_authentication_key in t_2(environment.getattr((undefined(name='ntp') if l_0_ntp is missing else l_0_ntp), 'authentication_keys'), 'id'):
            l_1_ntp_auth_key_cli = resolve('ntp_auth_key_cli')
            l_1_hide_passwords = resolve('hide_passwords')
            _loop_vars = {}
            pass
            if ((t_3(environment.getattr(l_1_authentication_key, 'id')) and t_3(environment.getattr(l_1_authentication_key, 'key'))) and t_3(environment.getattr(l_1_authentication_key, 'hash_algorithm'))):
                pass
                l_1_ntp_auth_key_cli = str_join(('ntp authentication-key ', environment.getattr(l_1_authentication_key, 'id'), ' ', environment.getattr(l_1_authentication_key, 'hash_algorithm'), ))
                _loop_vars['ntp_auth_key_cli'] = l_1_ntp_auth_key_cli
                if t_3(environment.getattr(l_1_authentication_key, 'key_type')):
                    pass
                    l_1_ntp_auth_key_cli = str_join(((undefined(name='ntp_auth_key_cli') if l_1_ntp_auth_key_cli is missing else l_1_ntp_auth_key_cli), ' ', environment.getattr(l_1_authentication_key, 'key_type'), ))
                    _loop_vars['ntp_auth_key_cli'] = l_1_ntp_auth_key_cli
                l_1_ntp_auth_key_cli = str_join(((undefined(name='ntp_auth_key_cli') if l_1_ntp_auth_key_cli is missing else l_1_ntp_auth_key_cli), ' ', t_1(environment.getattr(l_1_authentication_key, 'key'), (undefined(name='hide_passwords') if l_1_hide_passwords is missing else l_1_hide_passwords)), ))
                _loop_vars['ntp_auth_key_cli'] = l_1_ntp_auth_key_cli
                yield str((undefined(name='ntp_auth_key_cli') if l_1_ntp_auth_key_cli is missing else l_1_ntp_auth_key_cli))
                yield '\n'
        l_1_authentication_key = l_1_ntp_auth_key_cli = l_1_hide_passwords = missing
        if t_3(environment.getattr((undefined(name='ntp') if l_0_ntp is missing else l_0_ntp), 'trusted_keys')):
            pass
            yield 'ntp trusted-key '
            yield str(environment.getattr((undefined(name='ntp') if l_0_ntp is missing else l_0_ntp), 'trusted_keys'))
            yield '\n'
        if t_3(environment.getattr((undefined(name='ntp') if l_0_ntp is missing else l_0_ntp), 'authenticate_servers_only'), True):
            pass
            yield 'ntp authenticate servers\n'
        elif t_3(environment.getattr((undefined(name='ntp') if l_0_ntp is missing else l_0_ntp), 'authenticate'), True):
            pass
            yield 'ntp authenticate\n'
        if t_3(environment.getattr(environment.getattr((undefined(name='ntp') if l_0_ntp is missing else l_0_ntp), 'local_interface'), 'name')):
            pass
            l_0_ntp_int_cli = 'ntp local-interface'
            context.vars['ntp_int_cli'] = l_0_ntp_int_cli
            context.exported_vars.add('ntp_int_cli')
            if (t_3(environment.getattr(environment.getattr((undefined(name='ntp') if l_0_ntp is missing else l_0_ntp), 'local_interface'), 'vrf')) and (environment.getattr(environment.getattr((undefined(name='ntp') if l_0_ntp is missing else l_0_ntp), 'local_interface'), 'vrf') != 'default')):
                pass
                l_0_ntp_int_cli = str_join(((undefined(name='ntp_int_cli') if l_0_ntp_int_cli is missing else l_0_ntp_int_cli), ' vrf ', environment.getattr(environment.getattr((undefined(name='ntp') if l_0_ntp is missing else l_0_ntp), 'local_interface'), 'vrf'), ))
                context.vars['ntp_int_cli'] = l_0_ntp_int_cli
                context.exported_vars.add('ntp_int_cli')
            l_0_ntp_int_cli = str_join(((undefined(name='ntp_int_cli') if l_0_ntp_int_cli is missing else l_0_ntp_int_cli), ' ', environment.getattr(environment.getattr((undefined(name='ntp') if l_0_ntp is missing else l_0_ntp), 'local_interface'), 'name'), ))
            context.vars['ntp_int_cli'] = l_0_ntp_int_cli
            context.exported_vars.add('ntp_int_cli')
            yield str((undefined(name='ntp_int_cli') if l_0_ntp_int_cli is missing else l_0_ntp_int_cli))
            yield '\n'
        for l_1_server in t_2(environment.getattr((undefined(name='ntp') if l_0_ntp is missing else l_0_ntp), 'servers'), 'name'):
            l_1_ntp_server_cli = resolve('ntp_server_cli')
            l_1_hide_passwords = resolve('hide_passwords')
            _loop_vars = {}
            pass
            if t_3(environment.getattr(l_1_server, 'name')):
                pass
                l_1_ntp_server_cli = 'ntp server'
                _loop_vars['ntp_server_cli'] = l_1_ntp_server_cli
                if (t_3(environment.getattr(l_1_server, 'vrf')) and (environment.getattr(l_1_server, 'vrf') != 'default')):
                    pass
                    l_1_ntp_server_cli = str_join(((undefined(name='ntp_server_cli') if l_1_ntp_server_cli is missing else l_1_ntp_server_cli), ' vrf ', environment.getattr(l_1_server, 'vrf'), ))
                    _loop_vars['ntp_server_cli'] = l_1_ntp_server_cli
                l_1_ntp_server_cli = str_join(((undefined(name='ntp_server_cli') if l_1_ntp_server_cli is missing else l_1_ntp_server_cli), ' ', environment.getattr(l_1_server, 'name'), ))
                _loop_vars['ntp_server_cli'] = l_1_ntp_server_cli
                if t_3(environment.getattr(l_1_server, 'preferred'), True):
                    pass
                    l_1_ntp_server_cli = str_join(((undefined(name='ntp_server_cli') if l_1_ntp_server_cli is missing else l_1_ntp_server_cli), ' prefer', ))
                    _loop_vars['ntp_server_cli'] = l_1_ntp_server_cli
                if t_3(environment.getattr(l_1_server, 'burst'), True):
                    pass
                    l_1_ntp_server_cli = str_join(((undefined(name='ntp_server_cli') if l_1_ntp_server_cli is missing else l_1_ntp_server_cli), ' burst', ))
                    _loop_vars['ntp_server_cli'] = l_1_ntp_server_cli
                if t_3(environment.getattr(l_1_server, 'iburst'), True):
                    pass
                    l_1_ntp_server_cli = str_join(((undefined(name='ntp_server_cli') if l_1_ntp_server_cli is missing else l_1_ntp_server_cli), ' iburst', ))
                    _loop_vars['ntp_server_cli'] = l_1_ntp_server_cli
                if t_3(environment.getattr(l_1_server, 'version')):
                    pass
                    l_1_ntp_server_cli = str_join(((undefined(name='ntp_server_cli') if l_1_ntp_server_cli is missing else l_1_ntp_server_cli), ' version ', environment.getattr(l_1_server, 'version'), ))
                    _loop_vars['ntp_server_cli'] = l_1_ntp_server_cli
                if t_3(environment.getattr(l_1_server, 'minpoll')):
                    pass
                    l_1_ntp_server_cli = str_join(((undefined(name='ntp_server_cli') if l_1_ntp_server_cli is missing else l_1_ntp_server_cli), ' minpoll ', environment.getattr(l_1_server, 'minpoll'), ))
                    _loop_vars['ntp_server_cli'] = l_1_ntp_server_cli
                if t_3(environment.getattr(l_1_server, 'maxpoll')):
                    pass
                    l_1_ntp_server_cli = str_join(((undefined(name='ntp_server_cli') if l_1_ntp_server_cli is missing else l_1_ntp_server_cli), ' maxpoll ', environment.getattr(l_1_server, 'maxpoll'), ))
                    _loop_vars['ntp_server_cli'] = l_1_ntp_server_cli
                if t_3(environment.getattr(l_1_server, 'local_interface')):
                    pass
                    l_1_ntp_server_cli = str_join(((undefined(name='ntp_server_cli') if l_1_ntp_server_cli is missing else l_1_ntp_server_cli), ' local-interface ', environment.getattr(l_1_server, 'local_interface'), ))
                    _loop_vars['ntp_server_cli'] = l_1_ntp_server_cli
                if t_3(environment.getattr(l_1_server, 'key')):
                    pass
                    l_1_ntp_server_cli = str_join(((undefined(name='ntp_server_cli') if l_1_ntp_server_cli is missing else l_1_ntp_server_cli), ' key ', t_1(environment.getattr(l_1_server, 'key'), (undefined(name='hide_passwords') if l_1_hide_passwords is missing else l_1_hide_passwords)), ))
                    _loop_vars['ntp_server_cli'] = l_1_ntp_server_cli
                yield str((undefined(name='ntp_server_cli') if l_1_ntp_server_cli is missing else l_1_ntp_server_cli))
                yield '\n'
        l_1_server = l_1_ntp_server_cli = l_1_hide_passwords = missing

blocks = {}
debug_info = '2=31&4=34&5=39&8=41&9=43&10=45&12=47&13=49&16=52&17=55&19=57&21=60&24=63&25=65&26=68&27=70&29=73&30=76&32=78&33=83&34=85&35=87&36=89&38=91&39=93&40=95&42=97&43=99&45=101&46=103&48=105&49=107&51=109&52=111&54=113&55=115&57=117&58=119&60=121&61=123&63=125'