from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/tunnel-interfaces.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_tunnel_interfaces = resolve('tunnel_interfaces')
    try:
        t_1 = environment.filters['arista.avd.natural_sort']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.natural_sort' found.")
    try:
        t_2 = environment.filters['indent']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No filter named 'indent' found.")
    try:
        t_3 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    for l_1_tunnel_interface in t_1((undefined(name='tunnel_interfaces') if l_0_tunnel_interfaces is missing else l_0_tunnel_interfaces), 'name'):
        l_1_tcp_mss_ceiling_cli = resolve('tcp_mss_ceiling_cli')
        _loop_vars = {}
        pass
        yield '!\ninterface '
        yield str(environment.getattr(l_1_tunnel_interface, 'name'))
        yield '\n'
        if t_3(environment.getattr(l_1_tunnel_interface, 'description')):
            pass
            yield '   description '
            yield str(environment.getattr(l_1_tunnel_interface, 'description'))
            yield '\n'
        if t_3(environment.getattr(l_1_tunnel_interface, 'shutdown'), True):
            pass
            yield '   shutdown\n'
        elif t_3(environment.getattr(l_1_tunnel_interface, 'shutdown'), False):
            pass
            yield '   no shutdown\n'
        if t_3(environment.getattr(l_1_tunnel_interface, 'mtu')):
            pass
            yield '   mtu '
            yield str(environment.getattr(l_1_tunnel_interface, 'mtu'))
            yield '\n'
        if (t_3(environment.getattr(l_1_tunnel_interface, 'vrf')) and (environment.getattr(l_1_tunnel_interface, 'vrf') != 'default')):
            pass
            yield '   vrf '
            yield str(environment.getattr(l_1_tunnel_interface, 'vrf'))
            yield '\n'
        if t_3(environment.getattr(l_1_tunnel_interface, 'ip_address')):
            pass
            yield '   ip address '
            yield str(environment.getattr(l_1_tunnel_interface, 'ip_address'))
            yield '\n'
        if t_3(environment.getattr(l_1_tunnel_interface, 'ipv6_enable'), True):
            pass
            yield '   ipv6 enable\n'
        if t_3(environment.getattr(l_1_tunnel_interface, 'ipv6_address')):
            pass
            yield '   ipv6 address '
            yield str(environment.getattr(l_1_tunnel_interface, 'ipv6_address'))
            yield '\n'
        if t_3(environment.getattr(l_1_tunnel_interface, 'access_group_in')):
            pass
            yield '   ip access-group '
            yield str(environment.getattr(l_1_tunnel_interface, 'access_group_in'))
            yield ' in\n'
        if t_3(environment.getattr(l_1_tunnel_interface, 'access_group_out')):
            pass
            yield '   ip access-group '
            yield str(environment.getattr(l_1_tunnel_interface, 'access_group_out'))
            yield ' out\n'
        if t_3(environment.getattr(l_1_tunnel_interface, 'ipv6_access_group_in')):
            pass
            yield '   ipv6 access-group '
            yield str(environment.getattr(l_1_tunnel_interface, 'ipv6_access_group_in'))
            yield ' in\n'
        if t_3(environment.getattr(l_1_tunnel_interface, 'ipv6_access_group_out')):
            pass
            yield '   ipv6 access-group '
            yield str(environment.getattr(l_1_tunnel_interface, 'ipv6_access_group_out'))
            yield ' out\n'
        if t_3(environment.getattr(l_1_tunnel_interface, 'tcp_mss_ceiling')):
            pass
            l_1_tcp_mss_ceiling_cli = 'tcp mss ceiling'
            _loop_vars['tcp_mss_ceiling_cli'] = l_1_tcp_mss_ceiling_cli
            if t_3(environment.getattr(environment.getattr(l_1_tunnel_interface, 'tcp_mss_ceiling'), 'ipv4')):
                pass
                l_1_tcp_mss_ceiling_cli = str_join(((undefined(name='tcp_mss_ceiling_cli') if l_1_tcp_mss_ceiling_cli is missing else l_1_tcp_mss_ceiling_cli), ' ipv4 ', environment.getattr(environment.getattr(l_1_tunnel_interface, 'tcp_mss_ceiling'), 'ipv4'), ))
                _loop_vars['tcp_mss_ceiling_cli'] = l_1_tcp_mss_ceiling_cli
            if t_3(environment.getattr(environment.getattr(l_1_tunnel_interface, 'tcp_mss_ceiling'), 'ipv6')):
                pass
                l_1_tcp_mss_ceiling_cli = str_join(((undefined(name='tcp_mss_ceiling_cli') if l_1_tcp_mss_ceiling_cli is missing else l_1_tcp_mss_ceiling_cli), ' ipv6 ', environment.getattr(environment.getattr(l_1_tunnel_interface, 'tcp_mss_ceiling'), 'ipv6'), ))
                _loop_vars['tcp_mss_ceiling_cli'] = l_1_tcp_mss_ceiling_cli
            if t_3(environment.getattr(environment.getattr(l_1_tunnel_interface, 'tcp_mss_ceiling'), 'direction')):
                pass
                l_1_tcp_mss_ceiling_cli = str_join(((undefined(name='tcp_mss_ceiling_cli') if l_1_tcp_mss_ceiling_cli is missing else l_1_tcp_mss_ceiling_cli), ' ', environment.getattr(environment.getattr(l_1_tunnel_interface, 'tcp_mss_ceiling'), 'direction'), ))
                _loop_vars['tcp_mss_ceiling_cli'] = l_1_tcp_mss_ceiling_cli
            yield '   '
            yield str((undefined(name='tcp_mss_ceiling_cli') if l_1_tcp_mss_ceiling_cli is missing else l_1_tcp_mss_ceiling_cli))
            yield '\n'
        if t_3(environment.getattr(l_1_tunnel_interface, 'source_interface')):
            pass
            yield '   tunnel source interface '
            yield str(environment.getattr(l_1_tunnel_interface, 'source_interface'))
            yield '\n'
        if t_3(environment.getattr(l_1_tunnel_interface, 'destination')):
            pass
            yield '   tunnel destination '
            yield str(environment.getattr(l_1_tunnel_interface, 'destination'))
            yield '\n'
        if t_3(environment.getattr(l_1_tunnel_interface, 'path_mtu_discovery'), True):
            pass
            yield '   tunnel path-mtu-discovery\n'
        if t_3(environment.getattr(l_1_tunnel_interface, 'eos_cli')):
            pass
            yield '   '
            yield str(t_2(environment.getattr(l_1_tunnel_interface, 'eos_cli'), 3, False))
            yield '\n'
    l_1_tunnel_interface = l_1_tcp_mss_ceiling_cli = missing

blocks = {}
debug_info = '2=30&4=35&5=37&6=40&8=42&10=45&13=48&14=51&16=53&17=56&19=58&20=61&22=63&25=66&26=69&28=71&29=74&31=76&32=79&34=81&35=84&37=86&38=89&40=91&41=93&42=95&43=97&45=99&46=101&48=103&49=105&51=108&53=110&54=113&56=115&57=118&59=120&62=123&63=126'