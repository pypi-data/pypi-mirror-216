from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/queue-monitor-streaming.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_queue_monitor_streaming = resolve('queue_monitor_streaming')
    try:
        t_1 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_1((undefined(name='queue_monitor_streaming') if l_0_queue_monitor_streaming is missing else l_0_queue_monitor_streaming)):
        pass
        yield '!\nqueue-monitor streaming\n'
        if t_1(environment.getattr((undefined(name='queue_monitor_streaming') if l_0_queue_monitor_streaming is missing else l_0_queue_monitor_streaming), 'max_connections')):
            pass
            yield '   max-connections '
            yield str(environment.getattr((undefined(name='queue_monitor_streaming') if l_0_queue_monitor_streaming is missing else l_0_queue_monitor_streaming), 'max_connections'))
            yield '\n'
        if t_1(environment.getattr((undefined(name='queue_monitor_streaming') if l_0_queue_monitor_streaming is missing else l_0_queue_monitor_streaming), 'ip_access_group')):
            pass
            yield '   ip access-group '
            yield str(environment.getattr((undefined(name='queue_monitor_streaming') if l_0_queue_monitor_streaming is missing else l_0_queue_monitor_streaming), 'ip_access_group'))
            yield '\n'
        if t_1(environment.getattr((undefined(name='queue_monitor_streaming') if l_0_queue_monitor_streaming is missing else l_0_queue_monitor_streaming), 'ipv6_access_group')):
            pass
            yield '   ipv6 access-group '
            yield str(environment.getattr((undefined(name='queue_monitor_streaming') if l_0_queue_monitor_streaming is missing else l_0_queue_monitor_streaming), 'ip_access_group'))
            yield '\n'
        if t_1(environment.getattr((undefined(name='queue_monitor_streaming') if l_0_queue_monitor_streaming is missing else l_0_queue_monitor_streaming), 'vrf')):
            pass
            yield '   vrf '
            yield str(environment.getattr((undefined(name='queue_monitor_streaming') if l_0_queue_monitor_streaming is missing else l_0_queue_monitor_streaming), 'vrf'))
            yield '\n'
        if t_1(environment.getattr((undefined(name='queue_monitor_streaming') if l_0_queue_monitor_streaming is missing else l_0_queue_monitor_streaming), 'enable'), True):
            pass
            yield '   no shutdown\n'
        elif t_1(environment.getattr((undefined(name='queue_monitor_streaming') if l_0_queue_monitor_streaming is missing else l_0_queue_monitor_streaming), 'enable'), False):
            pass
            yield '   shutdown\n'

blocks = {}
debug_info = '2=18&5=21&6=24&8=26&9=29&11=31&12=34&14=36&15=39&17=41&19=44'