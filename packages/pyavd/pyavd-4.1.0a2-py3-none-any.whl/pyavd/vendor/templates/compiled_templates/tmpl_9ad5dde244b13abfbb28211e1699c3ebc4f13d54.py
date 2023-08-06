from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'documentation/qos-profiles.j2'

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
        t_3 = environment.filters['replace']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No filter named 'replace' found.")
    try:
        t_4 = environment.filters['trim']
    except KeyError:
        @internalcode
        def t_4(*unused):
            raise TemplateRuntimeError("No filter named 'trim' found.")
    try:
        t_5 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_5(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_5((undefined(name='qos_profiles') if l_0_qos_profiles is missing else l_0_qos_profiles)):
        pass
        yield '\n### QOS Profiles\n\n#### QOS Profiles Summary\n\n'
        for l_1_profile in t_2((undefined(name='qos_profiles') if l_0_qos_profiles is missing else l_0_qos_profiles), 'name'):
            l_1_cos = l_1_dscp = l_1_trust = l_1_shape_rate = l_1_qos_sp = missing
            _loop_vars = {}
            pass
            yield '\nQOS Profile: **'
            yield str(environment.getattr(l_1_profile, 'name'))
            yield '**\n\n**Settings**\n\n| Default COS | Default DSCP | Trust | Shape Rate | QOS Service Policy |\n| ----------- | ------------ | ----- | ---------- | ------------------ |\n'
            l_1_cos = t_1(environment.getattr(l_1_profile, 'cos'), '-')
            _loop_vars['cos'] = l_1_cos
            l_1_dscp = t_1(environment.getattr(l_1_profile, 'dscp'), '-')
            _loop_vars['dscp'] = l_1_dscp
            l_1_trust = t_1(environment.getattr(l_1_profile, 'trust'), '-')
            _loop_vars['trust'] = l_1_trust
            l_1_shape_rate = t_1(environment.getattr(environment.getattr(l_1_profile, 'shape'), 'rate'), '-')
            _loop_vars['shape_rate'] = l_1_shape_rate
            l_1_qos_sp = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_profile, 'service_policy'), 'type'), 'qos_input'), '-')
            _loop_vars['qos_sp'] = l_1_qos_sp
            yield '| '
            yield str((undefined(name='cos') if l_1_cos is missing else l_1_cos))
            yield ' | '
            yield str((undefined(name='dscp') if l_1_dscp is missing else l_1_dscp))
            yield ' | '
            yield str((undefined(name='trust') if l_1_trust is missing else l_1_trust))
            yield ' | '
            yield str((undefined(name='shape_rate') if l_1_shape_rate is missing else l_1_shape_rate))
            yield ' | '
            yield str((undefined(name='qos_sp') if l_1_qos_sp is missing else l_1_qos_sp))
            yield ' |\n'
            if ((t_5(environment.getattr(l_1_profile, 'tx_queues')) or t_5(environment.getattr(l_1_profile, 'uc_tx_queues'))) or t_5(environment.getattr(l_1_profile, 'mc_tx_queues'))):
                pass
                yield '\n**TX Queues**\n\n| TX queue | Type | Bandwidth | Priority | Shape Rate | Comment |\n| -------- | ---- | --------- | -------- | ---------- | ------- |\n'
                if t_5(environment.getattr(l_1_profile, 'tx_queues')):
                    pass
                    for l_2_tx_queue in t_2(environment.getattr(l_1_profile, 'tx_queues'), 'id'):
                        l_2_shape_rate = l_1_shape_rate
                        l_2_type = l_2_bw_percent = l_2_priority = l_2_comment = missing
                        _loop_vars = {}
                        pass
                        l_2_type = 'All'
                        _loop_vars['type'] = l_2_type
                        l_2_bw_percent = t_1(environment.getattr(l_2_tx_queue, 'bandwidth_percent'), environment.getattr(l_2_tx_queue, 'bandwidth_guaranteed_percent'), '-')
                        _loop_vars['bw_percent'] = l_2_bw_percent
                        l_2_priority = t_1(environment.getattr(l_2_tx_queue, 'priority'), '-')
                        _loop_vars['priority'] = l_2_priority
                        l_2_shape_rate = t_1(environment.getattr(environment.getattr(l_2_tx_queue, 'shape'), 'rate'), '-')
                        _loop_vars['shape_rate'] = l_2_shape_rate
                        l_2_comment = t_3(context.eval_ctx, t_4(t_1(environment.getattr(l_2_tx_queue, 'comment'), '-')), '\n', '<br>')
                        _loop_vars['comment'] = l_2_comment
                        yield '| '
                        yield str(environment.getattr(l_2_tx_queue, 'id'))
                        yield ' | '
                        yield str((undefined(name='type') if l_2_type is missing else l_2_type))
                        yield ' | '
                        yield str((undefined(name='bw_percent') if l_2_bw_percent is missing else l_2_bw_percent))
                        yield ' | '
                        yield str((undefined(name='priority') if l_2_priority is missing else l_2_priority))
                        yield ' | '
                        yield str((undefined(name='shape_rate') if l_2_shape_rate is missing else l_2_shape_rate))
                        yield ' | '
                        yield str((undefined(name='comment') if l_2_comment is missing else l_2_comment))
                        yield ' |\n'
                    l_2_tx_queue = l_2_type = l_2_bw_percent = l_2_priority = l_2_shape_rate = l_2_comment = missing
                if t_5(environment.getattr(l_1_profile, 'uc_tx_queues')):
                    pass
                    for l_2_uc_tx_queue in t_2(environment.getattr(l_1_profile, 'uc_tx_queues'), 'id'):
                        l_2_shape_rate = l_1_shape_rate
                        l_2_type = l_2_bw_percent = l_2_priority = l_2_comment = missing
                        _loop_vars = {}
                        pass
                        l_2_type = 'Unicast'
                        _loop_vars['type'] = l_2_type
                        l_2_bw_percent = t_1(environment.getattr(l_2_uc_tx_queue, 'bandwidth_percent'), environment.getattr(l_2_uc_tx_queue, 'bandwidth_guaranteed_percent'), '-')
                        _loop_vars['bw_percent'] = l_2_bw_percent
                        l_2_priority = t_1(environment.getattr(l_2_uc_tx_queue, 'priority'), '-')
                        _loop_vars['priority'] = l_2_priority
                        l_2_shape_rate = t_1(environment.getattr(environment.getattr(l_2_uc_tx_queue, 'shape'), 'rate'), '-')
                        _loop_vars['shape_rate'] = l_2_shape_rate
                        l_2_comment = t_3(context.eval_ctx, t_4(t_1(environment.getattr(l_2_uc_tx_queue, 'comment'), '-')), '\n', '<br>')
                        _loop_vars['comment'] = l_2_comment
                        yield '| '
                        yield str(environment.getattr(l_2_uc_tx_queue, 'id'))
                        yield ' | '
                        yield str((undefined(name='type') if l_2_type is missing else l_2_type))
                        yield ' | '
                        yield str((undefined(name='bw_percent') if l_2_bw_percent is missing else l_2_bw_percent))
                        yield ' | '
                        yield str((undefined(name='priority') if l_2_priority is missing else l_2_priority))
                        yield ' | '
                        yield str((undefined(name='shape_rate') if l_2_shape_rate is missing else l_2_shape_rate))
                        yield ' | '
                        yield str((undefined(name='comment') if l_2_comment is missing else l_2_comment))
                        yield ' |\n'
                    l_2_uc_tx_queue = l_2_type = l_2_bw_percent = l_2_priority = l_2_shape_rate = l_2_comment = missing
                if t_5(environment.getattr(l_1_profile, 'mc_tx_queues')):
                    pass
                    for l_2_mc_tx_queue in t_2(environment.getattr(l_1_profile, 'mc_tx_queues'), 'id'):
                        l_2_shape_rate = l_1_shape_rate
                        l_2_type = l_2_bw_percent = l_2_priority = l_2_comment = missing
                        _loop_vars = {}
                        pass
                        l_2_type = 'Multicast'
                        _loop_vars['type'] = l_2_type
                        l_2_bw_percent = t_1(environment.getattr(l_2_mc_tx_queue, 'bandwidth_percent'), environment.getattr(l_2_mc_tx_queue, 'bandwidth_guaranteed_percent'), '-')
                        _loop_vars['bw_percent'] = l_2_bw_percent
                        l_2_priority = t_1(environment.getattr(l_2_mc_tx_queue, 'priority'), '-')
                        _loop_vars['priority'] = l_2_priority
                        l_2_shape_rate = t_1(environment.getattr(environment.getattr(l_2_mc_tx_queue, 'shape'), 'rate'), '-')
                        _loop_vars['shape_rate'] = l_2_shape_rate
                        l_2_comment = t_3(context.eval_ctx, t_4(t_1(environment.getattr(l_2_mc_tx_queue, 'comment'), '-')), '\n', '<br>')
                        _loop_vars['comment'] = l_2_comment
                        yield '| '
                        yield str(environment.getattr(l_2_mc_tx_queue, 'id'))
                        yield ' | '
                        yield str((undefined(name='type') if l_2_type is missing else l_2_type))
                        yield ' | '
                        yield str((undefined(name='bw_percent') if l_2_bw_percent is missing else l_2_bw_percent))
                        yield ' | '
                        yield str((undefined(name='priority') if l_2_priority is missing else l_2_priority))
                        yield ' | '
                        yield str((undefined(name='shape_rate') if l_2_shape_rate is missing else l_2_shape_rate))
                        yield ' | '
                        yield str((undefined(name='comment') if l_2_comment is missing else l_2_comment))
                        yield ' |\n'
                    l_2_mc_tx_queue = l_2_type = l_2_bw_percent = l_2_priority = l_2_shape_rate = l_2_comment = missing
        l_1_profile = l_1_cos = l_1_dscp = l_1_trust = l_1_shape_rate = l_1_qos_sp = missing
        yield '\n#### QOS Profile Device Configuration\n\n```eos\n'
        template = environment.get_template('eos/qos-profiles.j2', 'documentation/qos-profiles.j2')
        for event in template.root_render_func(template.new_context(context.get_all(), True, {})):
            yield event
        yield '```\n'

blocks = {}
debug_info = '2=42&8=45&10=50&16=52&17=54&18=56&19=58&20=60&21=63&22=73&30=76&31=78&32=83&33=85&36=87&37=89&38=91&39=94&42=107&43=109&44=114&45=116&48=118&49=120&50=122&51=125&54=138&55=140&56=145&57=147&60=149&61=151&62=153&63=156&72=171'