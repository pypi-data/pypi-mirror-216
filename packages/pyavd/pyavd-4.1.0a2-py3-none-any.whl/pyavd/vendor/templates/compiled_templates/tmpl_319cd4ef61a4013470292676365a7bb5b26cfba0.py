from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/qos-profiles.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_qos_profiles = resolve('qos_profiles')
    try:
        t_1 = environment.filters['arista.avd.default']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.default' found.")
    try:
        t_2 = environment.filters['arista.avd.natural_sort']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.natural_sort' found.")
    try:
        t_3 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    for l_1_profile in t_2((undefined(name='qos_profiles') if l_0_qos_profiles is missing else l_0_qos_profiles), 'name'):
        _loop_vars = {}
        pass
        yield '!\nqos profile '
        yield str(environment.getattr(l_1_profile, 'name'))
        yield '\n'
        if t_3(environment.getattr(l_1_profile, 'trust')):
            pass
            if (environment.getattr(l_1_profile, 'trust') == 'disabled'):
                pass
                yield '   no qos trust\n'
            else:
                pass
                yield '   qos trust '
                yield str(environment.getattr(l_1_profile, 'trust'))
                yield '\n'
        if t_3(environment.getattr(l_1_profile, 'cos')):
            pass
            yield '   qos cos '
            yield str(environment.getattr(l_1_profile, 'cos'))
            yield '\n'
        if t_3(environment.getattr(l_1_profile, 'dscp')):
            pass
            yield '   qos dscp '
            yield str(environment.getattr(l_1_profile, 'dscp'))
            yield '\n'
        if t_3(environment.getattr(environment.getattr(l_1_profile, 'shape'), 'rate')):
            pass
            yield '   shape rate '
            yield str(environment.getattr(environment.getattr(l_1_profile, 'shape'), 'rate'))
            yield '\n'
        if t_3(environment.getattr(environment.getattr(environment.getattr(l_1_profile, 'service_policy'), 'type'), 'qos_input')):
            pass
            yield '   service-policy type qos input '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_profile, 'service_policy'), 'type'), 'qos_input'))
            yield '\n'
        for l_2_tx_queue in t_2(environment.getattr(l_1_profile, 'tx_queues'), 'id'):
            _loop_vars = {}
            pass
            yield '   !\n   tx-queue '
            yield str(environment.getattr(l_2_tx_queue, 'id'))
            yield '\n'
            if t_3(environment.getattr(l_2_tx_queue, 'comment')):
                pass
                for l_3_comment_line in t_1(context.call(environment.getattr(environment.getattr(l_2_tx_queue, 'comment'), 'splitlines'), _loop_vars=_loop_vars), []):
                    _loop_vars = {}
                    pass
                    yield '      !! '
                    yield str(l_3_comment_line)
                    yield '\n'
                l_3_comment_line = missing
            if t_3(environment.getattr(l_2_tx_queue, 'bandwidth_percent')):
                pass
                yield '      bandwidth percent '
                yield str(environment.getattr(l_2_tx_queue, 'bandwidth_percent'))
                yield '\n'
            elif t_3(environment.getattr(l_2_tx_queue, 'bandwidth_guaranteed_percent')):
                pass
                yield '      bandwidth guaranteed percent '
                yield str(environment.getattr(l_2_tx_queue, 'bandwidth_guaranteed_percent'))
                yield '\n'
            if t_3(environment.getattr(l_2_tx_queue, 'priority')):
                pass
                yield '      '
                yield str(environment.getattr(l_2_tx_queue, 'priority'))
                yield '\n'
            if t_3(environment.getattr(environment.getattr(l_2_tx_queue, 'shape'), 'rate')):
                pass
                yield '      shape rate '
                yield str(environment.getattr(environment.getattr(l_2_tx_queue, 'shape'), 'rate'))
                yield '\n'
        l_2_tx_queue = missing
        for l_2_uc_tx_queue in t_2(environment.getattr(l_1_profile, 'uc_tx_queues'), 'id'):
            _loop_vars = {}
            pass
            yield '   !\n   uc-tx-queue '
            yield str(environment.getattr(l_2_uc_tx_queue, 'id'))
            yield '\n'
            if t_3(environment.getattr(l_2_uc_tx_queue, 'comment')):
                pass
                for l_3_comment_line in t_1(context.call(environment.getattr(environment.getattr(l_2_uc_tx_queue, 'comment'), 'splitlines'), _loop_vars=_loop_vars), []):
                    _loop_vars = {}
                    pass
                    yield '      !! '
                    yield str(l_3_comment_line)
                    yield '\n'
                l_3_comment_line = missing
            if t_3(environment.getattr(l_2_uc_tx_queue, 'bandwidth_percent')):
                pass
                yield '      bandwidth percent '
                yield str(environment.getattr(l_2_uc_tx_queue, 'bandwidth_percent'))
                yield '\n'
            elif t_3(environment.getattr(l_2_uc_tx_queue, 'bandwidth_guaranteed_percent')):
                pass
                yield '      bandwidth guaranteed percent '
                yield str(environment.getattr(l_2_uc_tx_queue, 'bandwidth_guaranteed_percent'))
                yield '\n'
            if t_3(environment.getattr(l_2_uc_tx_queue, 'priority')):
                pass
                yield '      '
                yield str(environment.getattr(l_2_uc_tx_queue, 'priority'))
                yield '\n'
            if t_3(environment.getattr(environment.getattr(l_2_uc_tx_queue, 'shape'), 'rate')):
                pass
                yield '      shape rate '
                yield str(environment.getattr(environment.getattr(l_2_uc_tx_queue, 'shape'), 'rate'))
                yield '\n'
        l_2_uc_tx_queue = missing
        for l_2_mc_tx_queue in t_2(environment.getattr(l_1_profile, 'mc_tx_queues'), 'id'):
            _loop_vars = {}
            pass
            yield '   !\n   mc-tx-queue '
            yield str(environment.getattr(l_2_mc_tx_queue, 'id'))
            yield '\n'
            if t_3(environment.getattr(l_2_mc_tx_queue, 'comment')):
                pass
                for l_3_comment_line in t_1(context.call(environment.getattr(environment.getattr(l_2_mc_tx_queue, 'comment'), 'splitlines'), _loop_vars=_loop_vars), []):
                    _loop_vars = {}
                    pass
                    yield '      !! '
                    yield str(l_3_comment_line)
                    yield '\n'
                l_3_comment_line = missing
            if t_3(environment.getattr(l_2_mc_tx_queue, 'bandwidth_percent')):
                pass
                yield '      bandwidth percent '
                yield str(environment.getattr(l_2_mc_tx_queue, 'bandwidth_percent'))
                yield '\n'
            elif t_3(environment.getattr(l_2_mc_tx_queue, 'bandwidth_guaranteed_percent')):
                pass
                yield '      bandwidth guaranteed percent '
                yield str(environment.getattr(l_2_mc_tx_queue, 'bandwidth_guaranteed_percent'))
                yield '\n'
            if t_3(environment.getattr(l_2_mc_tx_queue, 'priority')):
                pass
                yield '      '
                yield str(environment.getattr(l_2_mc_tx_queue, 'priority'))
                yield '\n'
            if t_3(environment.getattr(environment.getattr(l_2_mc_tx_queue, 'shape'), 'rate')):
                pass
                yield '      shape rate '
                yield str(environment.getattr(environment.getattr(l_2_mc_tx_queue, 'shape'), 'rate'))
                yield '\n'
        l_2_mc_tx_queue = missing
    l_1_profile = missing

blocks = {}
debug_info = '2=30&4=34&5=36&6=38&9=44&12=46&13=49&15=51&16=54&18=56&19=59&21=61&22=64&24=66&26=70&27=72&28=74&29=78&32=81&33=84&34=86&35=89&37=91&38=94&40=96&41=99&44=102&46=106&47=108&48=110&49=114&52=117&53=120&54=122&55=125&57=127&58=130&60=132&61=135&64=138&66=142&67=144&68=146&69=150&72=153&73=156&74=158&75=161&77=163&78=166&80=168&81=171'