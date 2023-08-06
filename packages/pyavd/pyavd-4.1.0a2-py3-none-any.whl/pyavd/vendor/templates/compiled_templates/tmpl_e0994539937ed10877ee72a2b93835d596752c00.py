from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'documentation/aliases.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_aliases = resolve('aliases')
    try:
        t_1 = environment.tests['defined']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No test named 'defined' found.")
    try:
        t_2 = environment.tests['none']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No test named 'none' found.")
    pass
    if (t_1((undefined(name='aliases') if l_0_aliases is missing else l_0_aliases)) and (not t_2((undefined(name='aliases') if l_0_aliases is missing else l_0_aliases)))):
        pass
        yield '\n## Aliases\n\n```eos\n'
        yield str((undefined(name='aliases') if l_0_aliases is missing else l_0_aliases))
        yield '\n!\n```\n'

blocks = {}
debug_info = '2=24&7=27'