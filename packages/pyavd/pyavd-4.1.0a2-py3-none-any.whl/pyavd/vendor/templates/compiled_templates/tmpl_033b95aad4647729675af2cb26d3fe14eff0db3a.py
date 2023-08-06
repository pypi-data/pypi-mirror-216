from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/platform.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_platform = resolve('platform')
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
    if t_2((undefined(name='platform') if l_0_platform is missing else l_0_platform)):
        pass
        yield '!\n'
        if t_2(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'trident'), 'forwarding_table_partition')):
            pass
            yield 'platform trident forwarding-table partition '
            yield str(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'trident'), 'forwarding_table_partition'))
            yield '\n'
        if t_2(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand')):
            pass
            for l_1_qos_map in t_1(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand'), 'qos_maps'), 'traffic_class'):
                _loop_vars = {}
                pass
                if (t_2(environment.getattr(l_1_qos_map, 'traffic_class')) and t_2(environment.getattr(l_1_qos_map, 'to_network_qos'))):
                    pass
                    yield 'platform sand qos map traffic-class '
                    yield str(environment.getattr(l_1_qos_map, 'traffic_class'))
                    yield ' to network-qos '
                    yield str(environment.getattr(l_1_qos_map, 'to_network_qos'))
                    yield '\n'
            l_1_qos_map = missing
            if t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand'), 'lag'), 'hardware_only'), True):
                pass
                yield 'platform sand lag hardware-only\n'
            if t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand'), 'lag'), 'mode')):
                pass
                yield 'platform sand lag mode '
                yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand'), 'lag'), 'mode'))
                yield '\n'
            if t_2(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand'), 'forwarding_mode')):
                pass
                yield 'platform sand forwarding mode '
                yield str(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand'), 'forwarding_mode'))
                yield '\n'
            if t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand'), 'multicast_replication'), 'default')):
                pass
                yield 'platform sand multicast replication default '
                yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand'), 'multicast_replication'), 'default'))
                yield '\n'

blocks = {}
debug_info = '2=24&4=27&5=30&7=32&8=34&9=37&10=40&13=45&16=48&17=51&19=53&20=56&22=58&23=61'