from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/monitor-connectivity.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_monitor_connectivity = resolve('monitor_connectivity')
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
    if t_2((undefined(name='monitor_connectivity') if l_0_monitor_connectivity is missing else l_0_monitor_connectivity)):
        pass
        yield '!\nmonitor connectivity\n'
        if t_2(environment.getattr((undefined(name='monitor_connectivity') if l_0_monitor_connectivity is missing else l_0_monitor_connectivity), 'interval')):
            pass
            yield '   interval '
            yield str(environment.getattr((undefined(name='monitor_connectivity') if l_0_monitor_connectivity is missing else l_0_monitor_connectivity), 'interval'))
            yield '\n'
        if t_2(environment.getattr((undefined(name='monitor_connectivity') if l_0_monitor_connectivity is missing else l_0_monitor_connectivity), 'shutdown'), False):
            pass
            yield '   no shutdown\n'
        elif t_2(environment.getattr((undefined(name='monitor_connectivity') if l_0_monitor_connectivity is missing else l_0_monitor_connectivity), 'shutdown'), True):
            pass
            yield '   shutdown\n'
        for l_1_interface_set in t_1(environment.getattr((undefined(name='monitor_connectivity') if l_0_monitor_connectivity is missing else l_0_monitor_connectivity), 'interface_sets'), 'name'):
            _loop_vars = {}
            pass
            if (t_2(environment.getattr(l_1_interface_set, 'name')) and t_2(environment.getattr(l_1_interface_set, 'interfaces'))):
                pass
                yield '   interface set '
                yield str(environment.getattr(l_1_interface_set, 'name'))
                yield ' '
                yield str(environment.getattr(l_1_interface_set, 'interfaces'))
                yield '\n'
        l_1_interface_set = missing
        if t_2(environment.getattr((undefined(name='monitor_connectivity') if l_0_monitor_connectivity is missing else l_0_monitor_connectivity), 'local_interfaces')):
            pass
            yield '   local-interfaces '
            yield str(environment.getattr((undefined(name='monitor_connectivity') if l_0_monitor_connectivity is missing else l_0_monitor_connectivity), 'local_interfaces'))
            yield ' address-only default\n'
        for l_1_host in t_1(environment.getattr((undefined(name='monitor_connectivity') if l_0_monitor_connectivity is missing else l_0_monitor_connectivity), 'hosts'), 'name'):
            _loop_vars = {}
            pass
            if t_2(environment.getattr(l_1_host, 'name')):
                pass
                yield '   !\n   host '
                yield str(environment.getattr(l_1_host, 'name'))
                yield '\n'
                if t_2(environment.getattr(l_1_host, 'description')):
                    pass
                    yield '      description\n      '
                    yield str(environment.getattr(l_1_host, 'description'))
                    yield '\n'
                if t_2(environment.getattr(l_1_host, 'local_interfaces')):
                    pass
                    yield '      local-interfaces '
                    yield str(environment.getattr(l_1_host, 'local_interfaces'))
                    yield ' address-only\n'
                if t_2(environment.getattr(l_1_host, 'ip')):
                    pass
                    yield '      ip '
                    yield str(environment.getattr(l_1_host, 'ip'))
                    yield '\n'
                if t_2(environment.getattr(l_1_host, 'url')):
                    pass
                    yield '      url '
                    yield str(environment.getattr(l_1_host, 'url'))
                    yield '\n'
        l_1_host = missing
        for l_1_vrf in t_1(environment.getattr((undefined(name='monitor_connectivity') if l_0_monitor_connectivity is missing else l_0_monitor_connectivity), 'vrfs'), 'name'):
            _loop_vars = {}
            pass
            if t_2(environment.getattr(l_1_vrf, 'name')):
                pass
                yield '   vrf '
                yield str(environment.getattr(l_1_vrf, 'name'))
                yield '\n'
                for l_2_interface_set in t_1(environment.getattr(l_1_vrf, 'interface_sets'), 'name'):
                    _loop_vars = {}
                    pass
                    if (t_2(environment.getattr(l_2_interface_set, 'name')) and t_2(environment.getattr(l_2_interface_set, 'interfaces'))):
                        pass
                        yield '      interface set '
                        yield str(environment.getattr(l_2_interface_set, 'name'))
                        yield ' '
                        yield str(environment.getattr(l_2_interface_set, 'interfaces'))
                        yield '\n'
                l_2_interface_set = missing
                if t_2(environment.getattr(l_1_vrf, 'local_interfaces')):
                    pass
                    yield '      local-interfaces '
                    yield str(environment.getattr(l_1_vrf, 'local_interfaces'))
                    yield ' address-only default\n'
                if t_2(environment.getattr(l_1_vrf, 'description')):
                    pass
                    yield '      description\n      '
                    yield str(environment.getattr(l_1_vrf, 'description'))
                    yield '\n'
                for l_2_host in t_1(environment.getattr(l_1_vrf, 'hosts'), 'name'):
                    _loop_vars = {}
                    pass
                    if t_2(environment.getattr(l_2_host, 'name')):
                        pass
                        yield '      !\n      host '
                        yield str(environment.getattr(l_2_host, 'name'))
                        yield '\n'
                        if t_2(environment.getattr(l_2_host, 'description')):
                            pass
                            yield '         description\n         '
                            yield str(environment.getattr(l_2_host, 'description'))
                            yield '\n'
                        if t_2(environment.getattr(l_2_host, 'local_interfaces')):
                            pass
                            yield '         local-interfaces '
                            yield str(environment.getattr(l_2_host, 'local_interfaces'))
                            yield ' address-only\n'
                        if t_2(environment.getattr(l_2_host, 'ip')):
                            pass
                            yield '         ip '
                            yield str(environment.getattr(l_2_host, 'ip'))
                            yield '\n'
                        if t_2(environment.getattr(l_2_host, 'url')):
                            pass
                            yield '         url '
                            yield str(environment.getattr(l_2_host, 'url'))
                            yield '\n'
                l_2_host = missing
        l_1_vrf = missing

blocks = {}
debug_info = '2=24&5=27&6=30&8=32&10=35&13=38&14=41&15=44&18=49&19=52&21=54&22=57&24=60&25=62&27=65&29=67&30=70&32=72&33=75&35=77&36=80&40=83&41=86&42=89&43=91&44=94&45=97&48=102&49=105&51=107&53=110&55=112&56=115&58=118&59=120&61=123&63=125&64=128&66=130&67=133&69=135&70=138'