from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/banners.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_banners = resolve('banners')
    try:
        t_1 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_1(environment.getattr((undefined(name='banners') if l_0_banners is missing else l_0_banners), 'login')):
        pass
        yield '!\nbanner login\n'
        yield str(environment.getattr((undefined(name='banners') if l_0_banners is missing else l_0_banners), 'login'))
        yield '\n'
    if t_1(environment.getattr((undefined(name='banners') if l_0_banners is missing else l_0_banners), 'motd')):
        pass
        yield '!\nbanner motd\n'
        yield str(environment.getattr((undefined(name='banners') if l_0_banners is missing else l_0_banners), 'motd'))
        yield '\n'

blocks = {}
debug_info = '2=18&5=21&7=23&10=26'