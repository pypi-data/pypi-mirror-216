from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/interface-ip-nat.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_interface_ip_nat = resolve('interface_ip_nat')
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
    for l_1_nat in t_2(t_1(environment.getattr(environment.getattr((undefined(name='interface_ip_nat') if l_0_interface_ip_nat is missing else l_0_interface_ip_nat), 'source'), 'static'), []), 'original_ip'):
        l_1_nat_cli = resolve('nat_cli')
        _loop_vars = {}
        pass
        if ((not (t_3(environment.getattr(l_1_nat, 'access_list')) and t_3(environment.getattr(l_1_nat, 'group')))) and (not ((not t_3(environment.getattr(l_1_nat, 'original_port'))) and t_3(environment.getattr(l_1_nat, 'translated_port'))))):
            pass
            l_1_nat_cli = 'ip nat source'
            _loop_vars['nat_cli'] = l_1_nat_cli
            if t_3(environment.getattr(l_1_nat, 'direction')):
                pass
                l_1_nat_cli = str_join(((undefined(name='nat_cli') if l_1_nat_cli is missing else l_1_nat_cli), ' ', environment.getattr(l_1_nat, 'direction'), ))
                _loop_vars['nat_cli'] = l_1_nat_cli
            l_1_nat_cli = str_join(((undefined(name='nat_cli') if l_1_nat_cli is missing else l_1_nat_cli), ' static ', environment.getattr(l_1_nat, 'original_ip'), ))
            _loop_vars['nat_cli'] = l_1_nat_cli
            if t_3(environment.getattr(l_1_nat, 'original_port')):
                pass
                l_1_nat_cli = str_join(((undefined(name='nat_cli') if l_1_nat_cli is missing else l_1_nat_cli), ' ', environment.getattr(l_1_nat, 'original_port'), ))
                _loop_vars['nat_cli'] = l_1_nat_cli
            if t_3(environment.getattr(l_1_nat, 'access_list')):
                pass
                l_1_nat_cli = str_join(((undefined(name='nat_cli') if l_1_nat_cli is missing else l_1_nat_cli), ' access-list ', environment.getattr(l_1_nat, 'access_list'), ))
                _loop_vars['nat_cli'] = l_1_nat_cli
            l_1_nat_cli = str_join(((undefined(name='nat_cli') if l_1_nat_cli is missing else l_1_nat_cli), ' ', environment.getattr(l_1_nat, 'translated_ip'), ))
            _loop_vars['nat_cli'] = l_1_nat_cli
            if t_3(environment.getattr(l_1_nat, 'translated_port')):
                pass
                l_1_nat_cli = str_join(((undefined(name='nat_cli') if l_1_nat_cli is missing else l_1_nat_cli), ' ', environment.getattr(l_1_nat, 'translated_port'), ))
                _loop_vars['nat_cli'] = l_1_nat_cli
            if t_3(environment.getattr(l_1_nat, 'protocol')):
                pass
                l_1_nat_cli = str_join(((undefined(name='nat_cli') if l_1_nat_cli is missing else l_1_nat_cli), ' protocol ', environment.getattr(l_1_nat, 'protocol'), ))
                _loop_vars['nat_cli'] = l_1_nat_cli
            if t_3(environment.getattr(l_1_nat, 'group')):
                pass
                l_1_nat_cli = str_join(((undefined(name='nat_cli') if l_1_nat_cli is missing else l_1_nat_cli), ' group ', environment.getattr(l_1_nat, 'group'), ))
                _loop_vars['nat_cli'] = l_1_nat_cli
            if t_3(environment.getattr(l_1_nat, 'comment')):
                pass
                l_1_nat_cli = str_join(((undefined(name='nat_cli') if l_1_nat_cli is missing else l_1_nat_cli), ' comment ', environment.getattr(l_1_nat, 'comment'), ))
                _loop_vars['nat_cli'] = l_1_nat_cli
            yield '   '
            yield str((undefined(name='nat_cli') if l_1_nat_cli is missing else l_1_nat_cli))
            yield '\n'
    l_1_nat = l_1_nat_cli = missing
    for l_1_nat in t_2(t_1(environment.getattr(environment.getattr((undefined(name='interface_ip_nat') if l_0_interface_ip_nat is missing else l_0_interface_ip_nat), 'source'), 'dynamic'), []), 'access_list'):
        l_1_valid = l_1_nat_cli = missing
        _loop_vars = {}
        pass
        l_1_valid = False
        _loop_vars['valid'] = l_1_valid
        l_1_nat_cli = str_join(('ip nat source dynamic access-list ', environment.getattr(l_1_nat, 'access_list'), ))
        _loop_vars['nat_cli'] = l_1_nat_cli
        if (environment.getattr(l_1_nat, 'nat_type') == 'overload'):
            pass
            l_1_nat_cli = str_join(((undefined(name='nat_cli') if l_1_nat_cli is missing else l_1_nat_cli), ' overload', ))
            _loop_vars['nat_cli'] = l_1_nat_cli
            l_1_valid = True
            _loop_vars['valid'] = l_1_valid
        elif t_3(environment.getattr(l_1_nat, 'pool_name')):
            pass
            l_1_nat_cli = str_join(((undefined(name='nat_cli') if l_1_nat_cli is missing else l_1_nat_cli), ' pool ', environment.getattr(l_1_nat, 'pool_name'), ))
            _loop_vars['nat_cli'] = l_1_nat_cli
            l_1_valid = True
            _loop_vars['valid'] = l_1_valid
            if (environment.getattr(l_1_nat, 'nat_type') == 'pool-address-only'):
                pass
                l_1_nat_cli = str_join(((undefined(name='nat_cli') if l_1_nat_cli is missing else l_1_nat_cli), ' address-only', ))
                _loop_vars['nat_cli'] = l_1_nat_cli
            elif (environment.getattr(l_1_nat, 'nat_type') == 'pool-full-cone'):
                pass
                l_1_nat_cli = str_join(((undefined(name='nat_cli') if l_1_nat_cli is missing else l_1_nat_cli), ' full-cone', ))
                _loop_vars['nat_cli'] = l_1_nat_cli
        if (undefined(name='valid') if l_1_valid is missing else l_1_valid):
            pass
            if (t_1(environment.getattr(l_1_nat, 'priority'), 0) > 0):
                pass
                l_1_nat_cli = str_join(((undefined(name='nat_cli') if l_1_nat_cli is missing else l_1_nat_cli), ' priority ', environment.getattr(l_1_nat, 'priority'), ))
                _loop_vars['nat_cli'] = l_1_nat_cli
            if t_3(environment.getattr(l_1_nat, 'comment')):
                pass
                l_1_nat_cli = str_join(((undefined(name='nat_cli') if l_1_nat_cli is missing else l_1_nat_cli), ' comment ', environment.getattr(l_1_nat, 'comment'), ))
                _loop_vars['nat_cli'] = l_1_nat_cli
            yield '   '
            yield str((undefined(name='nat_cli') if l_1_nat_cli is missing else l_1_nat_cli))
            yield '\n'
    l_1_nat = l_1_valid = l_1_nat_cli = missing
    for l_1_nat in t_2(t_1(environment.getattr(environment.getattr((undefined(name='interface_ip_nat') if l_0_interface_ip_nat is missing else l_0_interface_ip_nat), 'destination'), 'static'), []), 'original_ip'):
        l_1_nat_cli = resolve('nat_cli')
        _loop_vars = {}
        pass
        if ((not (t_3(environment.getattr(l_1_nat, 'access_list')) and t_3(environment.getattr(l_1_nat, 'group')))) and (not ((not t_3(environment.getattr(l_1_nat, 'original_port'))) and t_3(environment.getattr(l_1_nat, 'translated_port'))))):
            pass
            l_1_nat_cli = 'ip nat destination'
            _loop_vars['nat_cli'] = l_1_nat_cli
            if t_3(environment.getattr(l_1_nat, 'direction')):
                pass
                l_1_nat_cli = str_join(((undefined(name='nat_cli') if l_1_nat_cli is missing else l_1_nat_cli), ' ', environment.getattr(l_1_nat, 'direction'), ))
                _loop_vars['nat_cli'] = l_1_nat_cli
            l_1_nat_cli = str_join(((undefined(name='nat_cli') if l_1_nat_cli is missing else l_1_nat_cli), ' static ', environment.getattr(l_1_nat, 'original_ip'), ))
            _loop_vars['nat_cli'] = l_1_nat_cli
            if t_3(environment.getattr(l_1_nat, 'original_port')):
                pass
                l_1_nat_cli = str_join(((undefined(name='nat_cli') if l_1_nat_cli is missing else l_1_nat_cli), ' ', environment.getattr(l_1_nat, 'original_port'), ))
                _loop_vars['nat_cli'] = l_1_nat_cli
            if t_3(environment.getattr(l_1_nat, 'access_list')):
                pass
                l_1_nat_cli = str_join(((undefined(name='nat_cli') if l_1_nat_cli is missing else l_1_nat_cli), ' access-list ', environment.getattr(l_1_nat, 'access_list'), ))
                _loop_vars['nat_cli'] = l_1_nat_cli
            l_1_nat_cli = str_join(((undefined(name='nat_cli') if l_1_nat_cli is missing else l_1_nat_cli), ' ', environment.getattr(l_1_nat, 'translated_ip'), ))
            _loop_vars['nat_cli'] = l_1_nat_cli
            if t_3(environment.getattr(l_1_nat, 'translated_port')):
                pass
                l_1_nat_cli = str_join(((undefined(name='nat_cli') if l_1_nat_cli is missing else l_1_nat_cli), ' ', environment.getattr(l_1_nat, 'translated_port'), ))
                _loop_vars['nat_cli'] = l_1_nat_cli
            if t_3(environment.getattr(l_1_nat, 'protocol')):
                pass
                l_1_nat_cli = str_join(((undefined(name='nat_cli') if l_1_nat_cli is missing else l_1_nat_cli), ' protocol ', environment.getattr(l_1_nat, 'protocol'), ))
                _loop_vars['nat_cli'] = l_1_nat_cli
            if t_3(environment.getattr(l_1_nat, 'group')):
                pass
                l_1_nat_cli = str_join(((undefined(name='nat_cli') if l_1_nat_cli is missing else l_1_nat_cli), ' group ', environment.getattr(l_1_nat, 'group'), ))
                _loop_vars['nat_cli'] = l_1_nat_cli
            if t_3(environment.getattr(l_1_nat, 'comment')):
                pass
                l_1_nat_cli = str_join(((undefined(name='nat_cli') if l_1_nat_cli is missing else l_1_nat_cli), ' comment ', environment.getattr(l_1_nat, 'comment'), ))
                _loop_vars['nat_cli'] = l_1_nat_cli
            yield '   '
            yield str((undefined(name='nat_cli') if l_1_nat_cli is missing else l_1_nat_cli))
            yield '\n'
    l_1_nat = l_1_nat_cli = missing
    for l_1_nat in t_2(t_1(environment.getattr(environment.getattr((undefined(name='interface_ip_nat') if l_0_interface_ip_nat is missing else l_0_interface_ip_nat), 'destination'), 'dynamic'), []), 'access_list'):
        l_1_nat_cli = missing
        _loop_vars = {}
        pass
        l_1_nat_cli = str_join(('ip nat destination dynamic access-list ', environment.getattr(l_1_nat, 'access_list'), ' pool ', environment.getattr(l_1_nat, 'pool_name'), ))
        _loop_vars['nat_cli'] = l_1_nat_cli
        if (t_1(environment.getattr(l_1_nat, 'priority'), 0) > 0):
            pass
            l_1_nat_cli = str_join(((undefined(name='nat_cli') if l_1_nat_cli is missing else l_1_nat_cli), ' priority ', environment.getattr(l_1_nat, 'priority'), ))
            _loop_vars['nat_cli'] = l_1_nat_cli
        if t_3(environment.getattr(l_1_nat, 'comment')):
            pass
            l_1_nat_cli = str_join(((undefined(name='nat_cli') if l_1_nat_cli is missing else l_1_nat_cli), ' comment ', environment.getattr(l_1_nat, 'comment'), ))
            _loop_vars['nat_cli'] = l_1_nat_cli
        yield '   '
        yield str((undefined(name='nat_cli') if l_1_nat_cli is missing else l_1_nat_cli))
        yield '\n'
    l_1_nat = l_1_nat_cli = missing

blocks = {}
debug_info = '3=30&4=34&6=36&7=38&8=40&10=42&11=44&12=46&14=48&15=50&17=52&18=54&19=56&21=58&22=60&24=62&25=64&27=66&28=68&30=71&34=74&35=78&36=80&37=82&38=84&39=86&40=88&41=90&42=92&43=94&44=96&45=98&46=100&49=102&50=104&51=106&53=108&54=110&56=113&60=116&61=120&63=122&64=124&65=126&67=128&68=130&69=132&71=134&72=136&74=138&75=140&76=142&78=144&79=146&81=148&82=150&84=152&85=154&87=157&91=160&92=164&93=166&94=168&96=170&97=172&99=175'