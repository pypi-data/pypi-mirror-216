from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/ip-igmp-snooping.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_ip_igmp_snooping = resolve('ip_igmp_snooping')
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
    if t_2((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping)):
        pass
        if ((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping) != {'globally_enabled': True}):
            pass
            yield '!\n'
        if t_2(environment.getattr((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping), 'globally_enabled'), False):
            pass
            yield 'no ip igmp snooping\n'
        if t_2(environment.getattr((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping), 'robustness_variable')):
            pass
            yield 'ip igmp snooping robustness-variable '
            yield str(environment.getattr((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping), 'robustness_variable'))
            yield '\n'
        if t_2(environment.getattr((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping), 'restart_query_interval')):
            pass
            yield 'ip igmp snooping restart query-interval '
            yield str(environment.getattr((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping), 'restart_query_interval'))
            yield '\n'
        if t_2(environment.getattr((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping), 'interface_restart_query')):
            pass
            yield 'ip igmp snooping interface-restart-query '
            yield str(environment.getattr((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping), 'interface_restart_query'))
            yield '\n'
        if t_2(environment.getattr((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping), 'fast_leave'), False):
            pass
            yield 'no ip igmp snooping fast-leave\n'
        elif t_2(environment.getattr((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping), 'fast_leave'), True):
            pass
            yield 'ip igmp snooping fast-leave\n'
        for l_1_vlan in t_1(environment.getattr((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping), 'vlans'), 'id'):
            _loop_vars = {}
            pass
            if t_2(environment.getattr(l_1_vlan, 'enabled'), False):
                pass
                yield 'no ip igmp snooping vlan '
                yield str(environment.getattr(l_1_vlan, 'id'))
                yield '\n'
            elif t_2(environment.getattr(l_1_vlan, 'enabled'), True):
                pass
                yield 'ip igmp snooping vlan '
                yield str(environment.getattr(l_1_vlan, 'id'))
                yield '\n'
            if t_2(environment.getattr(l_1_vlan, 'querier')):
                pass
                if t_2(environment.getattr(environment.getattr(l_1_vlan, 'querier'), 'enabled'), True):
                    pass
                    yield 'ip igmp snooping vlan '
                    yield str(environment.getattr(l_1_vlan, 'id'))
                    yield ' querier\n'
                elif t_2(environment.getattr(environment.getattr(l_1_vlan, 'querier'), 'enabled'), False):
                    pass
                    yield 'no ip igmp snooping vlan '
                    yield str(environment.getattr(l_1_vlan, 'id'))
                    yield ' querier\n'
                if t_2(environment.getattr(environment.getattr(l_1_vlan, 'querier'), 'address')):
                    pass
                    yield 'ip igmp snooping vlan '
                    yield str(environment.getattr(l_1_vlan, 'id'))
                    yield ' querier address '
                    yield str(environment.getattr(environment.getattr(l_1_vlan, 'querier'), 'address'))
                    yield '\n'
                if t_2(environment.getattr(environment.getattr(l_1_vlan, 'querier'), 'query_interval')):
                    pass
                    yield 'ip igmp snooping vlan '
                    yield str(environment.getattr(l_1_vlan, 'id'))
                    yield ' querier query-interval '
                    yield str(environment.getattr(environment.getattr(l_1_vlan, 'querier'), 'query_interval'))
                    yield '\n'
                if t_2(environment.getattr(environment.getattr(l_1_vlan, 'querier'), 'max_response_time')):
                    pass
                    yield 'ip igmp snooping vlan '
                    yield str(environment.getattr(l_1_vlan, 'id'))
                    yield ' querier max-response-time '
                    yield str(environment.getattr(environment.getattr(l_1_vlan, 'querier'), 'max_response_time'))
                    yield '\n'
                if t_2(environment.getattr(environment.getattr(l_1_vlan, 'querier'), 'last_member_query_interval')):
                    pass
                    yield 'ip igmp snooping vlan '
                    yield str(environment.getattr(l_1_vlan, 'id'))
                    yield ' querier last-member-query-interval '
                    yield str(environment.getattr(environment.getattr(l_1_vlan, 'querier'), 'last_member_query_interval'))
                    yield '\n'
                if t_2(environment.getattr(environment.getattr(l_1_vlan, 'querier'), 'last_member_query_count')):
                    pass
                    yield 'ip igmp snooping vlan '
                    yield str(environment.getattr(l_1_vlan, 'id'))
                    yield ' querier last-member-query-count '
                    yield str(environment.getattr(environment.getattr(l_1_vlan, 'querier'), 'last_member_query_count'))
                    yield '\n'
                if t_2(environment.getattr(environment.getattr(l_1_vlan, 'querier'), 'startup_query_interval')):
                    pass
                    yield 'ip igmp snooping vlan '
                    yield str(environment.getattr(l_1_vlan, 'id'))
                    yield ' querier startup-query-interval '
                    yield str(environment.getattr(environment.getattr(l_1_vlan, 'querier'), 'startup_query_interval'))
                    yield '\n'
                if t_2(environment.getattr(environment.getattr(l_1_vlan, 'querier'), 'startup_query_count')):
                    pass
                    yield 'ip igmp snooping vlan '
                    yield str(environment.getattr(l_1_vlan, 'id'))
                    yield ' querier startup-query-count '
                    yield str(environment.getattr(environment.getattr(l_1_vlan, 'querier'), 'startup_query_count'))
                    yield '\n'
                if t_2(environment.getattr(environment.getattr(l_1_vlan, 'querier'), 'version')):
                    pass
                    yield 'ip igmp snooping vlan '
                    yield str(environment.getattr(l_1_vlan, 'id'))
                    yield ' querier version '
                    yield str(environment.getattr(environment.getattr(l_1_vlan, 'querier'), 'version'))
                    yield '\n'
            if t_2(environment.getattr(l_1_vlan, 'max_groups')):
                pass
                yield 'ip igmp snooping vlan '
                yield str(environment.getattr(l_1_vlan, 'id'))
                yield ' max-groups '
                yield str(environment.getattr(l_1_vlan, 'max_groups'))
                yield '\n'
            if t_2(environment.getattr(l_1_vlan, 'fast_leave'), True):
                pass
                yield 'ip igmp snooping vlan '
                yield str(environment.getattr(l_1_vlan, 'id'))
                yield ' fast-leave\n'
            elif t_2(environment.getattr(l_1_vlan, 'fast_leave'), False):
                pass
                yield 'no ip igmp snooping vlan '
                yield str(environment.getattr(l_1_vlan, 'id'))
                yield ' fast-leave\n'
        l_1_vlan = missing
        if t_2(environment.getattr((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping), 'querier')):
            pass
            if t_2(environment.getattr(environment.getattr((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping), 'querier'), 'enabled'), True):
                pass
                yield 'ip igmp snooping querier\n'
            elif t_2(environment.getattr(environment.getattr((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping), 'querier'), 'enabled'), False):
                pass
                yield 'no ip igmp snooping querier\n'
            if t_2(environment.getattr(environment.getattr((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping), 'querier'), 'address')):
                pass
                yield 'ip igmp snooping querier address '
                yield str(environment.getattr(environment.getattr((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping), 'querier'), 'address'))
                yield '\n'
            if t_2(environment.getattr(environment.getattr((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping), 'querier'), 'query_interval')):
                pass
                yield 'ip igmp snooping querier query-interval '
                yield str(environment.getattr(environment.getattr((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping), 'querier'), 'query_interval'))
                yield '\n'
            if t_2(environment.getattr(environment.getattr((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping), 'querier'), 'max_response_time')):
                pass
                yield 'ip igmp snooping querier max-response-time '
                yield str(environment.getattr(environment.getattr((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping), 'querier'), 'max_response_time'))
                yield '\n'
            if t_2(environment.getattr(environment.getattr((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping), 'querier'), 'last_member_query_interval')):
                pass
                yield 'ip igmp snooping querier last-member-query-interval '
                yield str(environment.getattr(environment.getattr((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping), 'querier'), 'last_member_query_interval'))
                yield '\n'
            if t_2(environment.getattr(environment.getattr((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping), 'querier'), 'last_member_query_count')):
                pass
                yield 'ip igmp snooping querier last-member-query-count '
                yield str(environment.getattr(environment.getattr((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping), 'querier'), 'last_member_query_count'))
                yield '\n'
            if t_2(environment.getattr(environment.getattr((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping), 'querier'), 'startup_query_interval')):
                pass
                yield 'ip igmp snooping querier startup-query-interval '
                yield str(environment.getattr(environment.getattr((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping), 'querier'), 'startup_query_interval'))
                yield '\n'
            if t_2(environment.getattr(environment.getattr((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping), 'querier'), 'startup_query_count')):
                pass
                yield 'ip igmp snooping querier startup-query-count '
                yield str(environment.getattr(environment.getattr((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping), 'querier'), 'startup_query_count'))
                yield '\n'
            if t_2(environment.getattr(environment.getattr((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping), 'querier'), 'version')):
                pass
                yield 'ip igmp snooping querier version '
                yield str(environment.getattr(environment.getattr((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping), 'querier'), 'version'))
                yield '\n'
        if t_2(environment.getattr((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping), 'proxy'), True):
            pass
            yield '!\nip igmp snooping proxy\n'
        for l_1_vlan in t_1(environment.getattr((undefined(name='ip_igmp_snooping') if l_0_ip_igmp_snooping is missing else l_0_ip_igmp_snooping), 'vlans'), 'id'):
            _loop_vars = {}
            pass
            if t_2(environment.getattr(l_1_vlan, 'proxy'), True):
                pass
                yield 'ip igmp snooping vlan '
                yield str(environment.getattr(l_1_vlan, 'id'))
                yield ' proxy\n'
            elif t_2(environment.getattr(l_1_vlan, 'proxy'), False):
                pass
                yield 'no ip igmp snooping vlan '
                yield str(environment.getattr(l_1_vlan, 'id'))
                yield ' proxy\n'
        l_1_vlan = missing

blocks = {}
debug_info = '2=24&3=26&7=29&10=32&11=35&13=37&14=40&16=42&17=45&19=47&21=50&24=53&25=56&26=59&27=61&28=64&30=66&31=68&32=71&33=73&34=76&36=78&37=81&39=85&40=88&42=92&43=95&45=99&46=102&48=106&49=109&51=113&52=116&54=120&55=123&57=127&58=130&61=134&62=137&64=141&65=144&66=146&67=149&70=152&71=154&73=157&76=160&77=163&79=165&80=168&82=170&83=173&85=175&86=178&88=180&89=183&91=185&92=188&94=190&95=193&97=195&98=198&101=200&105=203&106=206&107=209&108=211&109=214'