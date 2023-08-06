from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/qos.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_qos = resolve('qos')
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
    if t_2((undefined(name='qos') if l_0_qos is missing else l_0_qos)):
        pass
        yield '!\n'
        if t_2(environment.getattr((undefined(name='qos') if l_0_qos is missing else l_0_qos), 'rewrite_dscp'), True):
            pass
            yield 'qos rewrite dscp\n'
        for l_1_cos_map in t_1(environment.getattr(environment.getattr((undefined(name='qos') if l_0_qos is missing else l_0_qos), 'map'), 'cos')):
            _loop_vars = {}
            pass
            yield 'qos map cos '
            yield str(l_1_cos_map)
            yield '\n'
        l_1_cos_map = missing
        for l_1_dscp_map in t_1(environment.getattr(environment.getattr((undefined(name='qos') if l_0_qos is missing else l_0_qos), 'map'), 'dscp')):
            _loop_vars = {}
            pass
            yield 'qos map dscp '
            yield str(l_1_dscp_map)
            yield '\n'
        l_1_dscp_map = missing
        for l_1_tc_map in t_1(environment.getattr(environment.getattr((undefined(name='qos') if l_0_qos is missing else l_0_qos), 'map'), 'traffic_class')):
            _loop_vars = {}
            pass
            yield 'qos map traffic-class '
            yield str(l_1_tc_map)
            yield '\n'
        l_1_tc_map = missing

blocks = {}
debug_info = '2=24&4=27&7=30&8=34&10=37&11=41&13=44&14=48'