from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos-intended-config.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_eos_cli_config_gen_configuration = resolve('eos_cli_config_gen_configuration')
    l_0_hide_passwords = missing
    try:
        t_1 = environment.filters['arista.avd.default']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.default' found.")
    pass
    l_0_hide_passwords = t_1(environment.getattr((undefined(name='eos_cli_config_gen_configuration') if l_0_eos_cli_config_gen_configuration is missing else l_0_eos_cli_config_gen_configuration), 'hide_passwords'), False)
    context.vars['hide_passwords'] = l_0_hide_passwords
    context.exported_vars.add('hide_passwords')
    template = environment.get_template('eos/rancid-content-type.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/boot.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/terminal.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/prompt.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/aliases.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/hardware-counters.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/service-routing-configuration-bgp.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/daemon-terminattr.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/daemons.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/dhcp-relay.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-dhcp-relay.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/switchport-default.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/vlan-internal-order.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-igmp-snooping.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/event-monitor.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/flow-trackings.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/load-interval.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/interface-defaults.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/interface-profiles.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/transceiver-qsfp-default-mode.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/errdisable.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/service-routing-protocols-model.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/queue-monitor-length.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/lldp.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/l2-protocol-forwarding.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/lacp.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/logging.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/mcs-client.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/match-list-input.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/as-path.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/mac-security.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-nat-part1.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/hostname.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-domain-lookup.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-name-servers.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/dns-domain.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/domain-list.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/trackers.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ntp.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/poe.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ptp.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/radius-servers.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/radius-server.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/router-l2-vpn.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/sflow.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/redundancy.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/qos-profiles.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/snmp-server.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/hardware.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/spanning-tree.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/platform.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/service-unsupported-transceiver.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/tacacs-servers.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/aaa.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/enable-password.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/aaa-root.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/local-users.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/roles.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/address-locking.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/tap-aggregation.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/clock.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/vlans.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/vrfs.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/link-tracking-groups.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/cvx.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/port-channel-interfaces.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ethernet-interfaces.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/loopback-interfaces.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/management-interfaces.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/tunnel-interfaces.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/vlan-interfaces.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/vxlan-interface.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/tcam-profile.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/monitor-connectivity.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/mac-address-table-aging-time.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-virtual-router-mac-address.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/virtual-source-nat-vrfs.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/event-handlers.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/bgp-groups.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/interface-groups.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ipv6-access-lists.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ipv6-standard-access-lists.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/access-lists.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-access-lists.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/standard-access-lists.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/mac-access-lists.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-routing.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-icmp-redirect.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-hardware.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-routing-vrfs.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ipv6-unicast-routing.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ipv6-unicast-routing-vrfs.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ipv6-icmp-redirect.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ipv6-hardware.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/monitor-sessions.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/qos.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/community-lists.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-community-lists.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-extcommunity-lists.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-extcommunity-lists-regexp.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/dynamic-prefix-lists.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/prefix-lists.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ipv6-prefix-lists.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/system.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/mac-address-table-notification.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/maintenance.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/mlag-configuration.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/static-routes.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ipv6-static-routes.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-nat-part2.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/class-maps.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/policy-maps-pbr.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/policy-maps-qos.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/arp.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/route-maps.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/router-bfd.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/peer-filters.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/router-bgp.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/router-igmp.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/router-multicast.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/router-general.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/router-traffic-engineering.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/router-ospf.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/router-pim-sparse-mode.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/router-isis.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/router-msdp.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/mpls.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/patch-panel.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/queue-monitor-streaming.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-tacacs-source-interfaces.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-radius-source-interfaces.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/vmtracer-sessions.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/traffic-policies.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/banners.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-http-client-source-interfaces.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-ssh-client-source-interfaces.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/management-api-http.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/management-console.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/management-cvx.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/management-defaults.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/management-api-gnmi.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/management-api-models.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/management-security.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/dot1x.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/management-ssh.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/management-tech-support.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/eos-cli.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/custom-templates.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/end.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event

blocks = {}
debug_info = '3=19&4=22&6=25&8=28&10=31&12=34&14=37&16=40&18=43&20=46&22=49&24=52&26=55&28=58&30=61&32=64&34=67&36=70&38=73&40=76&42=79&44=82&46=85&48=88&50=91&52=94&54=97&56=100&58=103&60=106&62=109&64=112&66=115&68=118&70=121&72=124&74=127&76=130&78=133&80=136&82=139&84=142&86=145&88=148&90=151&92=154&94=157&96=160&98=163&100=166&102=169&104=172&106=175&108=178&110=181&112=184&114=187&116=190&118=193&120=196&122=199&124=202&126=205&128=208&130=211&132=214&134=217&136=220&138=223&140=226&142=229&144=232&146=235&148=238&150=241&152=244&154=247&156=250&158=253&160=256&162=259&164=262&166=265&168=268&170=271&172=274&174=277&176=280&178=283&180=286&182=289&184=292&186=295&188=298&190=301&192=304&194=307&196=310&198=313&200=316&202=319&204=322&206=325&208=328&210=331&212=334&214=337&216=340&218=343&220=346&222=349&224=352&226=355&228=358&230=361&232=364&234=367&236=370&238=373&240=376&242=379&244=382&246=385&248=388&250=391&252=394&254=397&256=400&258=403&260=406&262=409&264=412&266=415&268=418&270=421&272=424&274=427&276=430&278=433&280=436&282=439&284=442&286=445&288=448&290=451&292=454&294=457&296=460&298=463&300=466'