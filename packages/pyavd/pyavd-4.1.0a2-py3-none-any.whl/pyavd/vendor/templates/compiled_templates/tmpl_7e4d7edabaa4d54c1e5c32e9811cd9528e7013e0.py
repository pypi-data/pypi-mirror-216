from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'documentation/router-ospf.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_router_ospf = resolve('router_ospf')
    l_0_ospf_distance_process_ids = resolve('ospf_distance_process_ids')
    l_0_namespace = resolve('namespace')
    l_0_has = resolve('has')
    l_0_ethernet_interface_ospf = resolve('ethernet_interface_ospf')
    l_0_port_channel_interface_ospf = resolve('port_channel_interface_ospf')
    l_0_vlan_interface_ospf = resolve('vlan_interface_ospf')
    l_0_loopback_interface_ospf = resolve('loopback_interface_ospf')
    l_0_vlan_interfaces = resolve('vlan_interfaces')
    l_0_ethernet_interfaces = resolve('ethernet_interfaces')
    l_0_port_channel_interfaces = resolve('port_channel_interfaces')
    l_0_loopback_interfaces = resolve('loopback_interfaces')
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
    try:
        t_6 = environment.tests['defined']
    except KeyError:
        @internalcode
        def t_6(*unused):
            raise TemplateRuntimeError("No test named 'defined' found.")
    pass
    if t_5(environment.getattr((undefined(name='router_ospf') if l_0_router_ospf is missing else l_0_router_ospf), 'process_ids')):
        pass
        yield '\n### Router OSPF\n\n#### Router OSPF Summary\n\n| Process ID | Router ID | Default Passive Interface | No Passive Interface | BFD | Max LSA | Default Information Originate | Log Adjacency Changes Detail | Auto Cost Reference Bandwidth | Maximum Paths | MPLS LDP Sync Default | Distribute List In |\n| ---------- | --------- | ------------------------- | -------------------- | --- | ------- | ----------------------------- | ---------------------------- | ----------------------------- | ------------- | --------------------- | ------------------ |\n'
        for l_1_process_id in t_2(environment.getattr((undefined(name='router_ospf') if l_0_router_ospf is missing else l_0_router_ospf), 'process_ids'), 'id'):
            l_1_passive_interface_default = resolve('passive_interface_default')
            l_1_bfd_enable = resolve('bfd_enable')
            l_1_default_information_originate = resolve('default_information_originate')
            l_1_log_adjacency_changes_detail = resolve('log_adjacency_changes_detail')
            l_1_distribute_list_in = resolve('distribute_list_in')
            l_1_router_id = l_1_no_passive_interfaces = l_1_max_lsa = l_1_auto_cost_reference_bandwidth = l_1_maximum_paths = l_1_mpls_ldp_sync_default = missing
            _loop_vars = {}
            pass
            l_1_router_id = t_1(environment.getattr(l_1_process_id, 'router_id'), '-')
            _loop_vars['router_id'] = l_1_router_id
            if t_5(environment.getattr(l_1_process_id, 'passive_interface_default'), True):
                pass
                l_1_passive_interface_default = 'enabled'
                _loop_vars['passive_interface_default'] = l_1_passive_interface_default
            else:
                pass
                l_1_passive_interface_default = 'disabled'
                _loop_vars['passive_interface_default'] = l_1_passive_interface_default
            l_1_no_passive_interfaces = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace), _loop_vars=_loop_vars)
            _loop_vars['no_passive_interfaces'] = l_1_no_passive_interfaces
            if not isinstance(l_1_no_passive_interfaces, Namespace):
                raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
            l_1_no_passive_interfaces['list'] = ''
            if t_5(environment.getattr(l_1_process_id, 'no_passive_interfaces')):
                pass
                for l_2_interface in environment.getattr(l_1_process_id, 'no_passive_interfaces'):
                    _loop_vars = {}
                    pass
                    if not isinstance(l_1_no_passive_interfaces, Namespace):
                        raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                    l_1_no_passive_interfaces['list'] = str_join((environment.getattr((undefined(name='no_passive_interfaces') if l_1_no_passive_interfaces is missing else l_1_no_passive_interfaces), 'list'), ' ', l_2_interface, ' <br>', ))
                l_2_interface = missing
            else:
                pass
                if not isinstance(l_1_no_passive_interfaces, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_1_no_passive_interfaces['list'] = '-'
            if t_5(environment.getattr(l_1_process_id, 'bfd_enable'), True):
                pass
                l_1_bfd_enable = 'enabled'
                _loop_vars['bfd_enable'] = l_1_bfd_enable
                if t_5(environment.getattr(l_1_process_id, 'bfd_adjacency_state_any'), True):
                    pass
                    l_1_bfd_enable = str_join(((undefined(name='bfd_enable') if l_1_bfd_enable is missing else l_1_bfd_enable), '<br>(any state)', ))
                    _loop_vars['bfd_enable'] = l_1_bfd_enable
            else:
                pass
                l_1_bfd_enable = 'disabled'
                _loop_vars['bfd_enable'] = l_1_bfd_enable
            l_1_max_lsa = t_1(environment.getattr(l_1_process_id, 'max_lsa'), 'default')
            _loop_vars['max_lsa'] = l_1_max_lsa
            if t_5(environment.getattr(l_1_process_id, 'default_information_originate')):
                pass
                if t_5(environment.getattr(environment.getattr(l_1_process_id, 'default_information_originate'), 'always'), True):
                    pass
                    l_1_default_information_originate = 'Always'
                    _loop_vars['default_information_originate'] = l_1_default_information_originate
                else:
                    pass
                    l_1_default_information_originate = 'enabled'
                    _loop_vars['default_information_originate'] = l_1_default_information_originate
            else:
                pass
                l_1_default_information_originate = 'disabled'
                _loop_vars['default_information_originate'] = l_1_default_information_originate
            if t_5(environment.getattr(l_1_process_id, 'log_adjacency_changes_detail'), True):
                pass
                l_1_log_adjacency_changes_detail = 'enabled'
                _loop_vars['log_adjacency_changes_detail'] = l_1_log_adjacency_changes_detail
            else:
                pass
                l_1_log_adjacency_changes_detail = 'disabled'
                _loop_vars['log_adjacency_changes_detail'] = l_1_log_adjacency_changes_detail
            l_1_auto_cost_reference_bandwidth = t_1(environment.getattr(l_1_process_id, 'auto_cost_reference_bandwidth'), '-')
            _loop_vars['auto_cost_reference_bandwidth'] = l_1_auto_cost_reference_bandwidth
            l_1_maximum_paths = t_1(environment.getattr(l_1_process_id, 'maximum_paths'), '-')
            _loop_vars['maximum_paths'] = l_1_maximum_paths
            l_1_mpls_ldp_sync_default = t_1(environment.getattr(l_1_process_id, 'mpls_ldp_sync_default'), '-')
            _loop_vars['mpls_ldp_sync_default'] = l_1_mpls_ldp_sync_default
            if t_5(environment.getattr(environment.getattr(l_1_process_id, 'distribute_list_in'), 'route_map')):
                pass
                l_1_distribute_list_in = str_join(('route-map ', environment.getattr(environment.getattr(l_1_process_id, 'distribute_list_in'), 'route_map'), ))
                _loop_vars['distribute_list_in'] = l_1_distribute_list_in
            else:
                pass
                l_1_distribute_list_in = '-'
                _loop_vars['distribute_list_in'] = l_1_distribute_list_in
            yield '| '
            yield str(environment.getattr(l_1_process_id, 'id'))
            yield ' | '
            yield str((undefined(name='router_id') if l_1_router_id is missing else l_1_router_id))
            yield ' | '
            yield str((undefined(name='passive_interface_default') if l_1_passive_interface_default is missing else l_1_passive_interface_default))
            yield ' |'
            yield str(environment.getattr((undefined(name='no_passive_interfaces') if l_1_no_passive_interfaces is missing else l_1_no_passive_interfaces), 'list'))
            yield ' | '
            yield str((undefined(name='bfd_enable') if l_1_bfd_enable is missing else l_1_bfd_enable))
            yield ' | '
            yield str((undefined(name='max_lsa') if l_1_max_lsa is missing else l_1_max_lsa))
            yield ' | '
            yield str((undefined(name='default_information_originate') if l_1_default_information_originate is missing else l_1_default_information_originate))
            yield ' | '
            yield str((undefined(name='log_adjacency_changes_detail') if l_1_log_adjacency_changes_detail is missing else l_1_log_adjacency_changes_detail))
            yield ' | '
            yield str((undefined(name='auto_cost_reference_bandwidth') if l_1_auto_cost_reference_bandwidth is missing else l_1_auto_cost_reference_bandwidth))
            yield ' | '
            yield str((undefined(name='maximum_paths') if l_1_maximum_paths is missing else l_1_maximum_paths))
            yield ' | '
            yield str((undefined(name='mpls_ldp_sync_default') if l_1_mpls_ldp_sync_default is missing else l_1_mpls_ldp_sync_default))
            yield ' | '
            yield str((undefined(name='distribute_list_in') if l_1_distribute_list_in is missing else l_1_distribute_list_in))
            yield ' |\n'
        l_1_process_id = l_1_router_id = l_1_passive_interface_default = l_1_no_passive_interfaces = l_1_bfd_enable = l_1_max_lsa = l_1_default_information_originate = l_1_log_adjacency_changes_detail = l_1_auto_cost_reference_bandwidth = l_1_maximum_paths = l_1_mpls_ldp_sync_default = l_1_distribute_list_in = missing
        l_0_ospf_distance_process_ids = []
        context.vars['ospf_distance_process_ids'] = l_0_ospf_distance_process_ids
        context.exported_vars.add('ospf_distance_process_ids')
        for l_1_process_id in environment.getattr((undefined(name='router_ospf') if l_0_router_ospf is missing else l_0_router_ospf), 'process_ids'):
            _loop_vars = {}
            pass
            if t_5(environment.getattr(l_1_process_id, 'distance')):
                pass
                context.call(environment.getattr((undefined(name='ospf_distance_process_ids') if l_0_ospf_distance_process_ids is missing else l_0_ospf_distance_process_ids), 'append'), l_1_process_id, _loop_vars=_loop_vars)
        l_1_process_id = missing
        if (t_4((undefined(name='ospf_distance_process_ids') if l_0_ospf_distance_process_ids is missing else l_0_ospf_distance_process_ids)) > 0):
            pass
            yield '\n#### Router OSPF Distance\n\n| Process ID | Intra Area | Inter Area | External |\n| ---------- | ---------- | ---------- | -------- |\n'
            for l_1_process_id in (undefined(name='ospf_distance_process_ids') if l_0_ospf_distance_process_ids is missing else l_0_ospf_distance_process_ids):
                l_1_distance_intra_area = l_1_distance_inter_area = l_1_distance_external = missing
                _loop_vars = {}
                pass
                l_1_distance_intra_area = t_1(environment.getattr(environment.getattr(l_1_process_id, 'distance'), 'intra_area'), '-')
                _loop_vars['distance_intra_area'] = l_1_distance_intra_area
                l_1_distance_inter_area = t_1(environment.getattr(environment.getattr(l_1_process_id, 'distance'), 'inter_area'), '-')
                _loop_vars['distance_inter_area'] = l_1_distance_inter_area
                l_1_distance_external = t_1(environment.getattr(environment.getattr(l_1_process_id, 'distance'), 'external'), '-')
                _loop_vars['distance_external'] = l_1_distance_external
                yield '| '
                yield str(environment.getattr(l_1_process_id, 'id'))
                yield ' | '
                yield str((undefined(name='distance_intra_area') if l_1_distance_intra_area is missing else l_1_distance_intra_area))
                yield ' | '
                yield str((undefined(name='distance_inter_area') if l_1_distance_inter_area is missing else l_1_distance_inter_area))
                yield ' | '
                yield str((undefined(name='distance_external') if l_1_distance_external is missing else l_1_distance_external))
                yield ' |\n'
            l_1_process_id = l_1_distance_intra_area = l_1_distance_inter_area = l_1_distance_external = missing
        l_0_has = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace))
        context.vars['has'] = l_0_has
        context.exported_vars.add('has')
        if not isinstance(l_0_has, Namespace):
            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
        l_0_has['found'] = False
        for l_1_process_id in environment.getattr((undefined(name='router_ospf') if l_0_router_ospf is missing else l_0_router_ospf), 'process_ids'):
            _loop_vars = {}
            pass
            if t_5(environment.getattr(l_1_process_id, 'redistribute')):
                pass
                if not isinstance(l_0_has, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_0_has['found'] = True
        l_1_process_id = missing
        if t_5(environment.getattr((undefined(name='has') if l_0_has is missing else l_0_has), 'found'), True):
            pass
            yield '\n#### Router OSPF Router Redistribution\n\n| Process ID | Source Protocol | Include Leaked | Route Map |\n| ---------- | --------------- | -------------- | --------- |\n'
            for l_1_process_id in t_2(environment.getattr((undefined(name='router_ospf') if l_0_router_ospf is missing else l_0_router_ospf), 'process_ids'), 'id'):
                l_1_source_protocols = resolve('source_protocols')
                l_1_include_leaked = resolve('include_leaked')
                _loop_vars = {}
                pass
                if t_5(environment.getattr(l_1_process_id, 'redistribute')):
                    pass
                    l_1_source_protocols = []
                    _loop_vars['source_protocols'] = l_1_source_protocols
                    if t_6(environment.getattr(environment.getattr(l_1_process_id, 'redistribute'), 'connected')):
                        pass
                        if t_5(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'redistribute'), 'connected'), 'include_leaked'), True):
                            pass
                            l_1_include_leaked = 'enabled'
                            _loop_vars['include_leaked'] = l_1_include_leaked
                        else:
                            pass
                            l_1_include_leaked = 'disabled'
                            _loop_vars['include_leaked'] = l_1_include_leaked
                        context.call(environment.getattr((undefined(name='source_protocols') if l_1_source_protocols is missing else l_1_source_protocols), 'append'), ('connected', (undefined(name='include_leaked') if l_1_include_leaked is missing else l_1_include_leaked), t_1(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'redistribute'), 'connected'), 'route_map'), '-')), _loop_vars=_loop_vars)
                    if t_6(environment.getattr(environment.getattr(l_1_process_id, 'redistribute'), 'static')):
                        pass
                        if t_5(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'redistribute'), 'static'), 'include_leaked'), True):
                            pass
                            l_1_include_leaked = 'enabled'
                            _loop_vars['include_leaked'] = l_1_include_leaked
                        else:
                            pass
                            l_1_include_leaked = 'disabled'
                            _loop_vars['include_leaked'] = l_1_include_leaked
                        context.call(environment.getattr((undefined(name='source_protocols') if l_1_source_protocols is missing else l_1_source_protocols), 'append'), ('static', (undefined(name='include_leaked') if l_1_include_leaked is missing else l_1_include_leaked), t_1(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'redistribute'), 'static'), 'route_map'), '-')), _loop_vars=_loop_vars)
                    if t_6(environment.getattr(environment.getattr(l_1_process_id, 'redistribute'), 'bgp')):
                        pass
                        if t_5(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'redistribute'), 'bgp'), 'include_leaked'), True):
                            pass
                            l_1_include_leaked = 'enabled'
                            _loop_vars['include_leaked'] = l_1_include_leaked
                        else:
                            pass
                            l_1_include_leaked = 'disabled'
                            _loop_vars['include_leaked'] = l_1_include_leaked
                        context.call(environment.getattr((undefined(name='source_protocols') if l_1_source_protocols is missing else l_1_source_protocols), 'append'), ('bgp', (undefined(name='include_leaked') if l_1_include_leaked is missing else l_1_include_leaked), t_1(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'redistribute'), 'bgp'), 'route_map'), '-')), _loop_vars=_loop_vars)
                    for l_2_source_protocol in (undefined(name='source_protocols') if l_1_source_protocols is missing else l_1_source_protocols):
                        _loop_vars = {}
                        pass
                        yield '| '
                        yield str(environment.getattr(l_1_process_id, 'id'))
                        yield ' | '
                        yield str(environment.getitem(l_2_source_protocol, 0))
                        yield ' | '
                        yield str(environment.getitem(l_2_source_protocol, 1))
                        yield ' | '
                        yield str(environment.getitem(l_2_source_protocol, 2))
                        yield ' |\n'
                    l_2_source_protocol = missing
            l_1_process_id = l_1_source_protocols = l_1_include_leaked = missing
        if not isinstance(l_0_has, Namespace):
            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
        l_0_has['found'] = False
        for l_1_process_id in environment.getattr((undefined(name='router_ospf') if l_0_router_ospf is missing else l_0_router_ospf), 'process_ids'):
            _loop_vars = {}
            pass
            if t_5(environment.getattr(l_1_process_id, 'max_metric')):
                pass
                if not isinstance(l_0_has, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_0_has['found'] = True
        l_1_process_id = missing
        if t_5(environment.getattr((undefined(name='has') if l_0_has is missing else l_0_has), 'found'), True):
            pass
            yield '\n#### Router OSPF Router Max-Metric\n\n| Process ID | Router-LSA | External-LSA (metric) | Include Stub | On Startup Delay | Summary-LSA (metric) |\n| ---------- | ---------- | --------------------- | ------------ | ---------------- | -------------------- |\n'
            for l_1_process_id in t_2(environment.getattr((undefined(name='router_ospf') if l_0_router_ospf is missing else l_0_router_ospf), 'process_ids'), 'id'):
                l_1_external_lsa = resolve('external_lsa')
                l_1_include_stub = resolve('include_stub')
                l_1_on_startup = resolve('on_startup')
                l_1_summary_lsa = resolve('summary_lsa')
                _loop_vars = {}
                pass
                if t_6(environment.getattr(environment.getattr(l_1_process_id, 'max_metric'), 'router_lsa')):
                    pass
                    if t_6(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'max_metric'), 'router_lsa'), 'external_lsa')):
                        pass
                        l_1_external_lsa = 'enabled'
                        _loop_vars['external_lsa'] = l_1_external_lsa
                        if t_5(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'max_metric'), 'router_lsa'), 'external_lsa'), 'override_metric')):
                            pass
                            l_1_external_lsa = str_join(((undefined(name='external_lsa') if l_1_external_lsa is missing else l_1_external_lsa), ' (', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'max_metric'), 'router_lsa'), 'external_lsa'), 'override_metric'), ')', ))
                            _loop_vars['external_lsa'] = l_1_external_lsa
                    else:
                        pass
                        l_1_external_lsa = 'disabled'
                        _loop_vars['external_lsa'] = l_1_external_lsa
                    if t_5(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'max_metric'), 'router_lsa'), 'include_stub'), True):
                        pass
                        l_1_include_stub = 'enabled'
                        _loop_vars['include_stub'] = l_1_include_stub
                    else:
                        pass
                        l_1_include_stub = 'disabled'
                        _loop_vars['include_stub'] = l_1_include_stub
                    l_1_on_startup = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'max_metric'), 'router_lsa'), 'on_startup'), 'disabled')
                    _loop_vars['on_startup'] = l_1_on_startup
                    if t_6(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'max_metric'), 'router_lsa'), 'summary_lsa')):
                        pass
                        l_1_summary_lsa = 'enabled'
                        _loop_vars['summary_lsa'] = l_1_summary_lsa
                        if t_5(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'max_metric'), 'router_lsa'), 'summary_lsa'), 'override_metric')):
                            pass
                            l_1_summary_lsa = str_join(((undefined(name='summary_lsa') if l_1_summary_lsa is missing else l_1_summary_lsa), ' (', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'max_metric'), 'router_lsa'), 'summary_lsa'), 'override_metric'), ')', ))
                            _loop_vars['summary_lsa'] = l_1_summary_lsa
                    else:
                        pass
                        l_1_summary_lsa = 'disabled'
                        _loop_vars['summary_lsa'] = l_1_summary_lsa
                    yield '| '
                    yield str(environment.getattr(l_1_process_id, 'id'))
                    yield ' | enabled | '
                    yield str((undefined(name='external_lsa') if l_1_external_lsa is missing else l_1_external_lsa))
                    yield ' | '
                    yield str((undefined(name='include_stub') if l_1_include_stub is missing else l_1_include_stub))
                    yield ' | '
                    yield str((undefined(name='on_startup') if l_1_on_startup is missing else l_1_on_startup))
                    yield ' | '
                    yield str((undefined(name='summary_lsa') if l_1_summary_lsa is missing else l_1_summary_lsa))
                    yield ' |\n'
            l_1_process_id = l_1_external_lsa = l_1_include_stub = l_1_on_startup = l_1_summary_lsa = missing
        if not isinstance(l_0_has, Namespace):
            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
        l_0_has['found'] = False
        for l_1_process_id in environment.getattr((undefined(name='router_ospf') if l_0_router_ospf is missing else l_0_router_ospf), 'process_ids'):
            _loop_vars = {}
            pass
            if t_5(environment.getattr(l_1_process_id, 'timers')):
                pass
                if not isinstance(l_0_has, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_0_has['found'] = True
        l_1_process_id = missing
        if t_5(environment.getattr((undefined(name='has') if l_0_has is missing else l_0_has), 'found'), True):
            pass
            yield '\n#### Router OSPF timers\n\n| Process ID | LSA rx | LSA tx (initial/min/max) | SPF (initial/min/max) |\n| ---------- | ------ | ------------------------ | --------------------- |\n'
            for l_1_process_id in t_2(environment.getattr((undefined(name='router_ospf') if l_0_router_ospf is missing else l_0_router_ospf), 'process_ids'), 'id'):
                l_1_lsa_rx = resolve('lsa_rx')
                l_1_lsa_tx = resolve('lsa_tx')
                l_1_spf_timers = resolve('spf_timers')
                _loop_vars = {}
                pass
                if t_5(environment.getattr(l_1_process_id, 'timers')):
                    pass
                    l_1_lsa_rx = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'timers'), 'lsa'), 'rx_min_interval'), '-')
                    _loop_vars['lsa_rx'] = l_1_lsa_rx
                    if ((t_5(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'timers'), 'lsa'), 'tx_delay'), 'initial')) and t_5(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'timers'), 'lsa'), 'tx_delay'), 'min'))) and t_5(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'timers'), 'lsa'), 'tx_delay'), 'max'))):
                        pass
                        l_1_lsa_tx = environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'timers'), 'lsa'), 'tx_delay'), 'initial')
                        _loop_vars['lsa_tx'] = l_1_lsa_tx
                        l_1_lsa_tx = str_join(((undefined(name='lsa_tx') if l_1_lsa_tx is missing else l_1_lsa_tx), ' / ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'timers'), 'lsa'), 'tx_delay'), 'min'), ))
                        _loop_vars['lsa_tx'] = l_1_lsa_tx
                        l_1_lsa_tx = str_join(((undefined(name='lsa_tx') if l_1_lsa_tx is missing else l_1_lsa_tx), ' / ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'timers'), 'lsa'), 'tx_delay'), 'max'), ))
                        _loop_vars['lsa_tx'] = l_1_lsa_tx
                    else:
                        pass
                        l_1_lsa_tx = '-'
                        _loop_vars['lsa_tx'] = l_1_lsa_tx
                    if ((t_5(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'timers'), 'spf_delay'), 'initial')) and t_5(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'timers'), 'spf_delay'), 'min'))) and t_5(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'timers'), 'spf_delay'), 'max'))):
                        pass
                        l_1_spf_timers = environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'timers'), 'spf_delay'), 'initial')
                        _loop_vars['spf_timers'] = l_1_spf_timers
                        l_1_spf_timers = str_join(((undefined(name='spf_timers') if l_1_spf_timers is missing else l_1_spf_timers), ' / ', environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'timers'), 'spf_delay'), 'min'), ))
                        _loop_vars['spf_timers'] = l_1_spf_timers
                        l_1_spf_timers = str_join(((undefined(name='spf_timers') if l_1_spf_timers is missing else l_1_spf_timers), ' / ', environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'timers'), 'spf_delay'), 'max'), ))
                        _loop_vars['spf_timers'] = l_1_spf_timers
                    else:
                        pass
                        l_1_spf_timers = '-'
                        _loop_vars['spf_timers'] = l_1_spf_timers
                    yield '| '
                    yield str(environment.getattr(l_1_process_id, 'id'))
                    yield ' | '
                    yield str((undefined(name='lsa_rx') if l_1_lsa_rx is missing else l_1_lsa_rx))
                    yield ' | '
                    yield str((undefined(name='lsa_tx') if l_1_lsa_tx is missing else l_1_lsa_tx))
                    yield ' | '
                    yield str((undefined(name='spf_timers') if l_1_spf_timers is missing else l_1_spf_timers))
                    yield ' |\n'
            l_1_process_id = l_1_lsa_rx = l_1_lsa_tx = l_1_spf_timers = missing
        if not isinstance(l_0_has, Namespace):
            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
        l_0_has['found'] = False
        for l_1_process_id in environment.getattr((undefined(name='router_ospf') if l_0_router_ospf is missing else l_0_router_ospf), 'process_ids'):
            _loop_vars = {}
            pass
            if t_5(environment.getattr(l_1_process_id, 'summary_addresses')):
                pass
                if not isinstance(l_0_has, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_0_has['found'] = True
        l_1_process_id = missing
        if t_5(environment.getattr((undefined(name='has') if l_0_has is missing else l_0_has), 'found'), True):
            pass
            yield '\n#### Router OSPF route summary\n\n| Process ID | Prefix | Tag | Attribute Route Map | Not Advertised |\n|------------|--------|-----|---------------------|----------------|\n'
            for l_1_process_id in t_2(environment.getattr((undefined(name='router_ospf') if l_0_router_ospf is missing else l_0_router_ospf), 'process_ids'), 'id'):
                _loop_vars = {}
                pass
                if t_5(environment.getattr(l_1_process_id, 'summary_addresses')):
                    pass
                    for l_2_summary_address in environment.getattr(l_1_process_id, 'summary_addresses'):
                        l_2_summary_prefix = l_2_summary_tag = l_2_summary_attribute_map = l_2_summary_not_advertise = missing
                        _loop_vars = {}
                        pass
                        l_2_summary_prefix = t_1(environment.getattr(l_2_summary_address, 'prefix'), '-')
                        _loop_vars['summary_prefix'] = l_2_summary_prefix
                        l_2_summary_tag = t_1(environment.getattr(l_2_summary_address, 'tag'), '-')
                        _loop_vars['summary_tag'] = l_2_summary_tag
                        l_2_summary_attribute_map = t_1(environment.getattr(l_2_summary_address, 'attribute_map'), '-')
                        _loop_vars['summary_attribute_map'] = l_2_summary_attribute_map
                        l_2_summary_not_advertise = t_1(environment.getattr(l_2_summary_address, 'not_advertise'), '-')
                        _loop_vars['summary_not_advertise'] = l_2_summary_not_advertise
                        yield '| '
                        yield str(environment.getattr(l_1_process_id, 'id'))
                        yield ' | '
                        yield str((undefined(name='summary_prefix') if l_2_summary_prefix is missing else l_2_summary_prefix))
                        yield ' | '
                        yield str((undefined(name='summary_tag') if l_2_summary_tag is missing else l_2_summary_tag))
                        yield ' | '
                        yield str((undefined(name='summary_attribute_map') if l_2_summary_attribute_map is missing else l_2_summary_attribute_map))
                        yield ' | '
                        yield str((undefined(name='summary_not_advertise') if l_2_summary_not_advertise is missing else l_2_summary_not_advertise))
                        yield ' |\n'
                    l_2_summary_address = l_2_summary_prefix = l_2_summary_tag = l_2_summary_attribute_map = l_2_summary_not_advertise = missing
            l_1_process_id = missing
        if not isinstance(l_0_has, Namespace):
            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
        l_0_has['found'] = False
        for l_1_process_id in environment.getattr((undefined(name='router_ospf') if l_0_router_ospf is missing else l_0_router_ospf), 'process_ids'):
            _loop_vars = {}
            pass
            if t_5(environment.getattr(l_1_process_id, 'areas')):
                pass
                if not isinstance(l_0_has, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_0_has['found'] = True
        l_1_process_id = missing
        if t_5(environment.getattr((undefined(name='has') if l_0_has is missing else l_0_has), 'found'), True):
            pass
            yield '\n#### Router OSPF Areas\n\n| Process ID | Area | Area Type | Filter Networks | Filter Prefix List | Additional Options |\n| ---------- | ---- | --------- | --------------- | ------------------ | ------------------ |\n'
            for l_1_process_id in t_2(environment.getattr((undefined(name='router_ospf') if l_0_router_ospf is missing else l_0_router_ospf), 'process_ids'), 'id'):
                _loop_vars = {}
                pass
                for l_2_area in t_2(environment.getattr(l_1_process_id, 'areas'), 'id'):
                    l_2_network_filter = resolve('network_filter')
                    l_2_tmp_cli = resolve('tmp_cli')
                    l_2_prefix_list_filter = l_2_area_type = l_2_additional_cfg_options_list = missing
                    _loop_vars = {}
                    pass
                    if t_5(environment.getattr(environment.getattr(l_2_area, 'filter'), 'networks')):
                        pass
                        l_2_network_filter = t_3(context.eval_ctx, environment.getattr(environment.getattr(l_2_area, 'filter'), 'networks'), ', ')
                        _loop_vars['network_filter'] = l_2_network_filter
                    else:
                        pass
                        l_2_network_filter = '-'
                        _loop_vars['network_filter'] = l_2_network_filter
                    l_2_prefix_list_filter = t_1(environment.getattr(environment.getattr(l_2_area, 'filter'), 'prefix_list'), '-')
                    _loop_vars['prefix_list_filter'] = l_2_prefix_list_filter
                    l_2_area_type = t_1(environment.getattr(l_2_area, 'type'), 'normal')
                    _loop_vars['area_type'] = l_2_area_type
                    l_2_additional_cfg_options_list = []
                    _loop_vars['additional_cfg_options_list'] = l_2_additional_cfg_options_list
                    if t_5(environment.getattr(l_2_area, 'no_summary'), True):
                        pass
                        context.call(environment.getattr((undefined(name='additional_cfg_options_list') if l_2_additional_cfg_options_list is missing else l_2_additional_cfg_options_list), 'append'), 'no-summary', _loop_vars=_loop_vars)
                    if t_6(environment.getattr(l_2_area, 'default_information_originate')):
                        pass
                        l_2_tmp_cli = 'default-information-originate'
                        _loop_vars['tmp_cli'] = l_2_tmp_cli
                        if t_5(environment.getattr(environment.getattr(l_2_area, 'default_information_originate'), 'metric')):
                            pass
                            l_2_tmp_cli = str_join(((undefined(name='tmp_cli') if l_2_tmp_cli is missing else l_2_tmp_cli), ' metric ', environment.getattr(environment.getattr(l_2_area, 'default_information_originate'), 'metric'), ))
                            _loop_vars['tmp_cli'] = l_2_tmp_cli
                        if t_5(environment.getattr(environment.getattr(l_2_area, 'default_information_originate'), 'metric_type')):
                            pass
                            l_2_tmp_cli = str_join(((undefined(name='tmp_cli') if l_2_tmp_cli is missing else l_2_tmp_cli), ' metric-type ', environment.getattr(environment.getattr(l_2_area, 'default_information_originate'), 'metric_type'), ))
                            _loop_vars['tmp_cli'] = l_2_tmp_cli
                        context.call(environment.getattr((undefined(name='additional_cfg_options_list') if l_2_additional_cfg_options_list is missing else l_2_additional_cfg_options_list), 'append'), (undefined(name='tmp_cli') if l_2_tmp_cli is missing else l_2_tmp_cli), _loop_vars=_loop_vars)
                    if t_5(environment.getattr(l_2_area, 'nssa_only'), True):
                        pass
                        context.call(environment.getattr((undefined(name='additional_cfg_options_list') if l_2_additional_cfg_options_list is missing else l_2_additional_cfg_options_list), 'append'), 'nssa-only', _loop_vars=_loop_vars)
                    yield '| '
                    yield str(environment.getattr(l_1_process_id, 'id'))
                    yield ' | '
                    yield str(environment.getattr(l_2_area, 'id'))
                    yield ' | '
                    yield str((undefined(name='area_type') if l_2_area_type is missing else l_2_area_type))
                    yield ' | '
                    yield str((undefined(name='network_filter') if l_2_network_filter is missing else l_2_network_filter))
                    yield ' | '
                    yield str((undefined(name='prefix_list_filter') if l_2_prefix_list_filter is missing else l_2_prefix_list_filter))
                    yield ' | '
                    yield str(t_3(context.eval_ctx, (undefined(name='additional_cfg_options_list') if l_2_additional_cfg_options_list is missing else l_2_additional_cfg_options_list), ', '))
                    yield ' |\n'
                l_2_area = l_2_network_filter = l_2_prefix_list_filter = l_2_area_type = l_2_additional_cfg_options_list = l_2_tmp_cli = missing
            l_1_process_id = missing
        l_0_ethernet_interface_ospf = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace), configured=False)
        context.vars['ethernet_interface_ospf'] = l_0_ethernet_interface_ospf
        context.exported_vars.add('ethernet_interface_ospf')
        l_0_port_channel_interface_ospf = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace), configured=False)
        context.vars['port_channel_interface_ospf'] = l_0_port_channel_interface_ospf
        context.exported_vars.add('port_channel_interface_ospf')
        l_0_vlan_interface_ospf = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace), configured=False)
        context.vars['vlan_interface_ospf'] = l_0_vlan_interface_ospf
        context.exported_vars.add('vlan_interface_ospf')
        l_0_loopback_interface_ospf = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace), configured=False)
        context.vars['loopback_interface_ospf'] = l_0_loopback_interface_ospf
        context.exported_vars.add('loopback_interface_ospf')
        for l_1_vlan_interface in t_2((undefined(name='vlan_interfaces') if l_0_vlan_interfaces is missing else l_0_vlan_interfaces), 'name'):
            _loop_vars = {}
            pass
            if t_5(environment.getattr(l_1_vlan_interface, 'ospf_area')):
                pass
                if not isinstance(l_0_vlan_interface_ospf, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_0_vlan_interface_ospf['configured'] = True
        l_1_vlan_interface = missing
        for l_1_ethernet_interface in t_2((undefined(name='ethernet_interfaces') if l_0_ethernet_interfaces is missing else l_0_ethernet_interfaces), 'name'):
            _loop_vars = {}
            pass
            if t_5(environment.getattr(l_1_ethernet_interface, 'ospf_area')):
                pass
                if not isinstance(l_0_ethernet_interface_ospf, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_0_ethernet_interface_ospf['configured'] = True
        l_1_ethernet_interface = missing
        for l_1_port_channel_interface in t_2((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), 'name'):
            _loop_vars = {}
            pass
            if t_5(environment.getattr(l_1_port_channel_interface, 'ospf_area')):
                pass
                if not isinstance(l_0_port_channel_interface_ospf, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_0_port_channel_interface_ospf['configured'] = True
        l_1_port_channel_interface = missing
        for l_1_loopback_interface in t_2((undefined(name='loopback_interfaces') if l_0_loopback_interfaces is missing else l_0_loopback_interfaces), 'name'):
            _loop_vars = {}
            pass
            if t_5(environment.getattr(l_1_loopback_interface, 'ospf_area')):
                pass
                if not isinstance(l_0_loopback_interface_ospf, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_0_loopback_interface_ospf['configured'] = True
        l_1_loopback_interface = missing
        if (((environment.getattr((undefined(name='vlan_interface_ospf') if l_0_vlan_interface_ospf is missing else l_0_vlan_interface_ospf), 'configured') or environment.getattr((undefined(name='ethernet_interface_ospf') if l_0_ethernet_interface_ospf is missing else l_0_ethernet_interface_ospf), 'configured')) or environment.getattr((undefined(name='port_channel_interface_ospf') if l_0_port_channel_interface_ospf is missing else l_0_port_channel_interface_ospf), 'configured')) or environment.getattr((undefined(name='loopback_interface_ospf') if l_0_loopback_interface_ospf is missing else l_0_loopback_interface_ospf), 'configured')):
            pass
            yield '\n#### OSPF Interfaces\n\n| Interface | Area | Cost | Point To Point |\n| -------- | -------- | -------- | -------- |\n'
            if environment.getattr((undefined(name='ethernet_interface_ospf') if l_0_ethernet_interface_ospf is missing else l_0_ethernet_interface_ospf), 'configured'):
                pass
                for l_1_ethernet_interface in t_2((undefined(name='ethernet_interfaces') if l_0_ethernet_interfaces is missing else l_0_ethernet_interfaces), 'name'):
                    l_1_ospf_area = resolve('ospf_area')
                    l_1_ospf_cost = resolve('ospf_cost')
                    l_1_ospf_network_point_to_point = resolve('ospf_network_point_to_point')
                    _loop_vars = {}
                    pass
                    if t_5(environment.getattr(l_1_ethernet_interface, 'ospf_area')):
                        pass
                        l_1_ospf_area = environment.getattr(l_1_ethernet_interface, 'ospf_area')
                        _loop_vars['ospf_area'] = l_1_ospf_area
                        l_1_ospf_cost = t_1(environment.getattr(l_1_ethernet_interface, 'ospf_cost'), '-')
                        _loop_vars['ospf_cost'] = l_1_ospf_cost
                        l_1_ospf_network_point_to_point = t_1(environment.getattr(l_1_ethernet_interface, 'ospf_network_point_to_point'), '-')
                        _loop_vars['ospf_network_point_to_point'] = l_1_ospf_network_point_to_point
                        yield '| '
                        yield str(environment.getattr(l_1_ethernet_interface, 'name'))
                        yield ' | '
                        yield str((undefined(name='ospf_area') if l_1_ospf_area is missing else l_1_ospf_area))
                        yield ' | '
                        yield str((undefined(name='ospf_cost') if l_1_ospf_cost is missing else l_1_ospf_cost))
                        yield ' | '
                        yield str((undefined(name='ospf_network_point_to_point') if l_1_ospf_network_point_to_point is missing else l_1_ospf_network_point_to_point))
                        yield ' |\n'
                l_1_ethernet_interface = l_1_ospf_area = l_1_ospf_cost = l_1_ospf_network_point_to_point = missing
            if environment.getattr((undefined(name='port_channel_interface_ospf') if l_0_port_channel_interface_ospf is missing else l_0_port_channel_interface_ospf), 'configured'):
                pass
                for l_1_port_channel_interface in t_2((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), 'name'):
                    l_1_ospf_area = resolve('ospf_area')
                    l_1_ospf_cost = resolve('ospf_cost')
                    l_1_ospf_network_point_to_point = resolve('ospf_network_point_to_point')
                    _loop_vars = {}
                    pass
                    if t_5(environment.getattr(l_1_port_channel_interface, 'ospf_area')):
                        pass
                        l_1_ospf_area = environment.getattr(l_1_port_channel_interface, 'ospf_area')
                        _loop_vars['ospf_area'] = l_1_ospf_area
                        l_1_ospf_cost = t_1(environment.getattr(l_1_port_channel_interface, 'ospf_cost'), '-')
                        _loop_vars['ospf_cost'] = l_1_ospf_cost
                        l_1_ospf_network_point_to_point = t_1(environment.getattr(l_1_port_channel_interface, 'ospf_network_point_to_point'), '-')
                        _loop_vars['ospf_network_point_to_point'] = l_1_ospf_network_point_to_point
                        yield '| '
                        yield str(environment.getattr(l_1_port_channel_interface, 'name'))
                        yield ' | '
                        yield str((undefined(name='ospf_area') if l_1_ospf_area is missing else l_1_ospf_area))
                        yield ' | '
                        yield str((undefined(name='ospf_cost') if l_1_ospf_cost is missing else l_1_ospf_cost))
                        yield ' | '
                        yield str((undefined(name='ospf_network_point_to_point') if l_1_ospf_network_point_to_point is missing else l_1_ospf_network_point_to_point))
                        yield ' |\n'
                l_1_port_channel_interface = l_1_ospf_area = l_1_ospf_cost = l_1_ospf_network_point_to_point = missing
            if environment.getattr((undefined(name='vlan_interface_ospf') if l_0_vlan_interface_ospf is missing else l_0_vlan_interface_ospf), 'configured'):
                pass
                for l_1_vlan_interface in t_2((undefined(name='vlan_interfaces') if l_0_vlan_interfaces is missing else l_0_vlan_interfaces), 'name'):
                    l_1_ospf_area = resolve('ospf_area')
                    l_1_ospf_cost = resolve('ospf_cost')
                    l_1_ospf_network_point_to_point = resolve('ospf_network_point_to_point')
                    _loop_vars = {}
                    pass
                    if t_5(environment.getattr(l_1_vlan_interface, 'ospf_area')):
                        pass
                        l_1_ospf_area = environment.getattr(l_1_vlan_interface, 'ospf_area')
                        _loop_vars['ospf_area'] = l_1_ospf_area
                        l_1_ospf_cost = t_1(environment.getattr(l_1_vlan_interface, 'ospf_cost'), '-')
                        _loop_vars['ospf_cost'] = l_1_ospf_cost
                        l_1_ospf_network_point_to_point = t_1(environment.getattr(l_1_vlan_interface, 'ospf_network_point_to_point'), '-')
                        _loop_vars['ospf_network_point_to_point'] = l_1_ospf_network_point_to_point
                        yield '| '
                        yield str(environment.getattr(l_1_vlan_interface, 'name'))
                        yield ' | '
                        yield str((undefined(name='ospf_area') if l_1_ospf_area is missing else l_1_ospf_area))
                        yield ' | '
                        yield str((undefined(name='ospf_cost') if l_1_ospf_cost is missing else l_1_ospf_cost))
                        yield ' | '
                        yield str((undefined(name='ospf_network_point_to_point') if l_1_ospf_network_point_to_point is missing else l_1_ospf_network_point_to_point))
                        yield ' |\n'
                l_1_vlan_interface = l_1_ospf_area = l_1_ospf_cost = l_1_ospf_network_point_to_point = missing
            if environment.getattr((undefined(name='loopback_interface_ospf') if l_0_loopback_interface_ospf is missing else l_0_loopback_interface_ospf), 'configured'):
                pass
                for l_1_loopback_interface in t_2((undefined(name='loopback_interfaces') if l_0_loopback_interfaces is missing else l_0_loopback_interfaces), 'name'):
                    l_1_ospf_area = resolve('ospf_area')
                    l_1_ospf_cost = resolve('ospf_cost')
                    l_1_ospf_network_point_to_point = resolve('ospf_network_point_to_point')
                    _loop_vars = {}
                    pass
                    if t_5(environment.getattr(l_1_loopback_interface, 'ospf_area')):
                        pass
                        l_1_ospf_area = environment.getattr(l_1_loopback_interface, 'ospf_area')
                        _loop_vars['ospf_area'] = l_1_ospf_area
                        l_1_ospf_cost = t_1(environment.getattr(l_1_loopback_interface, 'ospf_cost'), '-')
                        _loop_vars['ospf_cost'] = l_1_ospf_cost
                        l_1_ospf_network_point_to_point = t_1(environment.getattr(l_1_loopback_interface, 'ospf_network_point_to_point'), '-')
                        _loop_vars['ospf_network_point_to_point'] = l_1_ospf_network_point_to_point
                        yield '| '
                        yield str(environment.getattr(l_1_loopback_interface, 'name'))
                        yield ' | '
                        yield str((undefined(name='ospf_area') if l_1_ospf_area is missing else l_1_ospf_area))
                        yield ' | '
                        yield str((undefined(name='ospf_cost') if l_1_ospf_cost is missing else l_1_ospf_cost))
                        yield ' | '
                        yield str((undefined(name='ospf_network_point_to_point') if l_1_ospf_network_point_to_point is missing else l_1_ospf_network_point_to_point))
                        yield ' |\n'
                l_1_loopback_interface = l_1_ospf_area = l_1_ospf_cost = l_1_ospf_network_point_to_point = missing
        yield '\n#### Router OSPF Device Configuration\n\n```eos\n'
        template = environment.get_template('eos/router-ospf.j2', 'documentation/router-ospf.j2')
        for event in template.root_render_func(template.new_context(context.get_all(), True, {'ethernet_interface_ospf': l_0_ethernet_interface_ospf, 'has': l_0_has, 'loopback_interface_ospf': l_0_loopback_interface_ospf, 'ospf_distance_process_ids': l_0_ospf_distance_process_ids, 'port_channel_interface_ospf': l_0_port_channel_interface_ospf, 'vlan_interface_ospf': l_0_vlan_interface_ospf})):
            yield event
        yield '```\n'

blocks = {}
debug_info = '2=59&10=62&11=71&12=73&13=75&15=79&17=81&18=83&19=86&20=88&21=91&24=97&26=100&27=102&28=104&29=106&32=110&34=112&35=114&36=116&37=118&39=122&42=126&44=128&45=130&47=134&49=136&50=138&51=140&52=142&53=144&55=148&57=151&60=176&61=179&62=182&63=184&66=186&72=189&73=193&74=195&75=197&76=200&80=209&81=212&82=215&83=218&84=220&87=224&93=227&94=232&95=234&96=236&97=238&98=240&100=244&102=246&104=247&105=249&106=251&108=255&110=257&112=258&113=260&114=262&116=266&118=268&120=269&121=273&127=283&128=286&129=289&130=291&133=295&139=298&140=305&141=307&142=309&143=311&144=313&147=317&149=319&150=321&152=325&154=327&155=329&156=331&157=333&158=335&161=339&163=342&168=353&169=356&170=359&171=361&174=365&180=368&181=374&182=376&183=378&186=380&187=382&188=384&190=388&192=390&195=392&196=394&197=396&199=400&201=403&206=412&207=415&208=418&209=420&212=424&218=427&219=430&220=432&221=436&222=438&223=440&224=442&225=445&231=457&232=460&233=463&234=465&237=469&243=472&244=475&245=481&246=483&248=487&250=489&251=491&252=493&253=495&254=497&256=498&257=500&258=502&259=504&261=506&262=508&264=510&266=511&267=513&269=515&274=529&275=532&276=535&277=538&278=541&279=544&280=546&283=550&284=553&285=555&288=559&289=562&290=564&293=568&294=571&295=573&298=577&304=580&305=582&306=588&307=590&308=592&309=594&310=597&314=606&315=608&316=614&317=616&318=618&319=620&320=623&324=632&325=634&326=640&327=642&328=644&329=646&330=649&334=658&335=660&336=666&337=668&338=670&339=672&340=675&349=685'