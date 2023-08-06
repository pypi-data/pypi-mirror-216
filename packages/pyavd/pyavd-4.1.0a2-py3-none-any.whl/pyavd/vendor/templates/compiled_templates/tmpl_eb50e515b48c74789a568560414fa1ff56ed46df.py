from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/ip-nat-part1.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_ip_nat = resolve('ip_nat')
    try:
        t_1 = environment.filters['arista.avd.default']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.default' found.")
    try:
        t_2 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_2((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat)):
        pass
        yield '!\n'
        if t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'translation'), 'address_selection'), 'any'), False):
            pass
            yield 'ip nat translation address selection any\n'
        if t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'translation'), 'address_selection'), 'hash_field_source_ip'), False):
            pass
            yield 'ip nat translation address selection hash field source-ip\n'
        for l_1_timeout in t_1(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'translation'), 'timeouts'), []):
            _loop_vars = {}
            pass
            yield 'ip nat translation '
            yield str(environment.getattr(l_1_timeout, 'protocol'))
            yield '-timeout '
            yield str(environment.getattr(l_1_timeout, 'timeout'))
            yield '\n'
        l_1_timeout = missing
        if t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'translation'), 'max_entries'), 'limit')):
            pass
            yield 'ip nat translation max-entries '
            yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'translation'), 'max_entries'), 'limit'))
            yield '\n'
        if t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'translation'), 'low_mark'), 'percentage')):
            pass
            yield 'ip nat translation low-mark '
            yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'translation'), 'low_mark'), 'percentage'))
            yield '\n'
        if t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'translation'), 'max_entries'), 'host_limit')):
            pass
            yield 'ip nat translation max-entries '
            yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'translation'), 'max_entries'), 'host_limit'))
            yield ' host\n'
        if t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'translation'), 'low_mark'), 'host_percentage')):
            pass
            yield 'ip nat translation low-mark '
            yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'translation'), 'low_mark'), 'host_percentage'))
            yield ' host\n'
        for l_1_ip_limit in t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'translation'), 'max_entries'), 'ip_limits'), []):
            _loop_vars = {}
            pass
            yield 'ip nat translation max-entries '
            yield str(environment.getattr(l_1_ip_limit, 'limit'))
            yield ' '
            yield str(environment.getattr(l_1_ip_limit, 'ip'))
            yield '\n'
        l_1_ip_limit = missing
        if t_2(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'kernel_buffer_size')):
            pass
            yield 'ip nat kernel buffer size '
            yield str(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'kernel_buffer_size'))
            yield '\n'

blocks = {}
debug_info = '2=24&4=27&7=30&10=33&11=37&13=42&14=45&16=47&17=50&19=52&20=55&22=57&23=60&25=62&26=66&28=71&29=74'