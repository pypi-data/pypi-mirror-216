from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'documentation/cvx.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_cvx = resolve('cvx')
    l_0_peer_hosts = resolve('peer_hosts')
    l_0_enabled = resolve('enabled')
    l_0_settings = resolve('settings')
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
    if t_3((undefined(name='cvx') if l_0_cvx is missing else l_0_cvx)):
        pass
        yield '\n## CVX\n'
        if t_3(environment.getattr((undefined(name='cvx') if l_0_cvx is missing else l_0_cvx), 'peer_hosts')):
            pass
            yield '\n| Peer Hosts |\n| ---------- |\n'
            l_0_peer_hosts = t_2(context.eval_ctx, t_1(environment.getattr((undefined(name='cvx') if l_0_cvx is missing else l_0_cvx), 'peer_hosts')), ', ')
            context.vars['peer_hosts'] = l_0_peer_hosts
            context.exported_vars.add('peer_hosts')
        yield '| '
        yield str((undefined(name='peer_hosts') if l_0_peer_hosts is missing else l_0_peer_hosts))
        yield ' |\n'
        if t_3(environment.getattr((undefined(name='cvx') if l_0_cvx is missing else l_0_cvx), 'shutdown'), True):
            pass
            yield '\nCVX is disabled\n'
        elif t_3(environment.getattr((undefined(name='cvx') if l_0_cvx is missing else l_0_cvx), 'shutdown'), False):
            pass
            yield '\nCVX is enabled\n'
            if t_3(environment.getattr((undefined(name='cvx') if l_0_cvx is missing else l_0_cvx), 'services')):
                pass
                yield '\n### CVX services\n\n| Service | Enabled | Settings |\n| ------- | ------- | -------- |\n'
                if t_3(environment.getattr(environment.getattr((undefined(name='cvx') if l_0_cvx is missing else l_0_cvx), 'services'), 'mcs')):
                    pass
                    if t_3(environment.getattr(environment.getattr(environment.getattr((undefined(name='cvx') if l_0_cvx is missing else l_0_cvx), 'services'), 'mcs'), 'shutdown')):
                        pass
                        l_0_enabled = (not environment.getattr(environment.getattr(environment.getattr((undefined(name='cvx') if l_0_cvx is missing else l_0_cvx), 'services'), 'mcs'), 'shutdown'))
                        context.vars['enabled'] = l_0_enabled
                        context.exported_vars.add('enabled')
                    else:
                        pass
                        l_0_enabled = '-'
                        context.vars['enabled'] = l_0_enabled
                        context.exported_vars.add('enabled')
                    l_0_settings = []
                    context.vars['settings'] = l_0_settings
                    context.exported_vars.add('settings')
                    if t_3(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='cvx') if l_0_cvx is missing else l_0_cvx), 'services'), 'mcs'), 'redis'), 'password')):
                        pass
                        context.call(environment.getattr((undefined(name='settings') if l_0_settings is missing else l_0_settings), 'append'), 'Redis Password Set')
                    yield '| MCS | '
                    yield str((undefined(name='enabled') if l_0_enabled is missing else l_0_enabled))
                    yield ' | '
                    yield str(t_2(context.eval_ctx, (undefined(name='settings') if l_0_settings is missing else l_0_settings), '<br>'))
                    yield ' |\n'
                if t_3(environment.getattr(environment.getattr((undefined(name='cvx') if l_0_cvx is missing else l_0_cvx), 'services'), 'vxlan')):
                    pass
                    if t_3(environment.getattr(environment.getattr(environment.getattr((undefined(name='cvx') if l_0_cvx is missing else l_0_cvx), 'services'), 'vxlan'), 'shutdown')):
                        pass
                        l_0_enabled = (not environment.getattr(environment.getattr(environment.getattr((undefined(name='cvx') if l_0_cvx is missing else l_0_cvx), 'services'), 'vxlan'), 'shutdown'))
                        context.vars['enabled'] = l_0_enabled
                        context.exported_vars.add('enabled')
                    else:
                        pass
                        l_0_enabled = '-'
                        context.vars['enabled'] = l_0_enabled
                        context.exported_vars.add('enabled')
                    l_0_settings = []
                    context.vars['settings'] = l_0_settings
                    context.exported_vars.add('settings')
                    if t_3(environment.getattr(environment.getattr(environment.getattr((undefined(name='cvx') if l_0_cvx is missing else l_0_cvx), 'services'), 'vxlan'), 'vtep_mac_learning')):
                        pass
                        context.call(environment.getattr((undefined(name='settings') if l_0_settings is missing else l_0_settings), 'append'), str_join(('VTEP MAC learning: ', environment.getattr(environment.getattr(environment.getattr((undefined(name='cvx') if l_0_cvx is missing else l_0_cvx), 'services'), 'vxlan'), 'vtep_mac_learning'), )))
                    yield '| VXLAN | '
                    yield str((undefined(name='enabled') if l_0_enabled is missing else l_0_enabled))
                    yield ' | '
                    yield str(t_2(context.eval_ctx, (undefined(name='settings') if l_0_settings is missing else l_0_settings), '<br>'))
                    yield ' |\n'
        yield '\n### CVX configuration\n\n```eos\n'
        template = environment.get_template('eos/cvx.j2', 'documentation/cvx.j2')
        for event in template.root_render_func(template.new_context(context.get_all(), True, {'enabled': l_0_enabled, 'peer_hosts': l_0_peer_hosts, 'settings': l_0_settings})):
            yield event
        yield '```\n'

blocks = {}
debug_info = '2=33&5=36&9=39&11=43&12=45&15=48&18=51&24=54&25=56&26=58&28=63&30=66&31=69&32=71&34=73&36=77&37=79&38=81&40=86&42=89&43=92&44=94&46=96&54=101'