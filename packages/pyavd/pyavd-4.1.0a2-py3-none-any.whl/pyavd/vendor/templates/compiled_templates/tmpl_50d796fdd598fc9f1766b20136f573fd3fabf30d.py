from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'documentation/platform.j2'

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
        yield '\n## Platform\n'
        if (t_2(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'trident')) or t_2(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand'))):
            pass
            yield '\n### Platform Summary\n'
            if t_2(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'trident')):
                pass
                yield '\n#### Platform Trident Summary\n\n| Settings | Value |\n| -------- | ----- |\n'
                for l_1_tridentsetting in t_1(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'trident')):
                    _loop_vars = {}
                    pass
                    yield '| '
                    yield str(l_1_tridentsetting)
                    yield ' | '
                    yield str(environment.getitem(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'trident'), l_1_tridentsetting))
                    yield ' |\n'
                l_1_tridentsetting = missing
            if t_2(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand')):
                pass
                yield '\n#### Platform Sand Summary\n\n| Settings | Value |\n| -------- | ----- |\n'
                if t_2(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand'), 'forwarding_mode')):
                    pass
                    yield '| Forwarding Mode | '
                    yield str(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand'), 'forwarding_mode'))
                    yield ' |\n'
                if t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand'), 'lag'), 'hardware_only')):
                    pass
                    yield '| Hardware Only Lag | '
                    yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand'), 'lag'), 'hardware_only'))
                    yield ' |\n'
                if t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand'), 'lag'), 'mode')):
                    pass
                    yield '| Lag Mode | '
                    yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand'), 'lag'), 'mode'))
                    yield ' |\n'
                if t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand'), 'multicast_replication'), 'default')):
                    pass
                    yield '| Default Multicast Replication | '
                    yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand'), 'multicast_replication'), 'default'))
                    yield ' |\n'
                if t_2(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand'), 'qos_maps')):
                    pass
                    yield '\n##### Internal Network QOS Mapping\n\n| Traffic Class | To Network QOS |\n| ------------- | -------------- |\n'
                    for l_1_qos_map in t_1(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand'), 'qos_maps'), 'traffic_class'):
                        _loop_vars = {}
                        pass
                        if (t_2(environment.getattr(l_1_qos_map, 'traffic_class')) and t_2(environment.getattr(l_1_qos_map, 'to_network_qos'))):
                            pass
                            yield '| '
                            yield str(environment.getattr(l_1_qos_map, 'traffic_class'))
                            yield ' | '
                            yield str(environment.getattr(l_1_qos_map, 'to_network_qos'))
                            yield ' |\n'
                    l_1_qos_map = missing
        yield '\n### Platform Configuration\n\n```eos\n'
        template = environment.get_template('eos/platform.j2', 'documentation/platform.j2')
        for event in template.root_render_func(template.new_context(context.get_all(), True, {})):
            yield event
        yield '```\n'

blocks = {}
debug_info = '2=24&5=27&8=30&14=33&15=37&18=42&24=45&25=48&27=50&28=53&30=55&31=58&33=60&34=63&36=65&42=68&43=71&44=74&54=80'