from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/hardware-counters.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_hardware_counters = resolve('hardware_counters')
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
    if t_2(environment.getattr((undefined(name='hardware_counters') if l_0_hardware_counters is missing else l_0_hardware_counters), 'features')):
        pass
        yield '!\n'
        for l_1_feature in t_1(environment.getattr((undefined(name='hardware_counters') if l_0_hardware_counters is missing else l_0_hardware_counters), 'features'), 'name'):
            l_1_hardware_counters_cli = missing
            _loop_vars = {}
            pass
            l_1_hardware_counters_cli = ''
            _loop_vars['hardware_counters_cli'] = l_1_hardware_counters_cli
            if t_2(environment.getattr(l_1_feature, 'name'), fail_action='error', var_name="The data model 'hardware_counters' changed in AVD4.0.0. 'hardware_counters.features.name'"):
                pass
                l_1_hardware_counters_cli = str_join(('hardware counter feature ', environment.getattr(l_1_feature, 'name'), ))
                _loop_vars['hardware_counters_cli'] = l_1_hardware_counters_cli
            if t_2(environment.getattr(l_1_feature, 'direction')):
                pass
                l_1_hardware_counters_cli = str_join(((undefined(name='hardware_counters_cli') if l_1_hardware_counters_cli is missing else l_1_hardware_counters_cli), ' ', environment.getattr(l_1_feature, 'direction'), ))
                _loop_vars['hardware_counters_cli'] = l_1_hardware_counters_cli
            if t_2(environment.getattr(l_1_feature, 'address_type')):
                pass
                l_1_hardware_counters_cli = str_join(((undefined(name='hardware_counters_cli') if l_1_hardware_counters_cli is missing else l_1_hardware_counters_cli), ' ', environment.getattr(l_1_feature, 'address_type'), ))
                _loop_vars['hardware_counters_cli'] = l_1_hardware_counters_cli
            if t_2(environment.getattr(l_1_feature, 'layer3'), True):
                pass
                l_1_hardware_counters_cli = str_join(((undefined(name='hardware_counters_cli') if l_1_hardware_counters_cli is missing else l_1_hardware_counters_cli), ' layer3', ))
                _loop_vars['hardware_counters_cli'] = l_1_hardware_counters_cli
            if t_2(environment.getattr(l_1_feature, 'vrf')):
                pass
                l_1_hardware_counters_cli = str_join(((undefined(name='hardware_counters_cli') if l_1_hardware_counters_cli is missing else l_1_hardware_counters_cli), ' vrf ', environment.getattr(l_1_feature, 'vrf'), ))
                _loop_vars['hardware_counters_cli'] = l_1_hardware_counters_cli
            if t_2(environment.getattr(l_1_feature, 'prefix')):
                pass
                l_1_hardware_counters_cli = str_join(((undefined(name='hardware_counters_cli') if l_1_hardware_counters_cli is missing else l_1_hardware_counters_cli), ' ', environment.getattr(l_1_feature, 'prefix'), ))
                _loop_vars['hardware_counters_cli'] = l_1_hardware_counters_cli
            if t_2(environment.getattr(l_1_feature, 'units_packets'), True):
                pass
                l_1_hardware_counters_cli = str_join(((undefined(name='hardware_counters_cli') if l_1_hardware_counters_cli is missing else l_1_hardware_counters_cli), ' units packets', ))
                _loop_vars['hardware_counters_cli'] = l_1_hardware_counters_cli
            yield str((undefined(name='hardware_counters_cli') if l_1_hardware_counters_cli is missing else l_1_hardware_counters_cli))
            yield '\n'
        l_1_feature = l_1_hardware_counters_cli = missing

blocks = {}
debug_info = '2=24&4=27&5=31&6=33&7=35&9=37&10=39&12=41&13=43&15=45&16=47&18=49&19=51&21=53&22=55&24=57&25=59&27=61'