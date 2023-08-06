from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/router-pim-sparse-mode.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_router_pim_sparse_mode = resolve('router_pim_sparse_mode')
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
    if t_2((undefined(name='router_pim_sparse_mode') if l_0_router_pim_sparse_mode is missing else l_0_router_pim_sparse_mode)):
        pass
        yield '!\nrouter pim sparse-mode\n'
        if t_2(environment.getattr((undefined(name='router_pim_sparse_mode') if l_0_router_pim_sparse_mode is missing else l_0_router_pim_sparse_mode), 'ipv4')):
            pass
            yield '   ipv4\n'
            if t_2(environment.getattr(environment.getattr((undefined(name='router_pim_sparse_mode') if l_0_router_pim_sparse_mode is missing else l_0_router_pim_sparse_mode), 'ipv4'), 'bfd'), True):
                pass
                yield '      bfd\n'
            for l_1_rp_address in t_1(environment.getattr(environment.getattr((undefined(name='router_pim_sparse_mode') if l_0_router_pim_sparse_mode is missing else l_0_router_pim_sparse_mode), 'ipv4'), 'rp_addresses'), 'address'):
                l_1_rp_options_cli = missing
                _loop_vars = {}
                pass
                l_1_rp_options_cli = ''
                _loop_vars['rp_options_cli'] = l_1_rp_options_cli
                if t_2(environment.getattr(l_1_rp_address, 'priority')):
                    pass
                    l_1_rp_options_cli = str_join(((undefined(name='rp_options_cli') if l_1_rp_options_cli is missing else l_1_rp_options_cli), ' priority ', environment.getattr(l_1_rp_address, 'priority'), ))
                    _loop_vars['rp_options_cli'] = l_1_rp_options_cli
                if t_2(environment.getattr(l_1_rp_address, 'hashmask')):
                    pass
                    l_1_rp_options_cli = str_join(((undefined(name='rp_options_cli') if l_1_rp_options_cli is missing else l_1_rp_options_cli), ' hashmask ', environment.getattr(l_1_rp_address, 'hashmask'), ))
                    _loop_vars['rp_options_cli'] = l_1_rp_options_cli
                if t_2(environment.getattr(l_1_rp_address, 'override'), True):
                    pass
                    l_1_rp_options_cli = str_join(((undefined(name='rp_options_cli') if l_1_rp_options_cli is missing else l_1_rp_options_cli), ' override', ))
                    _loop_vars['rp_options_cli'] = l_1_rp_options_cli
                if (t_2(environment.getattr(l_1_rp_address, 'groups')) or t_2(environment.getattr(l_1_rp_address, 'access_lists'))):
                    pass
                    if t_2(environment.getattr(l_1_rp_address, 'groups')):
                        pass
                        for l_2_group in t_1(environment.getattr(l_1_rp_address, 'groups')):
                            _loop_vars = {}
                            pass
                            yield '      rp address '
                            yield str(environment.getattr(l_1_rp_address, 'address'))
                            yield ' '
                            yield str(l_2_group)
                            yield str((undefined(name='rp_options_cli') if l_1_rp_options_cli is missing else l_1_rp_options_cli))
                            yield '\n'
                        l_2_group = missing
                    if t_2(environment.getattr(l_1_rp_address, 'access_lists')):
                        pass
                        for l_2_access_list in t_1(environment.getattr(l_1_rp_address, 'access_lists')):
                            _loop_vars = {}
                            pass
                            yield '      rp address '
                            yield str(environment.getattr(l_1_rp_address, 'address'))
                            yield ' access-list '
                            yield str(l_2_access_list)
                            yield str((undefined(name='rp_options_cli') if l_1_rp_options_cli is missing else l_1_rp_options_cli))
                            yield '\n'
                        l_2_access_list = missing
                else:
                    pass
                    yield '      rp address '
                    yield str(environment.getattr(l_1_rp_address, 'address'))
                    yield str((undefined(name='rp_options_cli') if l_1_rp_options_cli is missing else l_1_rp_options_cli))
                    yield '\n'
            l_1_rp_address = l_1_rp_options_cli = missing
            for l_1_anycast_rp in t_1(environment.getattr(environment.getattr((undefined(name='router_pim_sparse_mode') if l_0_router_pim_sparse_mode is missing else l_0_router_pim_sparse_mode), 'ipv4'), 'anycast_rps'), 'address'):
                _loop_vars = {}
                pass
                for l_2_other_anycast_rp_address in t_1(environment.getattr(l_1_anycast_rp, 'other_anycast_rp_addresses'), 'address'):
                    l_2_other_anycast_rp_addresses_cli = missing
                    _loop_vars = {}
                    pass
                    l_2_other_anycast_rp_addresses_cli = str_join(('anycast-rp ', environment.getattr(l_1_anycast_rp, 'address'), ' ', environment.getattr(l_2_other_anycast_rp_address, 'address'), ))
                    _loop_vars['other_anycast_rp_addresses_cli'] = l_2_other_anycast_rp_addresses_cli
                    if t_2(environment.getattr(l_2_other_anycast_rp_address, 'register_count')):
                        pass
                        l_2_other_anycast_rp_addresses_cli = str_join(((undefined(name='other_anycast_rp_addresses_cli') if l_2_other_anycast_rp_addresses_cli is missing else l_2_other_anycast_rp_addresses_cli), ' register-count ', environment.getattr(l_2_other_anycast_rp_address, 'register_count'), ))
                        _loop_vars['other_anycast_rp_addresses_cli'] = l_2_other_anycast_rp_addresses_cli
                    yield '      '
                    yield str((undefined(name='other_anycast_rp_addresses_cli') if l_2_other_anycast_rp_addresses_cli is missing else l_2_other_anycast_rp_addresses_cli))
                    yield '\n'
                l_2_other_anycast_rp_address = l_2_other_anycast_rp_addresses_cli = missing
            l_1_anycast_rp = missing
            if t_2(environment.getattr(environment.getattr((undefined(name='router_pim_sparse_mode') if l_0_router_pim_sparse_mode is missing else l_0_router_pim_sparse_mode), 'ipv4'), 'ssm_range')):
                pass
                yield '      ssm range '
                yield str(environment.getattr(environment.getattr((undefined(name='router_pim_sparse_mode') if l_0_router_pim_sparse_mode is missing else l_0_router_pim_sparse_mode), 'ipv4'), 'ssm_range'))
                yield '\n'
        for l_1_vrf in t_1(environment.getattr((undefined(name='router_pim_sparse_mode') if l_0_router_pim_sparse_mode is missing else l_0_router_pim_sparse_mode), 'vrfs'), 'name'):
            _loop_vars = {}
            pass
            yield '   !\n   vrf '
            yield str(environment.getattr(l_1_vrf, 'name'))
            yield '\n'
            if t_2(environment.getattr(l_1_vrf, 'ipv4')):
                pass
                yield '      ipv4\n'
                if t_2(environment.getattr(environment.getattr(l_1_vrf, 'ipv4'), 'bfd'), True):
                    pass
                    yield '         bfd\n'
                for l_2_rp_address in t_1(environment.getattr(environment.getattr(l_1_vrf, 'ipv4'), 'rp_addresses'), 'address'):
                    l_2_rp_options_cli = missing
                    _loop_vars = {}
                    pass
                    l_2_rp_options_cli = ''
                    _loop_vars['rp_options_cli'] = l_2_rp_options_cli
                    if t_2(environment.getattr(l_2_rp_address, 'priority')):
                        pass
                        l_2_rp_options_cli = str_join(((undefined(name='rp_options_cli') if l_2_rp_options_cli is missing else l_2_rp_options_cli), ' priority ', environment.getattr(l_2_rp_address, 'priority'), ))
                        _loop_vars['rp_options_cli'] = l_2_rp_options_cli
                    if t_2(environment.getattr(l_2_rp_address, 'hashmask')):
                        pass
                        l_2_rp_options_cli = str_join(((undefined(name='rp_options_cli') if l_2_rp_options_cli is missing else l_2_rp_options_cli), ' hashmask ', environment.getattr(l_2_rp_address, 'hashmask'), ))
                        _loop_vars['rp_options_cli'] = l_2_rp_options_cli
                    if t_2(environment.getattr(l_2_rp_address, 'override'), True):
                        pass
                        l_2_rp_options_cli = str_join(((undefined(name='rp_options_cli') if l_2_rp_options_cli is missing else l_2_rp_options_cli), ' override', ))
                        _loop_vars['rp_options_cli'] = l_2_rp_options_cli
                    if (t_2(environment.getattr(l_2_rp_address, 'groups')) or t_2(environment.getattr(l_2_rp_address, 'access_lists'))):
                        pass
                        if t_2(environment.getattr(l_2_rp_address, 'groups')):
                            pass
                            for l_3_group in t_1(environment.getattr(l_2_rp_address, 'groups')):
                                _loop_vars = {}
                                pass
                                yield '         rp address '
                                yield str(environment.getattr(l_2_rp_address, 'address'))
                                yield ' '
                                yield str(l_3_group)
                                yield str((undefined(name='rp_options_cli') if l_2_rp_options_cli is missing else l_2_rp_options_cli))
                                yield '\n'
                            l_3_group = missing
                        if t_2(environment.getattr(l_2_rp_address, 'access_lists')):
                            pass
                            for l_3_access_list in t_1(environment.getattr(l_2_rp_address, 'access_lists')):
                                _loop_vars = {}
                                pass
                                yield '         rp address '
                                yield str(environment.getattr(l_2_rp_address, 'address'))
                                yield ' access-list '
                                yield str(l_3_access_list)
                                yield str((undefined(name='rp_options_cli') if l_2_rp_options_cli is missing else l_2_rp_options_cli))
                                yield '\n'
                            l_3_access_list = missing
                    else:
                        pass
                        yield '         rp address '
                        yield str(environment.getattr(l_2_rp_address, 'address'))
                        yield str((undefined(name='rp_options_cli') if l_2_rp_options_cli is missing else l_2_rp_options_cli))
                        yield '\n'
                l_2_rp_address = l_2_rp_options_cli = missing
        l_1_vrf = missing

blocks = {}
debug_info = '2=24&5=27&7=30&10=33&11=37&12=39&13=41&15=43&16=45&18=47&19=49&21=51&22=53&23=55&24=59&27=65&28=67&29=71&33=80&36=84&37=87&38=91&39=93&40=95&42=98&45=102&46=105&49=107&51=111&52=113&54=116&57=119&58=123&59=125&60=127&62=129&63=131&65=133&66=135&68=137&69=139&70=141&71=145&74=151&75=153&76=157&80=166'