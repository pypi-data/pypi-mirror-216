from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/router-bfd.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_router_bfd = resolve('router_bfd')
    l_0_localint = resolve('localint')
    try:
        t_1 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_1((undefined(name='router_bfd') if l_0_router_bfd is missing else l_0_router_bfd)):
        pass
        yield '!\nrouter bfd\n'
        if ((t_1(environment.getattr((undefined(name='router_bfd') if l_0_router_bfd is missing else l_0_router_bfd), 'interval')) and t_1(environment.getattr((undefined(name='router_bfd') if l_0_router_bfd is missing else l_0_router_bfd), 'min_rx'))) and t_1(environment.getattr((undefined(name='router_bfd') if l_0_router_bfd is missing else l_0_router_bfd), 'multiplier'))):
            pass
            yield '   interval '
            yield str(environment.getattr((undefined(name='router_bfd') if l_0_router_bfd is missing else l_0_router_bfd), 'interval'))
            yield ' min-rx '
            yield str(environment.getattr((undefined(name='router_bfd') if l_0_router_bfd is missing else l_0_router_bfd), 'min_rx'))
            yield ' multiplier '
            yield str(environment.getattr((undefined(name='router_bfd') if l_0_router_bfd is missing else l_0_router_bfd), 'multiplier'))
            yield ' default\n'
        if ((t_1(environment.getattr(environment.getattr((undefined(name='router_bfd') if l_0_router_bfd is missing else l_0_router_bfd), 'multihop'), 'interval')) and t_1(environment.getattr(environment.getattr((undefined(name='router_bfd') if l_0_router_bfd is missing else l_0_router_bfd), 'multihop'), 'min_rx'))) and t_1(environment.getattr(environment.getattr((undefined(name='router_bfd') if l_0_router_bfd is missing else l_0_router_bfd), 'multihop'), 'multiplier'))):
            pass
            yield '   multihop interval '
            yield str(environment.getattr(environment.getattr((undefined(name='router_bfd') if l_0_router_bfd is missing else l_0_router_bfd), 'multihop'), 'interval'))
            yield ' min-rx '
            yield str(environment.getattr(environment.getattr((undefined(name='router_bfd') if l_0_router_bfd is missing else l_0_router_bfd), 'multihop'), 'min_rx'))
            yield ' multiplier '
            yield str(environment.getattr(environment.getattr((undefined(name='router_bfd') if l_0_router_bfd is missing else l_0_router_bfd), 'multihop'), 'multiplier'))
            yield '\n'
        if t_1(environment.getattr((undefined(name='router_bfd') if l_0_router_bfd is missing else l_0_router_bfd), 'sbfd')):
            pass
            yield '   !\n   sbfd\n'
            if (t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bfd') if l_0_router_bfd is missing else l_0_router_bfd), 'sbfd'), 'local_interface'), 'name')) and (t_1(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bfd') if l_0_router_bfd is missing else l_0_router_bfd), 'sbfd'), 'local_interface'), 'protocols'), 'ipv4'), True) or t_1(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bfd') if l_0_router_bfd is missing else l_0_router_bfd), 'sbfd'), 'local_interface'), 'protocols'), 'ipv6'), True))):
                pass
                l_0_localint = environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bfd') if l_0_router_bfd is missing else l_0_router_bfd), 'sbfd'), 'local_interface'), 'name')
                context.vars['localint'] = l_0_localint
                context.exported_vars.add('localint')
                if t_1(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bfd') if l_0_router_bfd is missing else l_0_router_bfd), 'sbfd'), 'local_interface'), 'protocols'), 'ipv4'), True):
                    pass
                    l_0_localint = str_join(((undefined(name='localint') if l_0_localint is missing else l_0_localint), ' ipv4', ))
                    context.vars['localint'] = l_0_localint
                    context.exported_vars.add('localint')
                if t_1(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bfd') if l_0_router_bfd is missing else l_0_router_bfd), 'sbfd'), 'local_interface'), 'protocols'), 'ipv6'), True):
                    pass
                    l_0_localint = str_join(((undefined(name='localint') if l_0_localint is missing else l_0_localint), ' ipv6', ))
                    context.vars['localint'] = l_0_localint
                    context.exported_vars.add('localint')
                yield '      local-interface '
                yield str((undefined(name='localint') if l_0_localint is missing else l_0_localint))
                yield '\n'
            if (t_1(environment.getattr(environment.getattr((undefined(name='router_bfd') if l_0_router_bfd is missing else l_0_router_bfd), 'sbfd'), 'initiator_interval')) and t_1(environment.getattr(environment.getattr((undefined(name='router_bfd') if l_0_router_bfd is missing else l_0_router_bfd), 'sbfd'), 'initiator_multiplier'))):
                pass
                yield '      initiator interval '
                yield str(environment.getattr(environment.getattr((undefined(name='router_bfd') if l_0_router_bfd is missing else l_0_router_bfd), 'sbfd'), 'initiator_interval'))
                yield ' multiplier '
                yield str(environment.getattr(environment.getattr((undefined(name='router_bfd') if l_0_router_bfd is missing else l_0_router_bfd), 'sbfd'), 'initiator_multiplier'))
                yield '\n'
            if t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bfd') if l_0_router_bfd is missing else l_0_router_bfd), 'sbfd'), 'reflector'), 'min_rx')):
                pass
                yield '      reflector min-rx '
                yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bfd') if l_0_router_bfd is missing else l_0_router_bfd), 'sbfd'), 'reflector'), 'min_rx'))
                yield '\n'
            if t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bfd') if l_0_router_bfd is missing else l_0_router_bfd), 'sbfd'), 'reflector'), 'local_discriminator')):
                pass
                yield '      reflector local-discriminator '
                yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bfd') if l_0_router_bfd is missing else l_0_router_bfd), 'sbfd'), 'reflector'), 'local_discriminator'))
                yield '\n'

blocks = {}
debug_info = '2=19&5=22&6=25&8=31&9=34&11=40&14=43&18=45&19=48&20=50&22=53&23=55&25=59&27=61&28=64&30=68&31=71&33=73&34=76'