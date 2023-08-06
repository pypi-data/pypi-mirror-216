from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/traffic-policies.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_traffic_policies = resolve('traffic_policies')
    try:
        t_1 = environment.filters['join']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'join' found.")
    try:
        t_2 = environment.filters['length']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No filter named 'length' found.")
    try:
        t_3 = environment.filters['lower']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No filter named 'lower' found.")
    try:
        t_4 = environment.filters['string']
    except KeyError:
        @internalcode
        def t_4(*unused):
            raise TemplateRuntimeError("No filter named 'string' found.")
    try:
        t_5 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_5(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    try:
        t_6 = environment.tests['defined']
    except KeyError:
        @internalcode
        def t_6(*unused):
            raise TemplateRuntimeError("No test named 'defined' found.")
    pass
    if t_5((undefined(name='traffic_policies') if l_0_traffic_policies is missing else l_0_traffic_policies)):
        pass
        yield '!\ntraffic-policies\n'
        if t_5(environment.getattr(environment.getattr((undefined(name='traffic_policies') if l_0_traffic_policies is missing else l_0_traffic_policies), 'options'), 'counter_per_interface'), True):
            pass
            yield '   counter interface per-interface ingress\n'
        if t_5(environment.getattr(environment.getattr((undefined(name='traffic_policies') if l_0_traffic_policies is missing else l_0_traffic_policies), 'field_sets'), 'ipv4')):
            pass
            for l_1_field_set_ipv4 in environment.getattr(environment.getattr((undefined(name='traffic_policies') if l_0_traffic_policies is missing else l_0_traffic_policies), 'field_sets'), 'ipv4'):
                _loop_vars = {}
                pass
                yield '   field-set ipv4 prefix '
                yield str(environment.getattr(l_1_field_set_ipv4, 'name'))
                yield '\n      '
                yield str(t_1(context.eval_ctx, environment.getattr(l_1_field_set_ipv4, 'prefixes'), ' '))
                yield '\n   !\n'
            l_1_field_set_ipv4 = missing
        if t_5(environment.getattr(environment.getattr((undefined(name='traffic_policies') if l_0_traffic_policies is missing else l_0_traffic_policies), 'field_sets'), 'ipv6')):
            pass
            for l_1_field_set_ipv6 in environment.getattr(environment.getattr((undefined(name='traffic_policies') if l_0_traffic_policies is missing else l_0_traffic_policies), 'field_sets'), 'ipv6'):
                _loop_vars = {}
                pass
                yield '   field-set ipv6 prefix '
                yield str(environment.getattr(l_1_field_set_ipv6, 'name'))
                yield '\n      '
                yield str(t_1(context.eval_ctx, environment.getattr(l_1_field_set_ipv6, 'prefixes'), ' '))
                yield '\n   !\n'
            l_1_field_set_ipv6 = missing
        if t_5(environment.getattr(environment.getattr((undefined(name='traffic_policies') if l_0_traffic_policies is missing else l_0_traffic_policies), 'field_sets'), 'ports')):
            pass
            for l_1_field_set_port in environment.getattr(environment.getattr((undefined(name='traffic_policies') if l_0_traffic_policies is missing else l_0_traffic_policies), 'field_sets'), 'ports'):
                _loop_vars = {}
                pass
                yield '   field-set l4-port '
                yield str(environment.getattr(l_1_field_set_port, 'name'))
                yield '\n      '
                yield str(environment.getattr(l_1_field_set_port, 'port_range'))
                yield '\n   !\n'
            l_1_field_set_port = missing
        if t_5(environment.getattr((undefined(name='traffic_policies') if l_0_traffic_policies is missing else l_0_traffic_policies), 'policies')):
            pass
            for l_1_policy in environment.getattr((undefined(name='traffic_policies') if l_0_traffic_policies is missing else l_0_traffic_policies), 'policies'):
                l_1_namespace = resolve('namespace')
                l_1_transient_values = resolve('transient_values')
                _loop_vars = {}
                pass
                yield '   traffic-policy '
                yield str(environment.getattr(l_1_policy, 'name'))
                yield '\n'
                if t_5(environment.getattr(l_1_policy, 'matches')):
                    pass
                    l_1_transient_values = context.call((undefined(name='namespace') if l_1_namespace is missing else l_1_namespace), _loop_vars=_loop_vars)
                    _loop_vars['transient_values'] = l_1_transient_values
                    if not isinstance(l_1_transient_values, Namespace):
                        raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                    l_1_transient_values['counters'] = []
                    for l_2_match in environment.getattr(l_1_policy, 'matches'):
                        _loop_vars = {}
                        pass
                        if t_5(environment.getattr(environment.getattr(l_2_match, 'actions'), 'count')):
                            pass
                            context.call(environment.getattr(environment.getattr((undefined(name='transient_values') if l_1_transient_values is missing else l_1_transient_values), 'counters'), 'append'), t_4(environment.getattr(environment.getattr(l_2_match, 'actions'), 'count')), _loop_vars=_loop_vars)
                    l_2_match = missing
                    if (t_2(environment.getattr((undefined(name='transient_values') if l_1_transient_values is missing else l_1_transient_values), 'counters')) > 0):
                        pass
                        yield '      counter '
                        yield str(t_1(context.eval_ctx, environment.getattr((undefined(name='transient_values') if l_1_transient_values is missing else l_1_transient_values), 'counters'), ' '))
                        yield '\n'
                    for l_2_match in environment.getattr(l_1_policy, 'matches'):
                        _loop_vars = {}
                        pass
                        yield '      match '
                        yield str(environment.getattr(l_2_match, 'name'))
                        yield ' '
                        yield str(t_3(environment.getattr(l_2_match, 'type')))
                        yield '\n'
                        if t_5(environment.getattr(l_2_match, 'source')):
                            pass
                            if t_5(environment.getattr(environment.getattr(l_2_match, 'source'), 'prefixes')):
                                pass
                                yield '         source prefix '
                                yield str(t_1(context.eval_ctx, environment.getattr(environment.getattr(l_2_match, 'source'), 'prefixes'), ' '))
                                yield '\n'
                            if t_5(environment.getattr(environment.getattr(l_2_match, 'source'), 'prefix_lists')):
                                pass
                                yield '         source prefix field-set '
                                yield str(t_1(context.eval_ctx, environment.getattr(environment.getattr(l_2_match, 'source'), 'prefix_lists'), ' '))
                                yield '\n'
                        if t_5(environment.getattr(l_2_match, 'destination')):
                            pass
                            if t_5(environment.getattr(environment.getattr(l_2_match, 'destination'), 'prefixes')):
                                pass
                                yield '         destination prefix '
                                yield str(t_1(context.eval_ctx, environment.getattr(environment.getattr(l_2_match, 'destination'), 'prefixes'), ' '))
                                yield '\n'
                            if t_5(environment.getattr(environment.getattr(l_2_match, 'destination'), 'prefix_lists')):
                                pass
                                yield '         destination prefix field-set '
                                yield str(t_1(context.eval_ctx, environment.getattr(environment.getattr(l_2_match, 'destination'), 'prefix_lists'), ' '))
                                yield '\n'
                        if t_5(environment.getattr(l_2_match, 'protocols')):
                            pass
                            for l_3_protocol in environment.getattr(l_2_match, 'protocols'):
                                l_3_protocol_cli = resolve('protocol_cli')
                                _loop_vars = {}
                                pass
                                if (t_5(environment.getattr(l_3_protocol, 'dst_port')) and (t_3(environment.getattr(l_3_protocol, 'protocol')) in ['tcp', 'udp'])):
                                    pass
                                    l_3_protocol_cli = str_join(('protocol ', environment.getattr(l_3_protocol, 'protocol'), ))
                                    _loop_vars['protocol_cli'] = l_3_protocol_cli
                                    if t_5(environment.getattr(l_3_protocol, 'flags')):
                                        pass
                                        l_3_protocol_cli = str_join(((undefined(name='protocol_cli') if l_3_protocol_cli is missing else l_3_protocol_cli), ' flags ', t_1(context.eval_ctx, environment.getattr(l_3_protocol, 'flags'), ' '), ))
                                        _loop_vars['protocol_cli'] = l_3_protocol_cli
                                    l_3_protocol_cli = str_join(((undefined(name='protocol_cli') if l_3_protocol_cli is missing else l_3_protocol_cli), ' destination port ', environment.getattr(l_3_protocol, 'dst_port'), ))
                                    _loop_vars['protocol_cli'] = l_3_protocol_cli
                                    yield '         '
                                    yield str((undefined(name='protocol_cli') if l_3_protocol_cli is missing else l_3_protocol_cli))
                                    yield '\n'
                                elif (t_5(environment.getattr(l_3_protocol, 'src_port')) and (t_3(environment.getattr(l_3_protocol, 'protocol')) in ['tcp', 'udp'])):
                                    pass
                                    l_3_protocol_cli = str_join(('protocol ', environment.getattr(l_3_protocol, 'protocol'), ))
                                    _loop_vars['protocol_cli'] = l_3_protocol_cli
                                    if t_5(environment.getattr(l_3_protocol, 'flags')):
                                        pass
                                        l_3_protocol_cli = str_join(((undefined(name='protocol_cli') if l_3_protocol_cli is missing else l_3_protocol_cli), ' flags ', t_1(context.eval_ctx, environment.getattr(l_3_protocol, 'flags'), ' '), ))
                                        _loop_vars['protocol_cli'] = l_3_protocol_cli
                                    l_3_protocol_cli = str_join(((undefined(name='protocol_cli') if l_3_protocol_cli is missing else l_3_protocol_cli), ' source port ', environment.getattr(l_3_protocol, 'src_port'), ))
                                    _loop_vars['protocol_cli'] = l_3_protocol_cli
                                    yield '         '
                                    yield str((undefined(name='protocol_cli') if l_3_protocol_cli is missing else l_3_protocol_cli))
                                    yield '\n'
                                elif (t_5(environment.getattr(l_3_protocol, 'dst_field')) and (t_3(environment.getattr(l_3_protocol, 'protocol')) in ['tcp', 'udp'])):
                                    pass
                                    l_3_protocol_cli = str_join(('protocol ', environment.getattr(l_3_protocol, 'protocol'), ))
                                    _loop_vars['protocol_cli'] = l_3_protocol_cli
                                    if t_5(environment.getattr(l_3_protocol, 'flags')):
                                        pass
                                        l_3_protocol_cli = str_join(((undefined(name='protocol_cli') if l_3_protocol_cli is missing else l_3_protocol_cli), ' flags ', t_1(context.eval_ctx, environment.getattr(l_3_protocol, 'flags'), ' '), ))
                                        _loop_vars['protocol_cli'] = l_3_protocol_cli
                                    l_3_protocol_cli = str_join(((undefined(name='protocol_cli') if l_3_protocol_cli is missing else l_3_protocol_cli), ' destination port field-set ', environment.getattr(l_3_protocol, 'dst_field'), ))
                                    _loop_vars['protocol_cli'] = l_3_protocol_cli
                                    yield '         '
                                    yield str((undefined(name='protocol_cli') if l_3_protocol_cli is missing else l_3_protocol_cli))
                                    yield '\n'
                                elif (t_5(environment.getattr(l_3_protocol, 'src_field')) and (t_3(environment.getattr(l_3_protocol, 'protocol')) in ['tcp', 'udp'])):
                                    pass
                                    l_3_protocol_cli = str_join(('protocol ', environment.getattr(l_3_protocol, 'protocol'), ))
                                    _loop_vars['protocol_cli'] = l_3_protocol_cli
                                    if t_5(environment.getattr(l_3_protocol, 'flags')):
                                        pass
                                        l_3_protocol_cli = str_join(((undefined(name='protocol_cli') if l_3_protocol_cli is missing else l_3_protocol_cli), ' flags ', t_1(context.eval_ctx, environment.getattr(l_3_protocol, 'flags'), ' '), ))
                                        _loop_vars['protocol_cli'] = l_3_protocol_cli
                                    l_3_protocol_cli = str_join(((undefined(name='protocol_cli') if l_3_protocol_cli is missing else l_3_protocol_cli), ' source port field-set ', environment.getattr(l_3_protocol, 'src_field'), ))
                                    _loop_vars['protocol_cli'] = l_3_protocol_cli
                                    yield '         '
                                    yield str((undefined(name='protocol_cli') if l_3_protocol_cli is missing else l_3_protocol_cli))
                                    yield '\n'
                                elif (t_3(t_5(environment.getattr(l_3_protocol, 'icmp_type'), environment.getattr(l_3_protocol, 'protocol'))) == 'icmp'):
                                    pass
                                    yield '         protocol icmp type '
                                    yield str(t_1(context.eval_ctx, environment.getattr(l_3_protocol, 'icmp_type'), ' '))
                                    yield ' code all\n'
                                elif (t_3(environment.getattr(l_3_protocol, 'protocol')) == 'neighbors'):
                                    pass
                                    yield '         protocol neighbors bgp\n'
                                elif (t_3(environment.getattr(l_3_protocol, 'protocol')) != 'ip'):
                                    pass
                                    yield '         protocol '
                                    yield str(environment.getattr(l_3_protocol, 'protocol'))
                                    yield '\n'
                            l_3_protocol = l_3_protocol_cli = missing
                        if t_5(environment.getattr(l_2_match, 'ttl')):
                            pass
                            yield '         ttl '
                            yield str(environment.getattr(l_2_match, 'ttl'))
                            yield '\n'
                        if t_5(environment.getattr(environment.getattr(l_2_match, 'fragment'), 'offset')):
                            pass
                            yield '         fragment offset '
                            yield str(environment.getattr(environment.getattr(l_2_match, 'fragment'), 'offset'))
                            yield '\n'
                        elif t_6(environment.getattr(l_2_match, 'fragment')):
                            pass
                            yield '         fragment\n'
                        if (((t_5(environment.getattr(environment.getattr(l_2_match, 'actions'), 'count')) or t_5(environment.getattr(environment.getattr(l_2_match, 'actions'), 'traffic_class'))) or t_5(environment.getattr(environment.getattr(l_2_match, 'actions'), 'dscp'))) or t_5(environment.getattr(environment.getattr(l_2_match, 'actions'), 'drop'), True)):
                            pass
                            yield '         actions\n'
                            if t_5(environment.getattr(environment.getattr(l_2_match, 'actions'), 'count')):
                                pass
                                yield '            count '
                                yield str(environment.getattr(environment.getattr(l_2_match, 'actions'), 'count'))
                                yield '\n'
                            if t_5(environment.getattr(environment.getattr(l_2_match, 'actions'), 'traffic_class')):
                                pass
                                yield '            set traffic class '
                                yield str(environment.getattr(environment.getattr(l_2_match, 'actions'), 'traffic_class'))
                                yield '\n'
                            if t_5(environment.getattr(environment.getattr(l_2_match, 'actions'), 'dscp')):
                                pass
                                yield '            set dscp '
                                yield str(environment.getattr(environment.getattr(l_2_match, 'actions'), 'dscp'))
                                yield '\n'
                            if t_5(environment.getattr(environment.getattr(l_2_match, 'actions'), 'drop'), True):
                                pass
                                yield '            drop\n'
                                if t_5(environment.getattr(environment.getattr(l_2_match, 'actions'), 'log'), True):
                                    pass
                                    yield '            log\n'
                        yield '         !\n      !\n'
                    l_2_match = missing
                if t_5(environment.getattr(l_1_policy, 'default_actions')):
                    pass
                    for l_2_version in environment.getattr(l_1_policy, 'default_actions'):
                        _loop_vars = {}
                        pass
                        yield '      match '
                        yield str(t_3(l_2_version))
                        yield '-all-default '
                        yield str(t_3(l_2_version))
                        yield '\n         actions\n'
                        if t_5(l_2_version, 'ipv4'):
                            pass
                            if t_5(environment.getattr(environment.getattr(environment.getattr(l_1_policy, 'default_actions'), 'ipv4'), 'count')):
                                pass
                                yield '            count '
                                yield str(environment.getattr(environment.getattr(environment.getattr(l_1_policy, 'default_actions'), 'ipv4'), 'count'))
                                yield '\n'
                            if t_5(environment.getattr(environment.getattr(environment.getattr(l_1_policy, 'default_actions'), 'ipv4'), 'traffic_class')):
                                pass
                                yield '            set traffic class '
                                yield str(environment.getattr(environment.getattr(environment.getattr(l_1_policy, 'default_actions'), 'ipv4'), 'traffic_class'))
                                yield '\n'
                            if t_5(environment.getattr(environment.getattr(environment.getattr(l_1_policy, 'default_actions'), 'ipv4'), 'dscp')):
                                pass
                                yield '            set dscp '
                                yield str(environment.getattr(environment.getattr(environment.getattr(l_1_policy, 'default_actions'), 'ipv4'), 'dscp'))
                                yield '\n'
                            if t_5(environment.getattr(environment.getattr(environment.getattr(l_1_policy, 'default_actions'), 'ipv4'), 'drop'), True):
                                pass
                                yield '            drop\n'
                                if t_5(environment.getattr(environment.getattr(environment.getattr(l_1_policy, 'default_actions'), 'ipv4'), 'log'), True):
                                    pass
                                    yield '            log\n'
                        elif t_5(l_2_version, 'ipv6'):
                            pass
                            if t_5(environment.getattr(environment.getattr(environment.getattr(l_1_policy, 'default_actions'), 'ipv6'), 'count')):
                                pass
                                yield '            count '
                                yield str(environment.getattr(environment.getattr(environment.getattr(l_1_policy, 'default_actions'), 'ipv6'), 'count'))
                                yield '\n'
                            if t_5(environment.getattr(environment.getattr(environment.getattr(l_1_policy, 'default_actions'), 'ipv6'), 'traffic_class')):
                                pass
                                yield '            set traffic class '
                                yield str(environment.getattr(environment.getattr(environment.getattr(l_1_policy, 'default_actions'), 'ipv6'), 'traffic_class'))
                                yield '\n'
                            if t_5(environment.getattr(environment.getattr(environment.getattr(l_1_policy, 'default_actions'), 'ipv6'), 'dscp')):
                                pass
                                yield '            set dscp '
                                yield str(environment.getattr(environment.getattr(environment.getattr(l_1_policy, 'default_actions'), 'ipv6'), 'dscp'))
                                yield '\n'
                            if t_5(environment.getattr(environment.getattr(environment.getattr(l_1_policy, 'default_actions'), 'ipv6'), 'drop'), True):
                                pass
                                yield '            drop\n'
                                if t_5(environment.getattr(environment.getattr(environment.getattr(l_1_policy, 'default_actions'), 'ipv6'), 'log'), True):
                                    pass
                                    yield '            log\n'
                    l_2_version = missing
                yield '   !\n'
            l_1_policy = l_1_namespace = l_1_transient_values = missing

blocks = {}
debug_info = '2=48&6=51&11=54&12=56&13=60&14=62&19=65&20=67&21=71&22=73&27=76&28=78&29=82&30=84&35=87&36=89&37=95&38=97&40=99&41=101&42=104&43=107&44=109&47=111&48=114&51=116&52=120&54=124&55=126&56=129&58=131&59=134&63=136&64=138&65=141&67=143&68=146&72=148&73=150&75=154&76=156&77=158&78=160&80=162&81=165&83=167&84=169&85=171&86=173&88=175&89=178&91=180&92=182&93=184&94=186&96=188&97=191&99=193&100=195&101=197&102=199&104=201&105=204&106=206&107=209&108=211&110=214&111=217&116=220&117=223&120=225&121=228&122=230&126=233&129=236&130=239&133=241&134=244&137=246&138=249&141=251&144=254&155=259&156=261&157=265&159=269&161=271&162=274&165=276&166=279&169=281&170=284&173=286&176=289&180=292&182=294&183=297&186=299&187=302&190=304&191=307&194=309&197=312'