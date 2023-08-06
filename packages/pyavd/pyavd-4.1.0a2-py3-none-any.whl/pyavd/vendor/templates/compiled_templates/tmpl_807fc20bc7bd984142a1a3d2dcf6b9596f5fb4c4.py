from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/router-igmp.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_router_igmp = resolve('router_igmp')
    try:
        t_1 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_1((undefined(name='router_igmp') if l_0_router_igmp is missing else l_0_router_igmp)):
        pass
        yield '!\nrouter igmp\n'
        if t_1(environment.getattr((undefined(name='router_igmp') if l_0_router_igmp is missing else l_0_router_igmp), 'ssm_aware'), True):
            pass
            yield '   ssm aware\n'

blocks = {}
debug_info = '2=18&5=21'