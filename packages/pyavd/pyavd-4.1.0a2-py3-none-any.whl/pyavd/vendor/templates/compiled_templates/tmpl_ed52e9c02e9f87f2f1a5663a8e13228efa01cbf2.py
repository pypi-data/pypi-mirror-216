from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/router-general.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_router_general = resolve('router_general')
    l_0_delimiter = resolve('delimiter')
    try:
        t_1 = environment.filters['arista.avd.natural_sort']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.natural_sort' found.")
    try:
        t_2 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_2((undefined(name='router_general') if l_0_router_general is missing else l_0_router_general)):
        pass
        yield '!\nrouter general\n'
        l_0_delimiter = False
        context.vars['delimiter'] = l_0_delimiter
        context.exported_vars.add('delimiter')
        if t_2(environment.getattr(environment.getattr((undefined(name='router_general') if l_0_router_general is missing else l_0_router_general), 'router_id'), 'ipv4')):
            pass
            yield '   router-id ipv4 '
            yield str(environment.getattr(environment.getattr((undefined(name='router_general') if l_0_router_general is missing else l_0_router_general), 'router_id'), 'ipv4'))
            yield '\n'
            l_0_delimiter = True
            context.vars['delimiter'] = l_0_delimiter
            context.exported_vars.add('delimiter')
        if t_2(environment.getattr(environment.getattr((undefined(name='router_general') if l_0_router_general is missing else l_0_router_general), 'router_id'), 'ipv6')):
            pass
            yield '   router-id ipv6 '
            yield str(environment.getattr(environment.getattr((undefined(name='router_general') if l_0_router_general is missing else l_0_router_general), 'router_id'), 'ipv6'))
            yield '\n'
            l_0_delimiter = True
            context.vars['delimiter'] = l_0_delimiter
            context.exported_vars.add('delimiter')
        if t_2(environment.getattr((undefined(name='router_general') if l_0_router_general is missing else l_0_router_general), 'nexthop_fast_failover'), True):
            pass
            yield '   hardware next-hop fast-failover\n'
            l_0_delimiter = True
            context.vars['delimiter'] = l_0_delimiter
            context.exported_vars.add('delimiter')
        if (t_2((undefined(name='delimiter') if l_0_delimiter is missing else l_0_delimiter), True) and t_2(environment.getattr((undefined(name='router_general') if l_0_router_general is missing else l_0_router_general), 'vrfs'))):
            pass
            yield '   !\n'
        for l_1_vrf in t_1(environment.getattr((undefined(name='router_general') if l_0_router_general is missing else l_0_router_general), 'vrfs'), 'name'):
            _loop_vars = {}
            pass
            yield '   vrf '
            yield str(environment.getattr(l_1_vrf, 'name'))
            yield '\n'
            for l_2_leak_route in t_1(environment.getattr(l_1_vrf, 'leak_routes')):
                _loop_vars = {}
                pass
                if (t_2(environment.getattr(l_2_leak_route, 'source_vrf')) and t_2(environment.getattr(l_2_leak_route, 'subscribe_policy'))):
                    pass
                    yield '      leak routes source-vrf '
                    yield str(environment.getattr(l_2_leak_route, 'source_vrf'))
                    yield ' subscribe-policy '
                    yield str(environment.getattr(l_2_leak_route, 'subscribe_policy'))
                    yield '\n'
            l_2_leak_route = missing
            for l_2_dynamic_prefix_list in t_1(environment.getattr(environment.getattr(l_1_vrf, 'routes'), 'dynamic_prefix_lists'), 'name'):
                _loop_vars = {}
                pass
                if t_2(environment.getattr(l_2_dynamic_prefix_list, 'name')):
                    pass
                    yield '      routes dynamic prefix-list '
                    yield str(environment.getattr(l_2_dynamic_prefix_list, 'name'))
                    yield '\n'
            l_2_dynamic_prefix_list = missing
            yield '      exit\n   !\n'
        l_1_vrf = missing
        yield '   exit\n'

blocks = {}
debug_info = '2=25&5=28&6=31&7=34&8=36&10=39&11=42&12=44&14=47&16=50&18=53&21=56&22=60&23=62&24=65&25=68&28=73&29=76&30=79'