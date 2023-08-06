from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/event-handlers.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_event_handlers = resolve('event_handlers')
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
    if t_2((undefined(name='event_handlers') if l_0_event_handlers is missing else l_0_event_handlers)):
        pass
        for l_1_handler in t_1((undefined(name='event_handlers') if l_0_event_handlers is missing else l_0_event_handlers), 'name'):
            _loop_vars = {}
            pass
            yield '!\nevent-handler '
            yield str(environment.getattr(l_1_handler, 'name'))
            yield '\n'
            if t_2(environment.getattr(l_1_handler, 'trigger')):
                pass
                yield '   trigger '
                yield str(environment.getattr(l_1_handler, 'trigger'))
                yield '\n'
                if t_2(environment.getattr(l_1_handler, 'regex')):
                    pass
                    yield '      regex '
                    yield str(environment.getattr(l_1_handler, 'regex'))
                    yield '\n'
            if (t_2(environment.getattr(l_1_handler, 'action')) and t_2(environment.getattr(l_1_handler, 'action_type'))):
                pass
                yield '   action '
                yield str(environment.getattr(l_1_handler, 'action_type'))
                yield ' '
                yield str(environment.getattr(l_1_handler, 'action'))
                yield '\n'
            if t_2(environment.getattr(l_1_handler, 'delay')):
                pass
                yield '   delay '
                yield str(environment.getattr(l_1_handler, 'delay'))
                yield '\n'
            if t_2(environment.getattr(l_1_handler, 'asynchronous'), True):
                pass
                yield '   asynchronous\n'
        l_1_handler = missing

blocks = {}
debug_info = '2=24&3=26&5=30&6=32&7=35&8=37&9=40&12=42&13=45&15=49&16=52&18=54'