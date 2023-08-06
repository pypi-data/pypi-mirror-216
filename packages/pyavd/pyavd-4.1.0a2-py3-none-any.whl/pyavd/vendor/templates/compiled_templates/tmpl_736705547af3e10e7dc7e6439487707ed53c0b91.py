from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/aaa-accounting.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_aaa_accounting = resolve('aaa_accounting')
    try:
        t_1 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_1((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting)):
        pass
        if (t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'exec'), 'console'), 'type')) and t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'exec'), 'console'), 'group'))):
            pass
            yield 'aaa accounting exec console '
            yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'exec'), 'console'), 'type'))
            yield ' group '
            yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'exec'), 'console'), 'group'))
            yield '\n'
        if t_1(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'commands'), 'console')):
            pass
            for l_1_command_default in environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'commands'), 'console'):
                l_1_aaa_accounting_commands_commands_console_cli = resolve('aaa_accounting_commands_commands_console_cli')
                _loop_vars = {}
                pass
                if (t_1(environment.getattr(l_1_command_default, 'commands')) and t_1(environment.getattr(l_1_command_default, 'type'))):
                    pass
                    l_1_aaa_accounting_commands_commands_console_cli = str_join(('aaa accounting commands ', environment.getattr(l_1_command_default, 'commands'), ' console ', environment.getattr(l_1_command_default, 'type'), ))
                    _loop_vars['aaa_accounting_commands_commands_console_cli'] = l_1_aaa_accounting_commands_commands_console_cli
                    if t_1(environment.getattr(l_1_command_default, 'group')):
                        pass
                        l_1_aaa_accounting_commands_commands_console_cli = str_join(((undefined(name='aaa_accounting_commands_commands_console_cli') if l_1_aaa_accounting_commands_commands_console_cli is missing else l_1_aaa_accounting_commands_commands_console_cli), ' group ', environment.getattr(l_1_command_default, 'group'), ))
                        _loop_vars['aaa_accounting_commands_commands_console_cli'] = l_1_aaa_accounting_commands_commands_console_cli
                    if t_1(environment.getattr(l_1_command_default, 'logging'), True):
                        pass
                        l_1_aaa_accounting_commands_commands_console_cli = str_join(((undefined(name='aaa_accounting_commands_commands_console_cli') if l_1_aaa_accounting_commands_commands_console_cli is missing else l_1_aaa_accounting_commands_commands_console_cli), ' logging', ))
                        _loop_vars['aaa_accounting_commands_commands_console_cli'] = l_1_aaa_accounting_commands_commands_console_cli
                yield str((undefined(name='aaa_accounting_commands_commands_console_cli') if l_1_aaa_accounting_commands_commands_console_cli is missing else l_1_aaa_accounting_commands_commands_console_cli))
                yield '\n'
            l_1_command_default = l_1_aaa_accounting_commands_commands_console_cli = missing
        if (t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'exec'), 'default'), 'type')) and t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'exec'), 'default'), 'group'))):
            pass
            yield 'aaa accounting exec default '
            yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'exec'), 'default'), 'type'))
            yield ' group '
            yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'exec'), 'default'), 'group'))
            yield '\n'
        if (t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'system'), 'default'), 'type')) and t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'system'), 'default'), 'group'))):
            pass
            yield 'aaa accounting system default '
            yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'system'), 'default'), 'type'))
            yield ' group '
            yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'system'), 'default'), 'group'))
            yield '\n'
        if (t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'dot1x'), 'default'), 'type')) and t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'dot1x'), 'default'), 'group'))):
            pass
            yield 'aaa accounting dot1x default '
            yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'dot1x'), 'default'), 'type'))
            yield ' group '
            yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'dot1x'), 'default'), 'group'))
            yield '\n'
        if t_1(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'commands'), 'default')):
            pass
            for l_1_command_default in environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'commands'), 'default'):
                l_1_aaa_accounting_commands_commands_default_cli = resolve('aaa_accounting_commands_commands_default_cli')
                _loop_vars = {}
                pass
                if (t_1(environment.getattr(l_1_command_default, 'commands')) and t_1(environment.getattr(l_1_command_default, 'type'))):
                    pass
                    l_1_aaa_accounting_commands_commands_default_cli = str_join(('aaa accounting commands ', environment.getattr(l_1_command_default, 'commands'), ' default ', environment.getattr(l_1_command_default, 'type'), ))
                    _loop_vars['aaa_accounting_commands_commands_default_cli'] = l_1_aaa_accounting_commands_commands_default_cli
                    if t_1(environment.getattr(l_1_command_default, 'group')):
                        pass
                        l_1_aaa_accounting_commands_commands_default_cli = str_join(((undefined(name='aaa_accounting_commands_commands_default_cli') if l_1_aaa_accounting_commands_commands_default_cli is missing else l_1_aaa_accounting_commands_commands_default_cli), ' group ', environment.getattr(l_1_command_default, 'group'), ))
                        _loop_vars['aaa_accounting_commands_commands_default_cli'] = l_1_aaa_accounting_commands_commands_default_cli
                    if t_1(environment.getattr(l_1_command_default, 'logging'), True):
                        pass
                        l_1_aaa_accounting_commands_commands_default_cli = str_join(((undefined(name='aaa_accounting_commands_commands_default_cli') if l_1_aaa_accounting_commands_commands_default_cli is missing else l_1_aaa_accounting_commands_commands_default_cli), ' logging', ))
                        _loop_vars['aaa_accounting_commands_commands_default_cli'] = l_1_aaa_accounting_commands_commands_default_cli
                yield str((undefined(name='aaa_accounting_commands_commands_default_cli') if l_1_aaa_accounting_commands_commands_default_cli is missing else l_1_aaa_accounting_commands_commands_default_cli))
                yield '\n'
            l_1_command_default = l_1_aaa_accounting_commands_commands_default_cli = missing

blocks = {}
debug_info = '2=18&3=20&4=23&6=27&7=29&8=33&9=35&10=37&11=39&13=41&14=43&17=45&20=48&21=51&23=55&24=58&26=62&27=65&29=69&30=71&31=75&32=77&33=79&34=81&36=83&37=85&40=87'