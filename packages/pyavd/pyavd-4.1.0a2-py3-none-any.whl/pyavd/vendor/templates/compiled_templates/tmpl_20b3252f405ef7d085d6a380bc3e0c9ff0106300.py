from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'documentation/ip-nat.j2'

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
        t_2 = environment.filters['upper']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No filter named 'upper' found.")
    try:
        t_3 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_3((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat)):
        pass
        yield '\n## IP NAT\n'
        if t_3(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'kernel_buffer_size')):
            pass
            yield '\n| Setting | Value |\n| -------- | ----- |\n| Kernel Buffer Size | '
            yield str(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'kernel_buffer_size'))
            yield ' MB |\n'
        if t_3(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'pools')):
            pass
            yield '\n### NAT Pools\n'
            for l_1_pool in environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'pools'):
                _loop_vars = {}
                pass
                yield '\n#### Pool: '
                yield str(environment.getattr(l_1_pool, 'name'))
                yield '\n\n| Setting | Value |\n| -------- | ----- |\n| Pool Prefix Length | '
                yield str(environment.getattr(l_1_pool, 'prefix_length'))
                yield ' |\n'
                if t_3(environment.getattr(l_1_pool, 'utilization_log_threshold')):
                    pass
                    yield '| Pool Utilization Threshold | '
                    yield str(environment.getattr(l_1_pool, 'utilization_log_threshold'))
                    yield ' % (action: log) |\n'
                yield '\n##### Pool Ranges\n\n| First IP Address  | Last IP Address | First Port | Last Port |\n| ----------------- | --------------- | ---------- | --------- |\n'
                for l_2_range in t_1(environment.getattr(l_1_pool, 'ranges'), []):
                    _loop_vars = {}
                    pass
                    yield '| '
                    yield str(environment.getattr(l_2_range, 'first_ip'))
                    yield ' | '
                    yield str(environment.getattr(l_2_range, 'last_ip'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_2_range, 'first_port'), '-'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_2_range, 'last_port'), '-'))
                    yield ' |\n'
                l_2_range = missing
            l_1_pool = missing
        if t_3(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'synchronization')):
            pass
            yield '\n### NAT Synchronization\n\n| Setting | Value |\n| -------- | ----- |\n'
            if t_1(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'synchronization'), 'shutdown'), False):
                pass
                yield '| State | Disabled !\n'
            else:
                pass
                yield '| State | Enabled !\n'
            if t_3(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'synchronization'), 'expiry_interval')):
                pass
                yield '| Expiry Interval | '
                yield str(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'synchronization'), 'expiry_interval'))
                yield ' Seconds |\n'
            if t_3(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'synchronization'), 'local_interface')):
                pass
                yield '| Interface | '
                yield str(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'synchronization'), 'local_interface'))
                yield ' |\n'
            if t_3(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'synchronization'), 'peer_address')):
                pass
                yield '| Peer IP Address | '
                yield str(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'synchronization'), 'peer_address'))
                yield ' |\n'
            if (t_3(environment.getattr(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'synchronization'), 'port_range'), 'first_port')) and t_3(environment.getattr(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'synchronization'), 'port_range'), 'last_port'))):
                pass
                yield '| Port Range | '
                yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'synchronization'), 'port_range'), 'first_port'))
                yield ' - '
                yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'synchronization'), 'port_range'), 'last_port'))
                yield ' |\n'
            if t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'synchronization'), 'port_range'), 'split_disabled'), False):
                pass
                yield '| Port Range Split | Disabled |\n'
            else:
                pass
                yield '| Port Range Split | Enabled |\n'
        if t_3(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'translation')):
            pass
            yield '\n### NAT Translation Settings\n\n| Setting | Value |\n| -------- | ----- |\n'
            if t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'translation'), 'address_selection'), 'any'), False):
                pass
                yield '| Address Selection | Any |\n'
            if t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'translation'), 'address_selection'), 'hash_field_source_ip'), False):
                pass
                yield '| Address Selection | Hash Source IP Field |\n'
            if t_1(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'translation'), 'counters'), False):
                pass
                yield '| Counters | Enabled |\n'
            if t_3(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'translation'), 'max_entries')):
                pass
                if t_3(environment.getattr(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'translation'), 'max_entries'), 'limit')):
                    pass
                    yield '| Global Connection Limit | max. '
                    yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'translation'), 'max_entries'), 'limit'))
                    yield ' Connections |\n'
                if t_3(environment.getattr(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'translation'), 'max_entries'), 'host_limit')):
                    pass
                    yield '| per Host Connection Limit | max. '
                    yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'translation'), 'max_entries'), 'host_limit'))
                    yield ' Connections |\n'
                for l_1_ip_limit in t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'translation'), 'max_entries'), 'ip_limits'), []):
                    _loop_vars = {}
                    pass
                    yield '| IP Host '
                    yield str(environment.getattr(l_1_ip_limit, 'ip'))
                    yield ' Connection Limit | max. '
                    yield str(environment.getattr(l_1_ip_limit, 'limit'))
                    yield ' Connections |\n'
                l_1_ip_limit = missing
            if t_3(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'translation'), 'low_mark')):
                pass
                if t_3(environment.getattr(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'translation'), 'low_mark'), 'percentage')):
                    pass
                    yield '| Global Connection Limit Low Mark | '
                    yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'translation'), 'low_mark'), 'percentage'))
                    yield ' % |\n'
                if t_3(environment.getattr(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'translation'), 'low_mark'), 'host_percentage')):
                    pass
                    yield '| per Host Connection Limit Low Mark | '
                    yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'translation'), 'low_mark'), 'host_percentage'))
                    yield ' % |\n'
            for l_1_timeout in t_1(environment.getattr(environment.getattr((undefined(name='ip_nat') if l_0_ip_nat is missing else l_0_ip_nat), 'translation'), 'timeouts'), []):
                _loop_vars = {}
                pass
                yield '| '
                yield str(t_2(environment.getattr(l_1_timeout, 'protocol')))
                yield ' Connection Timeout | '
                yield str(environment.getattr(l_1_timeout, 'timeout'))
                yield ' Seconds |\n'
            l_1_timeout = missing
        yield '\n### IP NAT Device Configuration\n\n```eos\n'
        template = environment.get_template('eos/ip-nat-part1.j2', 'documentation/ip-nat.j2')
        for event in template.root_render_func(template.new_context(context.get_all(), True, {})):
            yield event
        template = environment.get_template('eos/ip-nat-part2.j2', 'documentation/ip-nat.j2')
        for event in template.root_render_func(template.new_context(context.get_all(), True, {})):
            yield event
        yield '```\n'

blocks = {}
debug_info = '2=30&5=33&9=36&11=38&14=41&16=45&20=47&21=49&22=52&29=55&30=59&34=69&40=72&45=78&46=81&48=83&49=86&51=88&52=91&54=93&56=96&58=100&64=106&70=109&73=112&76=115&79=118&80=120&81=123&83=125&84=128&86=130&87=134&90=139&91=141&92=144&94=146&95=149&98=151&99=155&106=161&107=164'