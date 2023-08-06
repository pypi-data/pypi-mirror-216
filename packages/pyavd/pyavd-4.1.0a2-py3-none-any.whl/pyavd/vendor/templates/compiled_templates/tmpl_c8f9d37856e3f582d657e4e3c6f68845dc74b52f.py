from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/maintenance.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_maintenance = resolve('maintenance')
    l_0_first_line = missing
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
    l_0_first_line = {'flag': True}
    context.vars['first_line'] = l_0_first_line
    context.exported_vars.add('first_line')
    if t_2((undefined(name='maintenance') if l_0_maintenance is missing else l_0_maintenance)):
        pass
        yield '!\nmaintenance\n'
        l_1_loop = missing
        for l_1_bgp_profile, l_1_loop in LoopContext(t_1(environment.getattr((undefined(name='maintenance') if l_0_maintenance is missing else l_0_maintenance), 'bgp_profiles'), 'name'), undefined):
            l_1_first_line = l_0_first_line
            _loop_vars = {}
            pass
            if (environment.getattr(l_1_loop, 'index0') > 0):
                pass
                yield '   !\n'
            l_1_first_line = {'flag': False}
            _loop_vars['first_line'] = l_1_first_line
            yield '   profile bgp '
            yield str(environment.getattr(l_1_bgp_profile, 'name'))
            yield '\n'
            if t_2(environment.getattr(environment.getattr(l_1_bgp_profile, 'initiator'), 'route_map_inout')):
                pass
                yield '      initiator route-map '
                yield str(environment.getattr(environment.getattr(l_1_bgp_profile, 'initiator'), 'route_map_inout'))
                yield ' inout\n'
        l_1_loop = l_1_bgp_profile = l_1_first_line = missing
        if t_2(environment.getattr((undefined(name='maintenance') if l_0_maintenance is missing else l_0_maintenance), 'default_bgp_profile')):
            pass
            l_0_first_line = {'flag': False}
            context.vars['first_line'] = l_0_first_line
            context.exported_vars.add('first_line')
            yield '   profile bgp '
            yield str(environment.getattr((undefined(name='maintenance') if l_0_maintenance is missing else l_0_maintenance), 'default_bgp_profile'))
            yield ' default\n'
        if t_2(environment.getattr((undefined(name='maintenance') if l_0_maintenance is missing else l_0_maintenance), 'default_interface_profile')):
            pass
            l_0_first_line = {'flag': False}
            context.vars['first_line'] = l_0_first_line
            context.exported_vars.add('first_line')
            yield '   profile interface '
            yield str(environment.getattr((undefined(name='maintenance') if l_0_maintenance is missing else l_0_maintenance), 'default_interface_profile'))
            yield ' default\n'
        if t_2(environment.getattr((undefined(name='maintenance') if l_0_maintenance is missing else l_0_maintenance), 'default_unit_profile')):
            pass
            l_0_first_line = {'flag': False}
            context.vars['first_line'] = l_0_first_line
            context.exported_vars.add('first_line')
            yield '   profile unit '
            yield str(environment.getattr((undefined(name='maintenance') if l_0_maintenance is missing else l_0_maintenance), 'default_unit_profile'))
            yield ' default\n'
        for l_1_interface_profile in t_1(environment.getattr((undefined(name='maintenance') if l_0_maintenance is missing else l_0_maintenance), 'interface_profiles'), 'name'):
            l_1_first_line = l_0_first_line
            _loop_vars = {}
            pass
            if (not environment.getattr((undefined(name='first_line') if l_1_first_line is missing else l_1_first_line), 'flag')):
                pass
                yield '   !\n'
            l_1_first_line = {'flag': False}
            _loop_vars['first_line'] = l_1_first_line
            yield '   profile interface '
            yield str(environment.getattr(l_1_interface_profile, 'name'))
            yield '\n'
            if t_2(environment.getattr(environment.getattr(l_1_interface_profile, 'rate_monitoring'), 'load_interval')):
                pass
                yield '      rate-monitoring load-interval '
                yield str(environment.getattr(environment.getattr(l_1_interface_profile, 'rate_monitoring'), 'load_interval'))
                yield '\n'
            if t_2(environment.getattr(environment.getattr(l_1_interface_profile, 'rate_monitoring'), 'threshold')):
                pass
                yield '      rate-monitoring threshold '
                yield str(environment.getattr(environment.getattr(l_1_interface_profile, 'rate_monitoring'), 'threshold'))
                yield '\n'
            if t_2(environment.getattr(environment.getattr(l_1_interface_profile, 'shutdown'), 'max_delay')):
                pass
                yield '      shutdown max-delay '
                yield str(environment.getattr(environment.getattr(l_1_interface_profile, 'shutdown'), 'max_delay'))
                yield '\n'
        l_1_interface_profile = l_1_first_line = missing
        for l_1_unit_profile in t_1(environment.getattr((undefined(name='maintenance') if l_0_maintenance is missing else l_0_maintenance), 'unit_profiles'), 'name'):
            l_1_first_line = l_0_first_line
            _loop_vars = {}
            pass
            if (not environment.getattr((undefined(name='first_line') if l_1_first_line is missing else l_1_first_line), 'flag')):
                pass
                yield '   !\n'
            l_1_first_line = {'flag': False}
            _loop_vars['first_line'] = l_1_first_line
            yield '   profile unit '
            yield str(environment.getattr(l_1_unit_profile, 'name'))
            yield '\n'
            if t_2(environment.getattr(environment.getattr(l_1_unit_profile, 'on_boot'), 'duration')):
                pass
                yield '      on-boot duration '
                yield str(environment.getattr(environment.getattr(l_1_unit_profile, 'on_boot'), 'duration'))
                yield '\n'
        l_1_unit_profile = l_1_first_line = missing
        for l_1_unit in t_1(environment.getattr((undefined(name='maintenance') if l_0_maintenance is missing else l_0_maintenance), 'units'), 'name'):
            l_1_first_line = l_0_first_line
            _loop_vars = {}
            pass
            if (not environment.getattr((undefined(name='first_line') if l_1_first_line is missing else l_1_first_line), 'flag')):
                pass
                yield '   !\n'
            l_1_first_line = {'flag': False}
            _loop_vars['first_line'] = l_1_first_line
            yield '   unit '
            yield str(environment.getattr(l_1_unit, 'name'))
            yield '\n'
            for l_2_bgp_group in t_1(environment.getattr(environment.getattr(l_1_unit, 'groups'), 'bgp_groups')):
                _loop_vars = {}
                pass
                yield '      group bgp '
                yield str(l_2_bgp_group)
                yield '\n'
            l_2_bgp_group = missing
            for l_2_interface_group in t_1(environment.getattr(environment.getattr(l_1_unit, 'groups'), 'interface_groups')):
                _loop_vars = {}
                pass
                yield '      group interface '
                yield str(l_2_interface_group)
                yield '\n'
            l_2_interface_group = missing
            if t_2(environment.getattr(l_1_unit, 'profile')):
                pass
                yield '      profile unit '
                yield str(environment.getattr(l_1_unit, 'profile'))
                yield '\n'
            if t_2(environment.getattr(l_1_unit, 'quiesce'), True):
                pass
                yield '      quiesce\n'
            elif t_2(environment.getattr(l_1_unit, 'quiesce'), False):
                pass
                yield '      no quiesce\n'
        l_1_unit = l_1_first_line = missing

blocks = {}
debug_info = '2=25&3=28&6=32&7=36&10=39&11=42&12=44&13=47&16=50&17=52&18=56&20=58&21=60&22=64&24=66&25=68&26=72&28=74&29=78&32=81&33=84&34=86&35=89&37=91&38=94&40=96&41=99&44=102&45=106&48=109&49=112&50=114&51=117&54=120&55=124&58=127&59=130&60=132&61=136&63=139&64=143&66=146&67=149&69=151&71=154'