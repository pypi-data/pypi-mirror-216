from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'documentation/dhcp-relay.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_dhcp_relay = resolve('dhcp_relay')
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
    if t_2((undefined(name='dhcp_relay') if l_0_dhcp_relay is missing else l_0_dhcp_relay)):
        pass
        yield '\n## DHCP Relay\n\n### DHCP Relay Summary\n'
        if t_2(environment.getattr((undefined(name='dhcp_relay') if l_0_dhcp_relay is missing else l_0_dhcp_relay), 'tunnel_requests_disabled'), True):
            pass
            yield '\n- DHCP Relay is disabled for tunnelled requests\n'
        elif t_2(environment.getattr((undefined(name='dhcp_relay') if l_0_dhcp_relay is missing else l_0_dhcp_relay), 'tunnel_requests_disabled'), False):
            pass
            yield '\n- DHCP Relay is enabled for tunnelled requests\n'
        if t_2(environment.getattr((undefined(name='dhcp_relay') if l_0_dhcp_relay is missing else l_0_dhcp_relay), 'servers')):
            pass
            yield '\n| DHCP Relay Servers |\n| ------------------ |\n'
            for l_1_server in t_1(environment.getattr((undefined(name='dhcp_relay') if l_0_dhcp_relay is missing else l_0_dhcp_relay), 'servers')):
                _loop_vars = {}
                pass
                yield '| '
                yield str(l_1_server)
                yield ' |\n'
            l_1_server = missing
        yield '\n### DHCP Relay Configuration\n\n```eos\n'
        template = environment.get_template('eos/dhcp-relay.j2', 'documentation/dhcp-relay.j2')
        for event in template.root_render_func(template.new_context(context.get_all(), True, {})):
            yield event
        yield '```\n'

blocks = {}
debug_info = '2=24&7=27&10=30&14=33&18=36&19=40&26=44'