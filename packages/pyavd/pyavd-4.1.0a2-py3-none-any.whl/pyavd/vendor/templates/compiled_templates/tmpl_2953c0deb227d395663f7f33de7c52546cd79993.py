from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/management-ssh.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_management_ssh = resolve('management_ssh')
    try:
        t_1 = environment.filters['arista.avd.natural_sort']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.natural_sort' found.")
    try:
        t_2 = environment.filters['join']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No filter named 'join' found.")
    try:
        t_3 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_3((undefined(name='management_ssh') if l_0_management_ssh is missing else l_0_management_ssh)):
        pass
        yield '!\nmanagement ssh\n'
        if t_3(environment.getattr((undefined(name='management_ssh') if l_0_management_ssh is missing else l_0_management_ssh), 'access_groups')):
            pass
            for l_1_access_group in environment.getattr((undefined(name='management_ssh') if l_0_management_ssh is missing else l_0_management_ssh), 'access_groups'):
                l_1_acl_cli = missing
                _loop_vars = {}
                pass
                l_1_acl_cli = str_join(('ip access-group ', environment.getattr(l_1_access_group, 'name'), ))
                _loop_vars['acl_cli'] = l_1_acl_cli
                if t_3(environment.getattr(l_1_access_group, 'vrf')):
                    pass
                    l_1_acl_cli = str_join(((undefined(name='acl_cli') if l_1_acl_cli is missing else l_1_acl_cli), ' vrf ', environment.getattr(l_1_access_group, 'vrf'), ))
                    _loop_vars['acl_cli'] = l_1_acl_cli
                l_1_acl_cli = str_join(((undefined(name='acl_cli') if l_1_acl_cli is missing else l_1_acl_cli), ' in', ))
                _loop_vars['acl_cli'] = l_1_acl_cli
                yield '   '
                yield str((undefined(name='acl_cli') if l_1_acl_cli is missing else l_1_acl_cli))
                yield '\n'
            l_1_access_group = l_1_acl_cli = missing
        if t_3(environment.getattr((undefined(name='management_ssh') if l_0_management_ssh is missing else l_0_management_ssh), 'ipv6_access_groups')):
            pass
            for l_1_ipv6_access_group in environment.getattr((undefined(name='management_ssh') if l_0_management_ssh is missing else l_0_management_ssh), 'ipv6_access_groups'):
                l_1_ipv6_acl_cli = missing
                _loop_vars = {}
                pass
                l_1_ipv6_acl_cli = str_join(('ipv6 access-group ', environment.getattr(l_1_ipv6_access_group, 'name'), ))
                _loop_vars['ipv6_acl_cli'] = l_1_ipv6_acl_cli
                if t_3(environment.getattr(l_1_ipv6_access_group, 'vrf')):
                    pass
                    l_1_ipv6_acl_cli = str_join(((undefined(name='ipv6_acl_cli') if l_1_ipv6_acl_cli is missing else l_1_ipv6_acl_cli), ' vrf ', environment.getattr(l_1_ipv6_access_group, 'vrf'), ))
                    _loop_vars['ipv6_acl_cli'] = l_1_ipv6_acl_cli
                l_1_ipv6_acl_cli = str_join(((undefined(name='ipv6_acl_cli') if l_1_ipv6_acl_cli is missing else l_1_ipv6_acl_cli), ' in', ))
                _loop_vars['ipv6_acl_cli'] = l_1_ipv6_acl_cli
                yield '   '
                yield str((undefined(name='ipv6_acl_cli') if l_1_ipv6_acl_cli is missing else l_1_ipv6_acl_cli))
                yield '\n'
            l_1_ipv6_access_group = l_1_ipv6_acl_cli = missing
        if t_3(environment.getattr((undefined(name='management_ssh') if l_0_management_ssh is missing else l_0_management_ssh), 'idle_timeout')):
            pass
            yield '   idle-timeout '
            yield str(environment.getattr((undefined(name='management_ssh') if l_0_management_ssh is missing else l_0_management_ssh), 'idle_timeout'))
            yield '\n'
        if t_3(environment.getattr(environment.getattr((undefined(name='management_ssh') if l_0_management_ssh is missing else l_0_management_ssh), 'connection'), 'limit')):
            pass
            yield '   connection limit '
            yield str(environment.getattr(environment.getattr((undefined(name='management_ssh') if l_0_management_ssh is missing else l_0_management_ssh), 'connection'), 'limit'))
            yield '\n'
        if t_3(environment.getattr(environment.getattr((undefined(name='management_ssh') if l_0_management_ssh is missing else l_0_management_ssh), 'connection'), 'per_host')):
            pass
            yield '   connection per-host '
            yield str(environment.getattr(environment.getattr((undefined(name='management_ssh') if l_0_management_ssh is missing else l_0_management_ssh), 'connection'), 'per_host'))
            yield '\n'
        if t_3(environment.getattr((undefined(name='management_ssh') if l_0_management_ssh is missing else l_0_management_ssh), 'cipher')):
            pass
            yield '   cipher '
            yield str(t_2(context.eval_ctx, environment.getattr((undefined(name='management_ssh') if l_0_management_ssh is missing else l_0_management_ssh), 'cipher'), ' '))
            yield '\n'
        if t_3(environment.getattr((undefined(name='management_ssh') if l_0_management_ssh is missing else l_0_management_ssh), 'key_exchange')):
            pass
            yield '   key-exchange '
            yield str(t_2(context.eval_ctx, environment.getattr((undefined(name='management_ssh') if l_0_management_ssh is missing else l_0_management_ssh), 'key_exchange'), ' '))
            yield '\n'
        if t_3(environment.getattr((undefined(name='management_ssh') if l_0_management_ssh is missing else l_0_management_ssh), 'mac')):
            pass
            yield '   mac '
            yield str(t_2(context.eval_ctx, environment.getattr((undefined(name='management_ssh') if l_0_management_ssh is missing else l_0_management_ssh), 'mac'), ' '))
            yield '\n'
        if t_3(environment.getattr(environment.getattr((undefined(name='management_ssh') if l_0_management_ssh is missing else l_0_management_ssh), 'hostkey'), 'server')):
            pass
            yield '   hostkey server '
            yield str(t_2(context.eval_ctx, environment.getattr(environment.getattr((undefined(name='management_ssh') if l_0_management_ssh is missing else l_0_management_ssh), 'hostkey'), 'server'), ' '))
            yield '\n'
        if t_3(environment.getattr((undefined(name='management_ssh') if l_0_management_ssh is missing else l_0_management_ssh), 'enable'), False):
            pass
            yield '   shutdown\n'
        elif t_3(environment.getattr((undefined(name='management_ssh') if l_0_management_ssh is missing else l_0_management_ssh), 'enable'), True):
            pass
            yield '   no shutdown\n'
        if t_3(environment.getattr((undefined(name='management_ssh') if l_0_management_ssh is missing else l_0_management_ssh), 'log_level')):
            pass
            yield '   log-level '
            yield str(environment.getattr((undefined(name='management_ssh') if l_0_management_ssh is missing else l_0_management_ssh), 'log_level'))
            yield '\n'
        for l_1_vrf in t_1(environment.getattr((undefined(name='management_ssh') if l_0_management_ssh is missing else l_0_management_ssh), 'vrfs'), 'name'):
            _loop_vars = {}
            pass
            yield '   !\n   vrf '
            yield str(environment.getattr(l_1_vrf, 'name'))
            yield '\n'
            if t_3(environment.getattr(l_1_vrf, 'enable'), True):
                pass
                yield '      no shutdown\n'
            elif t_3(environment.getattr(l_1_vrf, 'enable'), False):
                pass
                yield '      shutdown\n'
        l_1_vrf = missing

blocks = {}
debug_info = '2=30&5=33&6=35&7=39&8=41&9=43&11=45&12=48&15=51&16=53&17=57&18=59&19=61&21=63&22=66&25=69&26=72&28=74&29=77&31=79&32=82&34=84&35=87&37=89&38=92&40=94&41=97&43=99&44=102&46=104&48=107&51=110&52=113&54=115&56=119&57=121&59=124'