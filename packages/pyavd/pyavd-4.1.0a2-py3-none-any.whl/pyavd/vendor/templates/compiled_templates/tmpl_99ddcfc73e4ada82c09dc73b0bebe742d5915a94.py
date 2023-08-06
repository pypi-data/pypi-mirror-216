from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/roles.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_roles = resolve('roles')
    try:
        t_1 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_1((undefined(name='roles') if l_0_roles is missing else l_0_roles)):
        pass
        yield '!\n'
        for l_1_role in (undefined(name='roles') if l_0_roles is missing else l_0_roles):
            _loop_vars = {}
            pass
            if t_1(environment.getattr(l_1_role, 'name')):
                pass
                yield 'role '
                yield str(environment.getattr(l_1_role, 'name'))
                yield '\n'
                if t_1(environment.getattr(l_1_role, 'sequence_numbers')):
                    pass
                    for l_2_sequence in environment.getattr(l_1_role, 'sequence_numbers'):
                        l_2_sequence_cli = resolve('sequence_cli')
                        _loop_vars = {}
                        pass
                        if (t_1(environment.getattr(l_2_sequence, 'action')) and t_1(environment.getattr(l_2_sequence, 'command'))):
                            pass
                            l_2_sequence_cli = ''
                            _loop_vars['sequence_cli'] = l_2_sequence_cli
                            if t_1(environment.getattr(l_2_sequence, 'sequence')):
                                pass
                                l_2_sequence_cli = str_join((environment.getattr(l_2_sequence, 'sequence'), ' ', ))
                                _loop_vars['sequence_cli'] = l_2_sequence_cli
                            l_2_sequence_cli = str_join(((undefined(name='sequence_cli') if l_2_sequence_cli is missing else l_2_sequence_cli), environment.getattr(l_2_sequence, 'action'), ))
                            _loop_vars['sequence_cli'] = l_2_sequence_cli
                            if t_1(environment.getattr(l_2_sequence, 'mode')):
                                pass
                                l_2_sequence_cli = str_join(((undefined(name='sequence_cli') if l_2_sequence_cli is missing else l_2_sequence_cli), ' mode ', environment.getattr(l_2_sequence, 'mode'), ))
                                _loop_vars['sequence_cli'] = l_2_sequence_cli
                            l_2_sequence_cli = str_join(((undefined(name='sequence_cli') if l_2_sequence_cli is missing else l_2_sequence_cli), ' command ', environment.getattr(l_2_sequence, 'command'), ))
                            _loop_vars['sequence_cli'] = l_2_sequence_cli
                            yield '   '
                            yield str((undefined(name='sequence_cli') if l_2_sequence_cli is missing else l_2_sequence_cli))
                            yield '\n'
                    l_2_sequence = l_2_sequence_cli = missing
        l_1_role = missing

blocks = {}
debug_info = '2=18&4=21&5=24&6=27&7=29&8=31&9=35&10=37&11=39&12=41&14=43&15=45&16=47&18=49&19=52'