from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/ptp.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_ptp = resolve('ptp')
    try:
        t_1 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_1((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp)):
        pass
        yield '!\n'
        if t_1(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'clock_identity')):
            pass
            yield 'ptp clock-identity '
            yield str(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'clock_identity'))
            yield '\n'
        if t_1(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'source'), 'ip')):
            pass
            yield 'ptp source ip '
            yield str(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'source'), 'ip'))
            yield '\n'
        if t_1(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'priority1')):
            pass
            yield 'ptp priority1 '
            yield str(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'priority1'))
            yield '\n'
        if t_1(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'priority2')):
            pass
            yield 'ptp priority2 '
            yield str(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'priority2'))
            yield '\n'
        if t_1(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'ttl')):
            pass
            yield 'ptp ttl '
            yield str(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'ttl'))
            yield '\n'
        if t_1(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'domain')):
            pass
            yield 'ptp domain '
            yield str(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'domain'))
            yield '\n'
        if t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'message_type'), 'general'), 'dscp')):
            pass
            yield 'ptp message-type general dscp '
            yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'message_type'), 'general'), 'dscp'))
            yield ' default\n'
        if t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'message_type'), 'event'), 'dscp')):
            pass
            yield 'ptp message-type event dscp '
            yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'message_type'), 'event'), 'dscp'))
            yield ' default\n'
        if t_1(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'mode')):
            pass
            yield 'ptp mode '
            yield str(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'mode'))
            yield '\n'
        if t_1(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'forward_unicast'), True):
            pass
            yield 'ptp forward-unicast\n'
        if t_1(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'monitor'), 'enabled'), False):
            pass
            yield 'no ptp monitor\n'
        elif t_1(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'monitor')):
            pass
            if t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'monitor'), 'threshold'), 'offset_from_master')):
                pass
                yield 'ptp monitor threshold offset-from-master '
                yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'monitor'), 'threshold'), 'offset_from_master'))
                yield '\n'
            if t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'monitor'), 'threshold'), 'mean_path_delay')):
                pass
                yield 'ptp monitor threshold mean-path-delay '
                yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'monitor'), 'threshold'), 'mean_path_delay'))
                yield '\n'
            if t_1(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'monitor'), 'threshold'), 'drop'), 'offset_from_master')):
                pass
                yield 'ptp monitor threshold offset-from-master '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'monitor'), 'threshold'), 'drop'), 'offset_from_master'))
                yield ' nanoseconds drop\n'
            if t_1(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'monitor'), 'threshold'), 'drop'), 'mean_path_delay')):
                pass
                yield 'ptp monitor threshold mean-path-delay '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'monitor'), 'threshold'), 'drop'), 'mean_path_delay'))
                yield ' nanoseconds drop\n'
            if t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'monitor'), 'missing_message'), 'intervals')):
                pass
                if t_1(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'monitor'), 'missing_message'), 'intervals'), 'announce')):
                    pass
                    yield 'ptp monitor threshold missing-message announce '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'monitor'), 'missing_message'), 'intervals'), 'announce'))
                    yield ' intervals\n'
                if t_1(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'monitor'), 'missing_message'), 'intervals'), 'follow_up')):
                    pass
                    yield 'ptp monitor threshold missing-message follow-up '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'monitor'), 'missing_message'), 'intervals'), 'follow_up'))
                    yield ' intervals\n'
                if t_1(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'monitor'), 'missing_message'), 'intervals'), 'sync')):
                    pass
                    yield 'ptp monitor threshold missing-message sync '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'monitor'), 'missing_message'), 'intervals'), 'sync'))
                    yield ' intervals\n'
            if t_1(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'monitor'), 'missing_message'), 'sequence_ids'), 'enabled'), False):
                pass
                yield 'no ptp monitor sequence-id\n'
            elif t_1(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'monitor'), 'missing_message'), 'sequence_ids'), 'enabled'), True):
                pass
                yield 'ptp monitor sequence-id\n'
                if t_1(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'monitor'), 'missing_message'), 'sequence_ids'), 'announce')):
                    pass
                    yield 'ptp monitor threshold missing-message announce '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'monitor'), 'missing_message'), 'sequence_ids'), 'announce'))
                    yield ' sequence-ids\n'
                if t_1(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'monitor'), 'missing_message'), 'sequence_ids'), 'delay_resp')):
                    pass
                    yield 'ptp monitor threshold missing-message delay-resp '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'monitor'), 'missing_message'), 'sequence_ids'), 'delay_resp'))
                    yield ' sequence-ids\n'
                if t_1(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'monitor'), 'missing_message'), 'sequence_ids'), 'follow_up')):
                    pass
                    yield 'ptp monitor threshold missing-message follow-up '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'monitor'), 'missing_message'), 'sequence_ids'), 'follow_up'))
                    yield ' sequence-ids\n'
                if t_1(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'monitor'), 'missing_message'), 'sequence_ids'), 'sync')):
                    pass
                    yield 'ptp monitor threshold missing-message sync '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='ptp') if l_0_ptp is missing else l_0_ptp), 'monitor'), 'missing_message'), 'sequence_ids'), 'sync'))
                    yield ' sequence-ids\n'

blocks = {}
debug_info = '2=18&4=21&5=24&7=26&8=29&10=31&11=34&13=36&14=39&16=41&17=44&19=46&20=49&22=51&23=54&25=56&26=59&28=61&29=64&31=66&34=69&36=72&37=74&38=77&40=79&41=82&43=84&44=87&46=89&47=92&49=94&50=96&51=99&53=101&54=104&56=106&57=109&60=111&62=114&64=117&65=120&67=122&68=125&70=127&71=130&73=132&74=135'