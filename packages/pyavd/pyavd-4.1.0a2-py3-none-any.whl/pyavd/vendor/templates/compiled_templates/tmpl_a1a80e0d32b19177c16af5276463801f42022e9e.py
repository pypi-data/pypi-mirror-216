from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'documentation/errdisable.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_errdisable = resolve('errdisable')
    try:
        t_1 = environment.filters['arista.avd.natural_sort']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.natural_sort' found.")
    try:
        t_2 = environment.tests['defined']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No test named 'defined' found.")
    try:
        t_3 = environment.tests['none']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No test named 'none' found.")
    pass
    if (t_2((undefined(name='errdisable') if l_0_errdisable is missing else l_0_errdisable)) and (not t_3((undefined(name='errdisable') if l_0_errdisable is missing else l_0_errdisable)))):
        pass
        yield '\n## Errdisable\n\n'
        if t_2(environment.getattr((undefined(name='errdisable') if l_0_errdisable is missing else l_0_errdisable), 'recovery')):
            pass
            if t_2(environment.getattr(environment.getattr((undefined(name='errdisable') if l_0_errdisable is missing else l_0_errdisable), 'detect'), 'causes')):
                pass
                yield '|  Detect Cause | Enabled |\n| ------------- | ------- |\n'
                for l_1_cause in t_1(environment.getattr(environment.getattr((undefined(name='errdisable') if l_0_errdisable is missing else l_0_errdisable), 'detect'), 'causes')):
                    _loop_vars = {}
                    pass
                    if (l_1_cause == 'acl'):
                        pass
                        yield '| '
                        yield str(l_1_cause)
                        yield ' | True |\n'
                    elif (l_1_cause == 'arp-inspection'):
                        pass
                        yield '| '
                        yield str(l_1_cause)
                        yield ' | True |\n'
                    elif (l_1_cause == 'dot1x'):
                        pass
                        yield '| '
                        yield str(l_1_cause)
                        yield ' | True |\n'
                    elif (l_1_cause == 'link-change'):
                        pass
                        yield '| '
                        yield str(l_1_cause)
                        yield ' | True |\n'
                    elif (l_1_cause == 'tapagg'):
                        pass
                        yield '| '
                        yield str(l_1_cause)
                        yield ' | True |\n'
                    elif (l_1_cause == 'xcvr-misconfigured'):
                        pass
                        yield '| '
                        yield str(l_1_cause)
                        yield ' | True |\n'
                    elif (l_1_cause == 'xcvr-overheat'):
                        pass
                        yield '| '
                        yield str(l_1_cause)
                        yield ' | True |\n'
                    elif (l_1_cause == 'xcvr-power-unsupported'):
                        pass
                        yield '| '
                        yield str(l_1_cause)
                        yield ' | True |\n'
                l_1_cause = missing
            yield '\n'
            if (t_2(environment.getattr(environment.getattr((undefined(name='errdisable') if l_0_errdisable is missing else l_0_errdisable), 'recovery'), 'interval')) and (not t_3(environment.getattr(environment.getattr((undefined(name='errdisable') if l_0_errdisable is missing else l_0_errdisable), 'recovery'), 'interval')))):
                pass
            if t_2(environment.getattr(environment.getattr((undefined(name='errdisable') if l_0_errdisable is missing else l_0_errdisable), 'recovery'), 'causes')):
                pass
                yield '|  Detect Cause | Enabled | Interval |\n| ------------- | ------- | -------- |\n'
                for l_1_cause in t_1(environment.getattr(environment.getattr((undefined(name='errdisable') if l_0_errdisable is missing else l_0_errdisable), 'recovery'), 'causes')):
                    _loop_vars = {}
                    pass
                    if (l_1_cause == 'arp-inspection'):
                        pass
                        yield '| '
                        yield str(l_1_cause)
                        yield ' | True | '
                        yield str(environment.getattr(environment.getattr((undefined(name='errdisable') if l_0_errdisable is missing else l_0_errdisable), 'recovery'), 'interval'))
                        yield ' |\n'
                    elif (l_1_cause == 'bpduguard'):
                        pass
                        yield '| '
                        yield str(l_1_cause)
                        yield ' | True | '
                        yield str(environment.getattr(environment.getattr((undefined(name='errdisable') if l_0_errdisable is missing else l_0_errdisable), 'recovery'), 'interval'))
                        yield ' |\n'
                    elif (l_1_cause == 'dot1x'):
                        pass
                        yield '| '
                        yield str(l_1_cause)
                        yield ' | True | '
                        yield str(environment.getattr(environment.getattr((undefined(name='errdisable') if l_0_errdisable is missing else l_0_errdisable), 'recovery'), 'interval'))
                        yield ' |\n'
                    elif (l_1_cause == 'hitless-reload-down'):
                        pass
                        yield '| '
                        yield str(l_1_cause)
                        yield ' | True | '
                        yield str(environment.getattr(environment.getattr((undefined(name='errdisable') if l_0_errdisable is missing else l_0_errdisable), 'recovery'), 'interval'))
                        yield ' |\n'
                    elif (l_1_cause == 'lacp-rate-limit'):
                        pass
                        yield '| '
                        yield str(l_1_cause)
                        yield ' | True | '
                        yield str(environment.getattr(environment.getattr((undefined(name='errdisable') if l_0_errdisable is missing else l_0_errdisable), 'recovery'), 'interval'))
                        yield ' |\n'
                    elif (l_1_cause == 'link-flap'):
                        pass
                        yield '| '
                        yield str(l_1_cause)
                        yield ' | True | '
                        yield str(environment.getattr(environment.getattr((undefined(name='errdisable') if l_0_errdisable is missing else l_0_errdisable), 'recovery'), 'interval'))
                        yield ' |\n'
                    elif (l_1_cause == 'no-internal-vlan'):
                        pass
                        yield '| '
                        yield str(l_1_cause)
                        yield ' | True | '
                        yield str(environment.getattr(environment.getattr((undefined(name='errdisable') if l_0_errdisable is missing else l_0_errdisable), 'recovery'), 'interval'))
                        yield ' |\n'
                    elif (l_1_cause == 'portchannelguard'):
                        pass
                        yield '| '
                        yield str(l_1_cause)
                        yield ' | True | '
                        yield str(environment.getattr(environment.getattr((undefined(name='errdisable') if l_0_errdisable is missing else l_0_errdisable), 'recovery'), 'interval'))
                        yield ' |\n'
                    elif (l_1_cause == 'portsec'):
                        pass
                        yield '| '
                        yield str(l_1_cause)
                        yield ' | True | '
                        yield str(environment.getattr(environment.getattr((undefined(name='errdisable') if l_0_errdisable is missing else l_0_errdisable), 'recovery'), 'interval'))
                        yield ' |\n'
                    elif (l_1_cause == 'speed-misconfigured'):
                        pass
                        yield '| '
                        yield str(l_1_cause)
                        yield ' | True | '
                        yield str(environment.getattr(environment.getattr((undefined(name='errdisable') if l_0_errdisable is missing else l_0_errdisable), 'recovery'), 'interval'))
                        yield ' |\n'
                    elif (l_1_cause == 'tapagg'):
                        pass
                        yield '| '
                        yield str(l_1_cause)
                        yield ' | True | '
                        yield str(environment.getattr(environment.getattr((undefined(name='errdisable') if l_0_errdisable is missing else l_0_errdisable), 'recovery'), 'interval'))
                        yield ' |\n'
                    elif (l_1_cause == 'uplink-failure-detection'):
                        pass
                        yield '| '
                        yield str(l_1_cause)
                        yield ' | True | '
                        yield str(environment.getattr(environment.getattr((undefined(name='errdisable') if l_0_errdisable is missing else l_0_errdisable), 'recovery'), 'interval'))
                        yield ' |\n'
                    elif (l_1_cause == 'xcvr-misconfigured'):
                        pass
                        yield '| '
                        yield str(l_1_cause)
                        yield ' | True | '
                        yield str(environment.getattr(environment.getattr((undefined(name='errdisable') if l_0_errdisable is missing else l_0_errdisable), 'recovery'), 'interval'))
                        yield ' |\n'
                    elif (l_1_cause == 'xcvr-overheat'):
                        pass
                        yield '| '
                        yield str(l_1_cause)
                        yield ' | True | '
                        yield str(environment.getattr(environment.getattr((undefined(name='errdisable') if l_0_errdisable is missing else l_0_errdisable), 'recovery'), 'interval'))
                        yield ' |\n'
                    elif (l_1_cause == 'xcvr-power-unsupported'):
                        pass
                        yield '| '
                        yield str(l_1_cause)
                        yield ' | True | '
                        yield str(environment.getattr(environment.getattr((undefined(name='errdisable') if l_0_errdisable is missing else l_0_errdisable), 'recovery'), 'interval'))
                        yield ' |\n'
                    elif (l_1_cause == 'xcvr-unsupported'):
                        pass
                        yield '| '
                        yield str(l_1_cause)
                        yield ' | True | '
                        yield str(environment.getattr(environment.getattr((undefined(name='errdisable') if l_0_errdisable is missing else l_0_errdisable), 'recovery'), 'interval'))
                        yield ' |\n'
                l_1_cause = missing
        yield '\n```eos\n'
        template = environment.get_template('eos/errdisable.j2', 'documentation/errdisable.j2')
        for event in template.root_render_func(template.new_context(context.get_all(), True, {})):
            yield event
        yield '```\n'

blocks = {}
debug_info = '2=30&6=33&7=35&10=38&11=41&12=44&13=46&14=49&15=51&16=54&17=56&18=59&19=61&20=64&21=66&22=69&23=71&24=74&25=76&26=79&31=83&33=85&36=88&37=91&38=94&39=98&40=101&41=105&42=108&43=112&44=115&45=119&46=122&47=126&48=129&49=133&50=136&51=140&52=143&53=147&54=150&55=154&56=157&57=161&58=164&59=168&60=171&61=175&62=178&63=182&64=185&65=189&66=192&67=196&68=199&75=205'