from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/system.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_system = resolve('system')
    l_0_cp_mss_cli = resolve('cp_mss_cli')
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
    if t_2(environment.getattr((undefined(name='system') if l_0_system is missing else l_0_system), 'control_plane')):
        pass
        yield '!\nsystem control-plane\n'
        if (t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='system') if l_0_system is missing else l_0_system), 'control_plane'), 'tcp_mss'), 'ipv4')) or t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='system') if l_0_system is missing else l_0_system), 'control_plane'), 'tcp_mss'), 'ipv6'))):
            pass
            l_0_cp_mss_cli = 'tcp mss ceiling'
            context.vars['cp_mss_cli'] = l_0_cp_mss_cli
            context.exported_vars.add('cp_mss_cli')
            if t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='system') if l_0_system is missing else l_0_system), 'control_plane'), 'tcp_mss'), 'ipv4')):
                pass
                l_0_cp_mss_cli = str_join(((undefined(name='cp_mss_cli') if l_0_cp_mss_cli is missing else l_0_cp_mss_cli), ' ipv4 ', environment.getattr(environment.getattr(environment.getattr((undefined(name='system') if l_0_system is missing else l_0_system), 'control_plane'), 'tcp_mss'), 'ipv4'), ))
                context.vars['cp_mss_cli'] = l_0_cp_mss_cli
                context.exported_vars.add('cp_mss_cli')
            if t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='system') if l_0_system is missing else l_0_system), 'control_plane'), 'tcp_mss'), 'ipv6')):
                pass
                l_0_cp_mss_cli = str_join(((undefined(name='cp_mss_cli') if l_0_cp_mss_cli is missing else l_0_cp_mss_cli), ' ipv6 ', environment.getattr(environment.getattr(environment.getattr((undefined(name='system') if l_0_system is missing else l_0_system), 'control_plane'), 'tcp_mss'), 'ipv6'), ))
                context.vars['cp_mss_cli'] = l_0_cp_mss_cli
                context.exported_vars.add('cp_mss_cli')
            yield '   '
            yield str((undefined(name='cp_mss_cli') if l_0_cp_mss_cli is missing else l_0_cp_mss_cli))
            yield '\n'
        for l_1_acl_set in t_1(environment.getattr(environment.getattr((undefined(name='system') if l_0_system is missing else l_0_system), 'control_plane'), 'ipv4_access_groups')):
            l_1_cp_ipv4_access_grp = missing
            _loop_vars = {}
            pass
            l_1_cp_ipv4_access_grp = str_join(('ip access-group ', environment.getattr(l_1_acl_set, 'acl_name'), ))
            _loop_vars['cp_ipv4_access_grp'] = l_1_cp_ipv4_access_grp
            if t_2(environment.getattr(l_1_acl_set, 'vrf')):
                pass
                l_1_cp_ipv4_access_grp = str_join(((undefined(name='cp_ipv4_access_grp') if l_1_cp_ipv4_access_grp is missing else l_1_cp_ipv4_access_grp), ' vrf ', environment.getattr(l_1_acl_set, 'vrf'), ))
                _loop_vars['cp_ipv4_access_grp'] = l_1_cp_ipv4_access_grp
            l_1_cp_ipv4_access_grp = str_join(((undefined(name='cp_ipv4_access_grp') if l_1_cp_ipv4_access_grp is missing else l_1_cp_ipv4_access_grp), ' in', ))
            _loop_vars['cp_ipv4_access_grp'] = l_1_cp_ipv4_access_grp
            yield '   '
            yield str((undefined(name='cp_ipv4_access_grp') if l_1_cp_ipv4_access_grp is missing else l_1_cp_ipv4_access_grp))
            yield '\n'
        l_1_acl_set = l_1_cp_ipv4_access_grp = missing
        for l_1_acl_set in t_1(environment.getattr(environment.getattr((undefined(name='system') if l_0_system is missing else l_0_system), 'control_plane'), 'ipv6_access_groups')):
            l_1_cp_ipv6_access_grp = missing
            _loop_vars = {}
            pass
            l_1_cp_ipv6_access_grp = str_join(('ipv6 access-group ', environment.getattr(l_1_acl_set, 'acl_name'), ))
            _loop_vars['cp_ipv6_access_grp'] = l_1_cp_ipv6_access_grp
            if t_2(environment.getattr(l_1_acl_set, 'vrf')):
                pass
                l_1_cp_ipv6_access_grp = str_join(((undefined(name='cp_ipv6_access_grp') if l_1_cp_ipv6_access_grp is missing else l_1_cp_ipv6_access_grp), ' vrf ', environment.getattr(l_1_acl_set, 'vrf'), ))
                _loop_vars['cp_ipv6_access_grp'] = l_1_cp_ipv6_access_grp
            l_1_cp_ipv6_access_grp = str_join(((undefined(name='cp_ipv6_access_grp') if l_1_cp_ipv6_access_grp is missing else l_1_cp_ipv6_access_grp), ' in', ))
            _loop_vars['cp_ipv6_access_grp'] = l_1_cp_ipv6_access_grp
            yield '   '
            yield str((undefined(name='cp_ipv6_access_grp') if l_1_cp_ipv6_access_grp is missing else l_1_cp_ipv6_access_grp))
            yield '\n'
        l_1_acl_set = l_1_cp_ipv6_access_grp = missing

blocks = {}
debug_info = '2=25&6=28&7=30&8=33&9=35&11=38&12=40&14=44&17=46&18=50&19=52&20=54&22=56&23=59&26=62&27=66&28=68&29=70&31=72&32=75'