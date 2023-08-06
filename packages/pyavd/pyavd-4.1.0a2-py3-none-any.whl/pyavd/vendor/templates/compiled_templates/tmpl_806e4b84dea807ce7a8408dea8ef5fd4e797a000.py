from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/router-msdp.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_router_msdp = resolve('router_msdp')
    try:
        t_1 = environment.filters['arista.avd.default']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.default' found.")
    try:
        t_2 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_2((undefined(name='router_msdp') if l_0_router_msdp is missing else l_0_router_msdp)):
        pass
        yield '!\nrouter msdp\n'
        for l_1_group_limit in t_1(environment.getattr((undefined(name='router_msdp') if l_0_router_msdp is missing else l_0_router_msdp), 'group_limits'), []):
            _loop_vars = {}
            pass
            yield '   group-limit '
            yield str(environment.getattr(l_1_group_limit, 'limit'))
            yield ' source '
            yield str(environment.getattr(l_1_group_limit, 'source_prefix'))
            yield '\n'
        l_1_group_limit = missing
        if t_2(environment.getattr((undefined(name='router_msdp') if l_0_router_msdp is missing else l_0_router_msdp), 'originator_id_local_interface')):
            pass
            yield '   originator-id local-interface '
            yield str(environment.getattr((undefined(name='router_msdp') if l_0_router_msdp is missing else l_0_router_msdp), 'originator_id_local_interface'))
            yield '\n'
        if t_2(environment.getattr((undefined(name='router_msdp') if l_0_router_msdp is missing else l_0_router_msdp), 'rejected_limit')):
            pass
            yield '   rejected-limit '
            yield str(environment.getattr((undefined(name='router_msdp') if l_0_router_msdp is missing else l_0_router_msdp), 'rejected_limit'))
            yield '\n'
        if t_2(environment.getattr((undefined(name='router_msdp') if l_0_router_msdp is missing else l_0_router_msdp), 'forward_register_packets'), True):
            pass
            yield '   forward register-packets\n'
        if t_2(environment.getattr((undefined(name='router_msdp') if l_0_router_msdp is missing else l_0_router_msdp), 'connection_retry_interval')):
            pass
            yield '   connection retry interval '
            yield str(environment.getattr((undefined(name='router_msdp') if l_0_router_msdp is missing else l_0_router_msdp), 'connection_retry_interval'))
            yield '\n'
        for l_1_peer in t_1(environment.getattr((undefined(name='router_msdp') if l_0_router_msdp is missing else l_0_router_msdp), 'peers'), []):
            l_1_default_peer_cli = resolve('default_peer_cli')
            _loop_vars = {}
            pass
            if t_2(environment.getattr(l_1_peer, 'ipv4_address')):
                pass
                yield '   !\n   peer '
                yield str(environment.getattr(l_1_peer, 'ipv4_address'))
                yield '\n'
                if t_2(environment.getattr(environment.getattr(l_1_peer, 'default_peer'), 'enabled'), True):
                    pass
                    l_1_default_peer_cli = 'default-peer'
                    _loop_vars['default_peer_cli'] = l_1_default_peer_cli
                    if t_2(environment.getattr(environment.getattr(l_1_peer, 'default_peer'), 'prefix_list')):
                        pass
                        l_1_default_peer_cli = str_join(((undefined(name='default_peer_cli') if l_1_default_peer_cli is missing else l_1_default_peer_cli), ' prefix-list ', environment.getattr(environment.getattr(l_1_peer, 'default_peer'), 'prefix_list'), ))
                        _loop_vars['default_peer_cli'] = l_1_default_peer_cli
                    yield '      '
                    yield str((undefined(name='default_peer_cli') if l_1_default_peer_cli is missing else l_1_default_peer_cli))
                    yield '\n'
                for l_2_mesh_group in t_1(environment.getattr(l_1_peer, 'mesh_groups'), []):
                    _loop_vars = {}
                    pass
                    if t_2(environment.getattr(l_2_mesh_group, 'name')):
                        pass
                        yield '      mesh-group '
                        yield str(environment.getattr(l_2_mesh_group, 'name'))
                        yield '\n'
                l_2_mesh_group = missing
                if t_2(environment.getattr(l_1_peer, 'local_interface')):
                    pass
                    yield '      local-interface '
                    yield str(environment.getattr(l_1_peer, 'local_interface'))
                    yield '\n'
                if (t_2(environment.getattr(environment.getattr(l_1_peer, 'keepalive'), 'keepalive_timer')) and t_2(environment.getattr(environment.getattr(l_1_peer, 'keepalive'), 'hold_timer'))):
                    pass
                    yield '      keepalive '
                    yield str(environment.getattr(environment.getattr(l_1_peer, 'keepalive'), 'keepalive_timer'))
                    yield ' '
                    yield str(environment.getattr(environment.getattr(l_1_peer, 'keepalive'), 'hold_timer'))
                    yield '\n'
                if t_2(environment.getattr(environment.getattr(l_1_peer, 'sa_filter'), 'in_list')):
                    pass
                    yield '      sa-filter in list '
                    yield str(environment.getattr(environment.getattr(l_1_peer, 'sa_filter'), 'in_list'))
                    yield '\n'
                if t_2(environment.getattr(environment.getattr(l_1_peer, 'sa_filter'), 'out_list')):
                    pass
                    yield '      sa-filter out list '
                    yield str(environment.getattr(environment.getattr(l_1_peer, 'sa_filter'), 'in_list'))
                    yield '\n'
                if t_2(environment.getattr(l_1_peer, 'description')):
                    pass
                    yield '      description '
                    yield str(environment.getattr(l_1_peer, 'description'))
                    yield '\n'
                if t_2(environment.getattr(l_1_peer, 'disabled'), True):
                    pass
                    yield '      disabled\n'
                if t_2(environment.getattr(l_1_peer, 'sa_limit')):
                    pass
                    yield '      sa-limit '
                    yield str(environment.getattr(l_1_peer, 'sa_limit'))
                    yield '\n'
        l_1_peer = l_1_default_peer_cli = missing
        for l_1_vrf in t_1(environment.getattr((undefined(name='router_msdp') if l_0_router_msdp is missing else l_0_router_msdp), 'vrfs'), []):
            _loop_vars = {}
            pass
            if (t_2(environment.getattr(l_1_vrf, 'name')) and (environment.getattr(l_1_vrf, 'name') != 'default')):
                pass
                yield '   !\n   vrf '
                yield str(environment.getattr(l_1_vrf, 'name'))
                yield '\n'
                for l_2_group_limit in t_1(environment.getattr(l_1_vrf, 'group_limits'), []):
                    _loop_vars = {}
                    pass
                    yield '      group-limit '
                    yield str(environment.getattr(l_2_group_limit, 'limit'))
                    yield ' source '
                    yield str(environment.getattr(l_2_group_limit, 'source_prefix'))
                    yield '\n'
                l_2_group_limit = missing
                if t_2(environment.getattr(l_1_vrf, 'originator_id_local_interface')):
                    pass
                    yield '      originator-id local-interface '
                    yield str(environment.getattr(l_1_vrf, 'originator_id_local_interface'))
                    yield '\n'
                if t_2(environment.getattr(l_1_vrf, 'rejected_limit')):
                    pass
                    yield '      rejected-limit '
                    yield str(environment.getattr(l_1_vrf, 'rejected_limit'))
                    yield '\n'
                if t_2(environment.getattr(l_1_vrf, 'forward_register_packets'), True):
                    pass
                    yield '      forward register-packets\n'
                if t_2(environment.getattr(l_1_vrf, 'connection_retry_interval')):
                    pass
                    yield '      connection retry interval '
                    yield str(environment.getattr(l_1_vrf, 'connection_retry_interval'))
                    yield '\n'
                for l_2_peer in t_1(environment.getattr(l_1_vrf, 'peers'), []):
                    l_2_default_peer_cli = resolve('default_peer_cli')
                    _loop_vars = {}
                    pass
                    if t_2(environment.getattr(l_2_peer, 'ipv4_address')):
                        pass
                        yield '      !\n      peer '
                        yield str(environment.getattr(l_2_peer, 'ipv4_address'))
                        yield '\n'
                        if t_2(environment.getattr(environment.getattr(l_2_peer, 'default_peer'), 'enabled'), True):
                            pass
                            l_2_default_peer_cli = 'default-peer'
                            _loop_vars['default_peer_cli'] = l_2_default_peer_cli
                            if t_2(environment.getattr(environment.getattr(l_2_peer, 'default_peer'), 'prefix_list')):
                                pass
                                l_2_default_peer_cli = str_join(((undefined(name='default_peer_cli') if l_2_default_peer_cli is missing else l_2_default_peer_cli), ' prefix-list ', environment.getattr(environment.getattr(l_2_peer, 'default_peer'), 'prefix_list'), ))
                                _loop_vars['default_peer_cli'] = l_2_default_peer_cli
                            yield '         '
                            yield str((undefined(name='default_peer_cli') if l_2_default_peer_cli is missing else l_2_default_peer_cli))
                            yield '\n'
                        for l_3_mesh_group in t_1(environment.getattr(l_2_peer, 'mesh_groups'), []):
                            _loop_vars = {}
                            pass
                            if t_2(environment.getattr(l_3_mesh_group, 'name')):
                                pass
                                yield '         mesh-group '
                                yield str(environment.getattr(l_3_mesh_group, 'name'))
                                yield '\n'
                        l_3_mesh_group = missing
                        if t_2(environment.getattr(l_2_peer, 'local_interface')):
                            pass
                            yield '         local-interface '
                            yield str(environment.getattr(l_2_peer, 'local_interface'))
                            yield '\n'
                        if (t_2(environment.getattr(environment.getattr(l_2_peer, 'keepalive'), 'keepalive_timer')) and t_2(environment.getattr(environment.getattr(l_2_peer, 'keepalive'), 'hold_timer'))):
                            pass
                            yield '         keepalive '
                            yield str(environment.getattr(environment.getattr(l_2_peer, 'keepalive'), 'keepalive_timer'))
                            yield ' '
                            yield str(environment.getattr(environment.getattr(l_2_peer, 'keepalive'), 'hold_timer'))
                            yield '\n'
                        if t_2(environment.getattr(environment.getattr(l_2_peer, 'sa_filter'), 'in_list')):
                            pass
                            yield '         sa-filter in list '
                            yield str(environment.getattr(environment.getattr(l_2_peer, 'sa_filter'), 'in_list'))
                            yield '\n'
                        if t_2(environment.getattr(environment.getattr(l_2_peer, 'sa_filter'), 'out_list')):
                            pass
                            yield '         sa-filter out list '
                            yield str(environment.getattr(environment.getattr(l_2_peer, 'sa_filter'), 'in_list'))
                            yield '\n'
                        if t_2(environment.getattr(l_2_peer, 'description')):
                            pass
                            yield '         description '
                            yield str(environment.getattr(l_2_peer, 'description'))
                            yield '\n'
                        if t_2(environment.getattr(l_2_peer, 'disabled'), True):
                            pass
                            yield '         disabled\n'
                        if t_2(environment.getattr(l_2_peer, 'sa_limit')):
                            pass
                            yield '         sa-limit '
                            yield str(environment.getattr(l_2_peer, 'sa_limit'))
                            yield '\n'
                l_2_peer = l_2_default_peer_cli = missing
        l_1_vrf = missing

blocks = {}
debug_info = '2=24&5=27&6=31&8=36&9=39&11=41&12=44&14=46&17=49&18=52&20=54&21=58&23=61&24=63&25=65&26=67&27=69&29=72&31=74&32=77&33=80&36=83&37=86&39=88&40=91&42=95&43=98&45=100&46=103&48=105&49=108&51=110&54=113&55=116&59=119&60=122&62=125&63=127&64=131&66=136&67=139&69=141&70=144&72=146&75=149&76=152&78=154&79=158&81=161&82=163&83=165&84=167&85=169&87=172&89=174&90=177&91=180&94=183&95=186&97=188&98=191&100=195&101=198&103=200&104=203&106=205&107=208&109=210&112=213&113=216'