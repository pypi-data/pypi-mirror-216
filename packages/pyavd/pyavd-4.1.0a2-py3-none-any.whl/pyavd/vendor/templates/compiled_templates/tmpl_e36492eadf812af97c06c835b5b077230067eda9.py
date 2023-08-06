from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'documentation/flow-trackings.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_flow_trackings = resolve('flow_trackings')
    try:
        t_1 = environment.filters['arista.avd.default']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.default' found.")
    try:
        t_2 = environment.filters['arista.avd.natural_sort']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.natural_sort' found.")
    try:
        t_3 = environment.filters['join']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No filter named 'join' found.")
    try:
        t_4 = environment.filters['length']
    except KeyError:
        @internalcode
        def t_4(*unused):
            raise TemplateRuntimeError("No filter named 'length' found.")
    try:
        t_5 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_5(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_5((undefined(name='flow_trackings') if l_0_flow_trackings is missing else l_0_flow_trackings)):
        pass
        yield '\n### Flow Tracking\n'
        for l_1_flow_tracking in (undefined(name='flow_trackings') if l_0_flow_trackings is missing else l_0_flow_trackings):
            _loop_vars = {}
            pass
            if (environment.getattr(l_1_flow_tracking, 'type') == 'sampled'):
                pass
                yield '\n#### Flow Tracking Sampled\n\nSample: '
                yield str(t_1(environment.getattr(l_1_flow_tracking, 'sample'), 'default'))
                yield '\n'
                if t_5(environment.getattr(l_1_flow_tracking, 'trackers')):
                    pass
                    yield '\n##### Trackers Summary\n\n| Tracker Name | Record Export On Inactive Timeout | Record Export On Interval | MPLS | Number of Exporters | Applied On |\n| ------------ | --------------------------------- | ------------------------- | ---- | ------------------- | ---------- |\n'
                    for l_2_tracker in t_2(environment.getattr(l_1_flow_tracking, 'trackers'), 'name'):
                        l_2_ethernet_interfaces = resolve('ethernet_interfaces')
                        l_2_port_channel_interfaces = resolve('port_channel_interfaces')
                        l_2_on_inactive_timeout = l_2_on_interval = l_2_mpls = l_2_count_exporter = l_2_applied_on = missing
                        _loop_vars = {}
                        pass
                        l_2_on_inactive_timeout = t_1(environment.getattr(environment.getattr(l_2_tracker, 'record_export'), 'on_inactive_timeout'), '-')
                        _loop_vars['on_inactive_timeout'] = l_2_on_inactive_timeout
                        l_2_on_interval = t_1(environment.getattr(environment.getattr(l_2_tracker, 'record_export'), 'on_interval'), '-')
                        _loop_vars['on_interval'] = l_2_on_interval
                        l_2_mpls = t_1(environment.getattr(environment.getattr(l_2_tracker, 'record_export'), 'mpls'), '-')
                        _loop_vars['mpls'] = l_2_mpls
                        l_2_count_exporter = t_4(t_1(environment.getattr(l_2_tracker, 'exporters'), []))
                        _loop_vars['count_exporter'] = l_2_count_exporter
                        l_2_applied_on = []
                        _loop_vars['applied_on'] = l_2_applied_on
                        for l_3_ethernet_interface in t_1((undefined(name='ethernet_interfaces') if l_2_ethernet_interfaces is missing else l_2_ethernet_interfaces), []):
                            _loop_vars = {}
                            pass
                            if t_5(environment.getattr(environment.getattr(l_3_ethernet_interface, 'flow_tracker'), 'sampled'), environment.getattr(l_2_tracker, 'name')):
                                pass
                                context.call(environment.getattr((undefined(name='applied_on') if l_2_applied_on is missing else l_2_applied_on), 'append'), environment.getattr(l_3_ethernet_interface, 'name'), _loop_vars=_loop_vars)
                        l_3_ethernet_interface = missing
                        for l_3_port_channel_interface in t_1((undefined(name='port_channel_interfaces') if l_2_port_channel_interfaces is missing else l_2_port_channel_interfaces), []):
                            _loop_vars = {}
                            pass
                            if t_5(environment.getattr(environment.getattr(l_3_port_channel_interface, 'flow_tracker'), 'sampled'), environment.getattr(l_2_tracker, 'name')):
                                pass
                                context.call(environment.getattr((undefined(name='applied_on') if l_2_applied_on is missing else l_2_applied_on), 'append'), environment.getattr(l_3_port_channel_interface, 'name'), _loop_vars=_loop_vars)
                        l_3_port_channel_interface = missing
                        yield '| '
                        yield str(environment.getattr(l_2_tracker, 'name'))
                        yield ' | '
                        yield str((undefined(name='on_inactive_timeout') if l_2_on_inactive_timeout is missing else l_2_on_inactive_timeout))
                        yield ' | '
                        yield str((undefined(name='on_interval') if l_2_on_interval is missing else l_2_on_interval))
                        yield ' | '
                        yield str((undefined(name='mpls') if l_2_mpls is missing else l_2_mpls))
                        yield ' | '
                        yield str((undefined(name='count_exporter') if l_2_count_exporter is missing else l_2_count_exporter))
                        yield ' | '
                        yield str(t_3(context.eval_ctx, (undefined(name='applied_on') if l_2_applied_on is missing else l_2_applied_on), '<br>'))
                        yield ' |\n'
                    l_2_tracker = l_2_on_inactive_timeout = l_2_on_interval = l_2_mpls = l_2_count_exporter = l_2_applied_on = l_2_ethernet_interfaces = l_2_port_channel_interfaces = missing
                    yield '\n##### Exporters Summary\n\n| Tracker Name | Exporter Name | Collector IP/Host | Collector Port | Local Interface |\n| ------------ | ------------- | ----------------- | -------------- | --------------- |\n'
                    for l_2_tracker in t_2(environment.getattr(l_1_flow_tracking, 'trackers'), 'name'):
                        _loop_vars = {}
                        pass
                        for l_3_exporter in t_2(environment.getattr(l_2_tracker, 'exporters'), 'name'):
                            l_3_host = l_3_port = l_3_local_interface = missing
                            _loop_vars = {}
                            pass
                            l_3_host = t_1(environment.getattr(l_3_exporter, 'host'), '-')
                            _loop_vars['host'] = l_3_host
                            l_3_port = t_1(environment.getattr(l_3_exporter, 'port'), '-')
                            _loop_vars['port'] = l_3_port
                            l_3_local_interface = t_1(environment.getattr(l_3_exporter, 'local_interface'), 'No local interface')
                            _loop_vars['local_interface'] = l_3_local_interface
                            yield '| '
                            yield str(environment.getattr(l_2_tracker, 'name'))
                            yield ' | '
                            yield str(environment.getattr(l_3_exporter, 'name'))
                            yield ' | '
                            yield str((undefined(name='host') if l_3_host is missing else l_3_host))
                            yield ' | '
                            yield str((undefined(name='port') if l_3_port is missing else l_3_port))
                            yield ' | '
                            yield str((undefined(name='local_interface') if l_3_local_interface is missing else l_3_local_interface))
                            yield ' |\n'
                        l_3_exporter = l_3_host = l_3_port = l_3_local_interface = missing
                    l_2_tracker = missing
        l_1_flow_tracking = missing
        yield '\n#### Flow Tracking Configuration\n\n```eos\n'
        template = environment.get_template('eos/flow-trackings.j2', 'documentation/flow-trackings.j2')
        for event in template.root_render_func(template.new_context(context.get_all(), True, {})):
            yield event
        yield '```\n'

blocks = {}
debug_info = '2=42&5=45&6=48&10=51&11=53&17=56&18=62&19=64&20=66&21=68&22=70&23=72&24=75&25=77&28=79&29=82&30=84&33=87&40=101&41=104&42=108&43=110&44=112&45=115&55=129'