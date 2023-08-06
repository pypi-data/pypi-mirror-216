from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/static-routes.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_static_routes = resolve('static_routes')
    try:
        t_1 = environment.filters['capitalize']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'capitalize' found.")
    try:
        t_2 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_2((undefined(name='static_routes') if l_0_static_routes is missing else l_0_static_routes)):
        pass
        yield '!\n'
        for l_1_static_route in (undefined(name='static_routes') if l_0_static_routes is missing else l_0_static_routes):
            l_1_static_route_cli = missing
            _loop_vars = {}
            pass
            l_1_static_route_cli = 'ip route'
            _loop_vars['static_route_cli'] = l_1_static_route_cli
            if (t_2(environment.getattr(l_1_static_route, 'vrf')) and (environment.getattr(l_1_static_route, 'vrf') != 'default')):
                pass
                l_1_static_route_cli = str_join(((undefined(name='static_route_cli') if l_1_static_route_cli is missing else l_1_static_route_cli), ' vrf ', environment.getattr(l_1_static_route, 'vrf'), ))
                _loop_vars['static_route_cli'] = l_1_static_route_cli
            if t_2(environment.getattr(l_1_static_route, 'destination_address_prefix')):
                pass
                l_1_static_route_cli = str_join(((undefined(name='static_route_cli') if l_1_static_route_cli is missing else l_1_static_route_cli), ' ', environment.getattr(l_1_static_route, 'destination_address_prefix'), ))
                _loop_vars['static_route_cli'] = l_1_static_route_cli
            if t_2(environment.getattr(l_1_static_route, 'interface')):
                pass
                l_1_static_route_cli = str_join(((undefined(name='static_route_cli') if l_1_static_route_cli is missing else l_1_static_route_cli), ' ', t_1(environment.getattr(l_1_static_route, 'interface')), ))
                _loop_vars['static_route_cli'] = l_1_static_route_cli
            if t_2(environment.getattr(l_1_static_route, 'gateway')):
                pass
                l_1_static_route_cli = str_join(((undefined(name='static_route_cli') if l_1_static_route_cli is missing else l_1_static_route_cli), ' ', environment.getattr(l_1_static_route, 'gateway'), ))
                _loop_vars['static_route_cli'] = l_1_static_route_cli
                if t_2(environment.getattr(l_1_static_route, 'track_bfd'), True):
                    pass
                    l_1_static_route_cli = str_join(((undefined(name='static_route_cli') if l_1_static_route_cli is missing else l_1_static_route_cli), ' track bfd', ))
                    _loop_vars['static_route_cli'] = l_1_static_route_cli
            if t_2(environment.getattr(l_1_static_route, 'distance')):
                pass
                l_1_static_route_cli = str_join(((undefined(name='static_route_cli') if l_1_static_route_cli is missing else l_1_static_route_cli), ' ', environment.getattr(l_1_static_route, 'distance'), ))
                _loop_vars['static_route_cli'] = l_1_static_route_cli
            if t_2(environment.getattr(l_1_static_route, 'tag')):
                pass
                l_1_static_route_cli = str_join(((undefined(name='static_route_cli') if l_1_static_route_cli is missing else l_1_static_route_cli), ' tag ', environment.getattr(l_1_static_route, 'tag'), ))
                _loop_vars['static_route_cli'] = l_1_static_route_cli
            if t_2(environment.getattr(l_1_static_route, 'name')):
                pass
                l_1_static_route_cli = str_join(((undefined(name='static_route_cli') if l_1_static_route_cli is missing else l_1_static_route_cli), ' name ', environment.getattr(l_1_static_route, 'name'), ))
                _loop_vars['static_route_cli'] = l_1_static_route_cli
            if t_2(environment.getattr(l_1_static_route, 'metric')):
                pass
                l_1_static_route_cli = str_join(((undefined(name='static_route_cli') if l_1_static_route_cli is missing else l_1_static_route_cli), ' metric ', environment.getattr(l_1_static_route, 'metric'), ))
                _loop_vars['static_route_cli'] = l_1_static_route_cli
            yield str((undefined(name='static_route_cli') if l_1_static_route_cli is missing else l_1_static_route_cli))
            yield '\n'
        l_1_static_route = l_1_static_route_cli = missing

blocks = {}
debug_info = '2=24&4=27&5=31&6=33&7=35&9=37&10=39&12=41&13=43&15=45&16=47&17=49&18=51&21=53&22=55&24=57&25=59&27=61&28=63&30=65&31=67&33=69'