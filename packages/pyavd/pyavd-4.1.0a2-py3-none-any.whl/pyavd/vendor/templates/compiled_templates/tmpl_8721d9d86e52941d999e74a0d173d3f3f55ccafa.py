from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'documentation/traffic-policies.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_traffic_policies = resolve('traffic_policies')
    l_0_traffic_policy_interfaces = resolve('traffic_policy_interfaces')
    l_0_ethernet_interfaces = resolve('ethernet_interfaces')
    l_0_port_channel_interfaces = resolve('port_channel_interfaces')
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
        t_5 = environment.filters['lower']
    except KeyError:
        @internalcode
        def t_5(*unused):
            raise TemplateRuntimeError("No filter named 'lower' found.")
    try:
        t_6 = environment.filters['map']
    except KeyError:
        @internalcode
        def t_6(*unused):
            raise TemplateRuntimeError("No filter named 'map' found.")
    try:
        t_7 = environment.filters['string']
    except KeyError:
        @internalcode
        def t_7(*unused):
            raise TemplateRuntimeError("No filter named 'string' found.")
    try:
        t_8 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_8(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_8((undefined(name='traffic_policies') if l_0_traffic_policies is missing else l_0_traffic_policies)):
        pass
        yield '\n### Traffic Policies information\n'
        if t_8(environment.getattr((undefined(name='traffic_policies') if l_0_traffic_policies is missing else l_0_traffic_policies), 'field_sets')):
            pass
            yield '\n**IPv4 Field sets**\n\n'
            if t_8(environment.getattr(environment.getattr((undefined(name='traffic_policies') if l_0_traffic_policies is missing else l_0_traffic_policies), 'field_sets'), 'ipv4')):
                pass
                yield '| Field Set Name | Values |\n| -------------- | ------ |\n'
                for l_1_field_set_ipv4 in environment.getattr(environment.getattr((undefined(name='traffic_policies') if l_0_traffic_policies is missing else l_0_traffic_policies), 'field_sets'), 'ipv4'):
                    l_1_value = resolve('value')
                    _loop_vars = {}
                    pass
                    if (t_4(l_1_field_set_ipv4) > 1):
                        pass
                        l_1_value = t_3(context.eval_ctx, environment.getattr(l_1_field_set_ipv4, 'prefixes'), '<br/>')
                        _loop_vars['value'] = l_1_value
                    else:
                        pass
                        l_1_value = environment.getattr(environment.getitem(l_1_field_set_ipv4, 0), 'prefixes')
                        _loop_vars['value'] = l_1_value
                    yield '| '
                    yield str(environment.getattr(l_1_field_set_ipv4, 'name'))
                    yield ' | '
                    yield str((undefined(name='value') if l_1_value is missing else l_1_value))
                    yield ' |\n'
                l_1_field_set_ipv4 = l_1_value = missing
            else:
                pass
                yield 'No IPv4 field-set configured.\n'
            yield '\n**IPv6 Field sets**\n\n'
            if t_8(environment.getattr(environment.getattr((undefined(name='traffic_policies') if l_0_traffic_policies is missing else l_0_traffic_policies), 'field_sets'), 'ipv6')):
                pass
                yield '| Field Set Name | Values |\n| -------------- | ------ |\n'
                for l_1_field_set_ipv6 in environment.getattr(environment.getattr((undefined(name='traffic_policies') if l_0_traffic_policies is missing else l_0_traffic_policies), 'field_sets'), 'ipv6'):
                    l_1_value = resolve('value')
                    _loop_vars = {}
                    pass
                    if (t_4(l_1_field_set_ipv6) > 1):
                        pass
                        l_1_value = t_3(context.eval_ctx, environment.getattr(l_1_field_set_ipv6, 'prefixes'), '<br/>')
                        _loop_vars['value'] = l_1_value
                    else:
                        pass
                        l_1_value = environment.getattr(environment.getitem(l_1_field_set_ipv6, 0), 'prefixes')
                        _loop_vars['value'] = l_1_value
                    yield '| '
                    yield str(environment.getattr(l_1_field_set_ipv6, 'name'))
                    yield ' | '
                    yield str((undefined(name='value') if l_1_value is missing else l_1_value))
                    yield ' |\n'
                l_1_field_set_ipv6 = l_1_value = missing
            else:
                pass
                yield 'No IPv6 field-set configured.\n'
            yield '\n**L4 Port Field sets**\n\n'
            if t_8(environment.getattr(environment.getattr((undefined(name='traffic_policies') if l_0_traffic_policies is missing else l_0_traffic_policies), 'field_sets'), 'ports')):
                pass
                yield '| Field Set Name | Values |\n| -------------- | ------ |\n'
                for l_1_field_set_port in environment.getattr(environment.getattr((undefined(name='traffic_policies') if l_0_traffic_policies is missing else l_0_traffic_policies), 'field_sets'), 'ports'):
                    _loop_vars = {}
                    pass
                    yield '| '
                    yield str(environment.getattr(l_1_field_set_port, 'name'))
                    yield ' | '
                    yield str(environment.getattr(l_1_field_set_port, 'port_range'))
                    yield '|\n'
                l_1_field_set_port = missing
            else:
                pass
                yield 'No L4 Port field-set configured.\n'
        else:
            pass
            yield 'No Field-set configured on device.\n'
        if t_8(environment.getattr((undefined(name='traffic_policies') if l_0_traffic_policies is missing else l_0_traffic_policies), 'policies')):
            pass
            yield '\n#### Traffic Policies\n'
            for l_1_policy in t_2(environment.getattr((undefined(name='traffic_policies') if l_0_traffic_policies is missing else l_0_traffic_policies), 'policies'), 'name'):
                _loop_vars = {}
                pass
                yield '\n**'
                yield str(environment.getattr(l_1_policy, 'name'))
                yield ':**\n\n'
                if t_8(environment.getattr(l_1_policy, 'matches')):
                    pass
                    yield '| Match set | Type | Sources | Destinations | Protocol | Source Port(s) | Destination port(s) | Action |\n| --------- | ---- | ------- | ------------ | -------- | -------------- | ------------------- | ------ |\n'
                    for l_2_match in t_2(environment.getattr(l_1_policy, 'matches'), 'name'):
                        l_2_namespace = resolve('namespace')
                        l_2_row = missing
                        _loop_vars = {}
                        pass
                        l_2_row = context.call((undefined(name='namespace') if l_2_namespace is missing else l_2_namespace), _loop_vars=_loop_vars)
                        _loop_vars['row'] = l_2_row
                        if not isinstance(l_2_row, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_row['match_set'] = environment.getattr(l_2_match, 'name')
                        if not isinstance(l_2_row, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_row['type'] = t_5(environment.getattr(l_2_match, 'type'))
                        if not isinstance(l_2_row, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_row['src_net'] = ''
                        if t_8(environment.getattr(environment.getattr(l_2_match, 'source'), 'prefix_lists')):
                            pass
                            if not isinstance(l_2_row, Namespace):
                                raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                            l_2_row['src_net'] = t_3(context.eval_ctx, environment.getattr(environment.getattr(l_2_match, 'source'), 'prefix_lists'), '<br/>')
                        elif t_8(environment.getattr(environment.getattr(l_2_match, 'source'), 'prefixes')):
                            pass
                            if not isinstance(l_2_row, Namespace):
                                raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                            l_2_row['src_net'] = t_3(context.eval_ctx, environment.getattr(environment.getattr(l_2_match, 'source'), 'prefixes'), '<br/>')
                        else:
                            pass
                            if not isinstance(l_2_row, Namespace):
                                raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                            l_2_row['src_net'] = 'ANY'
                        if not isinstance(l_2_row, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_row['dst_net'] = ''
                        if t_8(environment.getattr(environment.getattr(l_2_match, 'destination'), 'prefix_lists')):
                            pass
                            if not isinstance(l_2_row, Namespace):
                                raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                            l_2_row['dst_net'] = t_3(context.eval_ctx, environment.getattr(environment.getattr(l_2_match, 'destination'), 'prefix_lists'), '<br/>')
                        elif t_8(environment.getattr(environment.getattr(l_2_match, 'destination'), 'prefixes')):
                            pass
                            if not isinstance(l_2_row, Namespace):
                                raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                            l_2_row['dst_net'] = t_3(context.eval_ctx, environment.getattr(environment.getattr(l_2_match, 'destination'), 'prefixes'), '<br/>')
                        else:
                            pass
                            if not isinstance(l_2_row, Namespace):
                                raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                            l_2_row['dst_net'] = 'ANY'
                        if not isinstance(l_2_row, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_row['protocols'] = ''
                        if t_8(environment.getattr(l_2_match, 'protocols')):
                            pass
                            if not isinstance(l_2_row, Namespace):
                                raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                            l_2_row['protocols'] = t_3(context.eval_ctx, t_6(context, environment.getattr(l_2_match, 'protocols'), attribute='protocol'), '<br/>')
                        else:
                            pass
                            if not isinstance(l_2_row, Namespace):
                                raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                            l_2_row['protocols'] = 'ANY'
                        if not isinstance(l_2_row, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_row['src_port'] = ''
                        if t_8(environment.getattr(l_2_match, 'protocols')):
                            pass
                            for l_3_protocol in environment.getattr(l_2_match, 'protocols'):
                                _loop_vars = {}
                                pass
                                if t_8(environment.getattr(l_3_protocol, 'src_field')):
                                    pass
                                    if not isinstance(l_2_row, Namespace):
                                        raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                                    l_2_row['src_port'] = environment.getattr(l_3_protocol, 'src_field')
                                elif t_8(environment.getattr(l_3_protocol, 'src_port')):
                                    pass
                                    if not isinstance(l_2_row, Namespace):
                                        raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                                    l_2_row['src_port'] = environment.getattr(l_3_protocol, 'src_port')
                            l_3_protocol = missing
                            if (environment.getattr((undefined(name='row') if l_2_row is missing else l_2_row), 'src_port') == ''):
                                pass
                                if not isinstance(l_2_row, Namespace):
                                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                                l_2_row['src_port'] = 'ANY'
                        if not isinstance(l_2_row, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_row['dst_port'] = ''
                        if t_8(environment.getattr(l_2_match, 'protocols')):
                            pass
                            for l_3_protocol in environment.getattr(l_2_match, 'protocols'):
                                _loop_vars = {}
                                pass
                                if t_8(environment.getattr(l_3_protocol, 'dst_field')):
                                    pass
                                    if not isinstance(l_2_row, Namespace):
                                        raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                                    l_2_row['dst_port'] = environment.getattr(l_3_protocol, 'dst_field')
                                elif t_8(environment.getattr(l_3_protocol, 'dst_port')):
                                    pass
                                    if not isinstance(l_2_row, Namespace):
                                        raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                                    l_2_row['dst_port'] = environment.getattr(l_3_protocol, 'dst_port')
                            l_3_protocol = missing
                            if (environment.getattr((undefined(name='row') if l_2_row is missing else l_2_row), 'dst_port') == ''):
                                pass
                                if not isinstance(l_2_row, Namespace):
                                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                                l_2_row['dst_port'] = 'ANY'
                        if not isinstance(l_2_row, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_row['actions'] = []
                        if t_8(environment.getattr(l_2_match, 'actions')):
                            pass
                            if t_8(environment.getattr(environment.getattr(l_2_match, 'actions'), 'drop'), True):
                                pass
                                context.call(environment.getattr(environment.getattr((undefined(name='row') if l_2_row is missing else l_2_row), 'actions'), 'append'), 'action: DROP', _loop_vars=_loop_vars)
                            else:
                                pass
                                context.call(environment.getattr(environment.getattr((undefined(name='row') if l_2_row is missing else l_2_row), 'actions'), 'append'), 'action: PASS', _loop_vars=_loop_vars)
                            if t_8(environment.getattr(environment.getattr(l_2_match, 'actions'), 'count')):
                                pass
                                context.call(environment.getattr(environment.getattr((undefined(name='row') if l_2_row is missing else l_2_row), 'actions'), 'append'), ('counter: ' + environment.getattr(environment.getattr(l_2_match, 'actions'), 'count')), _loop_vars=_loop_vars)
                            if t_8(environment.getattr(environment.getattr(l_2_match, 'actions'), 'log'), True):
                                pass
                                context.call(environment.getattr(environment.getattr((undefined(name='row') if l_2_row is missing else l_2_row), 'actions'), 'append'), 'logging', _loop_vars=_loop_vars)
                            if t_8(environment.getattr(environment.getattr(l_2_match, 'actions'), 'dscp')):
                                pass
                                context.call(environment.getattr(environment.getattr((undefined(name='row') if l_2_row is missing else l_2_row), 'actions'), 'append'), ('dscp marking: ' + t_7(environment.getattr(environment.getattr(l_2_match, 'actions'), 'dscp'))), _loop_vars=_loop_vars)
                            if t_8(environment.getattr(environment.getattr(l_2_match, 'actions'), 'traffic_class')):
                                pass
                                context.call(environment.getattr(environment.getattr((undefined(name='row') if l_2_row is missing else l_2_row), 'actions'), 'append'), ('traffic-class: ' + t_7(environment.getattr(environment.getattr(l_2_match, 'actions'), 'traffic_class'))), _loop_vars=_loop_vars)
                        else:
                            pass
                            context.call(environment.getattr(environment.getattr((undefined(name='row') if l_2_row is missing else l_2_row), 'actions'), 'append'), 'default action: PASS', _loop_vars=_loop_vars)
                        yield '| '
                        yield str(environment.getattr((undefined(name='row') if l_2_row is missing else l_2_row), 'match_set'))
                        yield ' | '
                        yield str(environment.getattr((undefined(name='row') if l_2_row is missing else l_2_row), 'type'))
                        yield ' | '
                        yield str(environment.getattr((undefined(name='row') if l_2_row is missing else l_2_row), 'src_net'))
                        yield ' | '
                        yield str(environment.getattr((undefined(name='row') if l_2_row is missing else l_2_row), 'dst_net'))
                        yield ' | '
                        yield str(environment.getattr((undefined(name='row') if l_2_row is missing else l_2_row), 'protocols'))
                        yield ' | '
                        yield str(environment.getattr((undefined(name='row') if l_2_row is missing else l_2_row), 'src_port'))
                        yield ' | '
                        yield str(environment.getattr((undefined(name='row') if l_2_row is missing else l_2_row), 'dst_port'))
                        yield ' | '
                        yield str(t_3(context.eval_ctx, environment.getattr((undefined(name='row') if l_2_row is missing else l_2_row), 'actions'), '<br/>'))
                        yield ' |\n'
                    l_2_match = l_2_namespace = l_2_row = missing
                else:
                    pass
                    yield 'No Match condition configured.\n'
                yield '\n'
            l_1_policy = missing
        l_0_traffic_policy_interfaces = []
        context.vars['traffic_policy_interfaces'] = l_0_traffic_policy_interfaces
        context.exported_vars.add('traffic_policy_interfaces')
        for l_1_ethernet_interface in t_2((undefined(name='ethernet_interfaces') if l_0_ethernet_interfaces is missing else l_0_ethernet_interfaces), 'name'):
            _loop_vars = {}
            pass
            if (t_8(environment.getattr(environment.getattr(l_1_ethernet_interface, 'traffic_policy'), 'input')) or t_8(environment.getattr(environment.getattr(l_1_ethernet_interface, 'traffic_policy'), 'output'))):
                pass
                context.call(environment.getattr((undefined(name='traffic_policy_interfaces') if l_0_traffic_policy_interfaces is missing else l_0_traffic_policy_interfaces), 'append'), l_1_ethernet_interface, _loop_vars=_loop_vars)
        l_1_ethernet_interface = missing
        for l_1_port_channel_interface in t_2((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), 'name'):
            _loop_vars = {}
            pass
            if (t_8(environment.getattr(environment.getattr(l_1_port_channel_interface, 'traffic_policy'), 'input')) or t_8(environment.getattr(environment.getattr(l_1_port_channel_interface, 'traffic_policy'), 'output'))):
                pass
                context.call(environment.getattr((undefined(name='traffic_policy_interfaces') if l_0_traffic_policy_interfaces is missing else l_0_traffic_policy_interfaces), 'append'), l_1_port_channel_interface, _loop_vars=_loop_vars)
        l_1_port_channel_interface = missing
        if (t_4((undefined(name='traffic_policy_interfaces') if l_0_traffic_policy_interfaces is missing else l_0_traffic_policy_interfaces)) > 0):
            pass
            yield '\n##### Traffic-Policy Interfaces\n\n| Interface | Input Traffic-Policy | Output Traffic-Policy |\n| --------- | -------------------- | --------------------- |\n'
            for l_1_interface in (undefined(name='traffic_policy_interfaces') if l_0_traffic_policy_interfaces is missing else l_0_traffic_policy_interfaces):
                l_1_row_in_policy = l_1_row_out_policy = missing
                _loop_vars = {}
                pass
                l_1_row_in_policy = t_1(environment.getattr(environment.getattr(l_1_interface, 'traffic_policy'), 'input'), '-')
                _loop_vars['row_in_policy'] = l_1_row_in_policy
                l_1_row_out_policy = t_1(environment.getattr(environment.getattr(l_1_interface, 'traffic_policy'), 'output'), '-')
                _loop_vars['row_out_policy'] = l_1_row_out_policy
                yield '| '
                yield str(environment.getattr(l_1_interface, 'name'))
                yield ' | '
                yield str((undefined(name='row_in_policy') if l_1_row_in_policy is missing else l_1_row_in_policy))
                yield ' | '
                yield str((undefined(name='row_out_policy') if l_1_row_out_policy is missing else l_1_row_out_policy))
                yield ' |\n'
            l_1_interface = l_1_row_in_policy = l_1_row_out_policy = missing
            yield '\n'
        yield '#### Traffic Policies Device Configuration\n\n```eos\n'
        template = environment.get_template('eos/traffic-policies.j2', 'documentation/traffic-policies.j2')
        for event in template.root_render_func(template.new_context(context.get_all(), True, {'traffic_policy_interfaces': l_0_traffic_policy_interfaces})):
            yield event
        yield '```\n'

blocks = {}
debug_info = '2=63&5=66&9=69&12=72&13=76&14=78&16=82&18=85&26=94&29=97&30=101&31=103&33=107&35=110&43=119&46=122&47=126&55=137&58=140&60=144&62=146&65=149&66=154&67=156&68=159&70=162&71=165&72=167&73=170&74=172&76=177&79=180&80=183&81=185&82=188&83=190&85=195&88=198&89=201&90=203&92=208&95=211&96=214&97=216&98=219&99=221&100=224&101=226&104=230&105=232&109=235&110=238&111=240&112=243&113=245&114=248&115=250&118=254&119=256&123=259&124=262&125=264&126=266&128=269&130=270&131=272&133=273&134=275&136=276&137=278&139=279&140=281&143=284&146=286&155=308&156=311&157=314&158=316&161=318&162=321&163=323&166=325&172=328&173=332&174=334&175=337&182=346'