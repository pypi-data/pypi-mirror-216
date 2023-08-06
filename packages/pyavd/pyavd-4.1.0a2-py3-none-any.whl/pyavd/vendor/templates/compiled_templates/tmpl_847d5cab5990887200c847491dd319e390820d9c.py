from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'documentation/management-security.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_management_security = resolve('management_security')
    l_0_ssl_profiles_certs = resolve('ssl_profiles_certs')
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
        t_3 = environment.filters['join']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No filter named 'join' found.")
    try:
        t_4 = environment.filters['length']
    except KeyError:
        @internalcode
        def t_4(*unused):
            raise TemplateRuntimeError("No filter named 'length' found.")
    try:
        t_5 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_5(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_5((undefined(name='management_security') if l_0_management_security is missing else l_0_management_security)):
        pass
        yield '\n## Management Security\n\n### Management Security Summary\n\n| Settings | Value |\n| -------- | ----- |\n'
        if t_5(environment.getattr((undefined(name='management_security') if l_0_management_security is missing else l_0_management_security), 'entropy_source')):
            pass
            yield '| Entropy source | '
            yield str(environment.getattr((undefined(name='management_security') if l_0_management_security is missing else l_0_management_security), 'entropy_source'))
            yield ' |\n'
        if t_5(environment.getattr(environment.getattr((undefined(name='management_security') if l_0_management_security is missing else l_0_management_security), 'password'), 'encryption_key_common')):
            pass
            yield '| Common password encryption key | '
            yield str(environment.getattr(environment.getattr((undefined(name='management_security') if l_0_management_security is missing else l_0_management_security), 'password'), 'encryption_key_common'))
            yield ' |\n'
        if t_5(environment.getattr(environment.getattr((undefined(name='management_security') if l_0_management_security is missing else l_0_management_security), 'password'), 'encryption_reversible')):
            pass
            yield '| Reversible password encryption | '
            yield str(environment.getattr(environment.getattr((undefined(name='management_security') if l_0_management_security is missing else l_0_management_security), 'password'), 'encryption_reversible'))
            yield ' |\n'
        if t_5(environment.getattr(environment.getattr((undefined(name='management_security') if l_0_management_security is missing else l_0_management_security), 'password'), 'minimum_length')):
            pass
            yield '| Minimum password length | '
            yield str(environment.getattr(environment.getattr((undefined(name='management_security') if l_0_management_security is missing else l_0_management_security), 'password'), 'minimum_length'))
            yield ' |\n'
        if t_5(environment.getattr((undefined(name='management_security') if l_0_management_security is missing else l_0_management_security), 'ssl_profiles')):
            pass
            yield '\n### Management Security SSL Profiles\n\n| SSL Profile Name | TLS protocol accepted | Certificate filename | Key filename | Cipher List |\n| ---------------- | --------------------- | -------------------- | ------------ | ----------- |\n'
            l_0_ssl_profiles_certs = []
            context.vars['ssl_profiles_certs'] = l_0_ssl_profiles_certs
            context.exported_vars.add('ssl_profiles_certs')
            for l_1_ssl_profile in t_2(environment.getattr((undefined(name='management_security') if l_0_management_security is missing else l_0_management_security), 'ssl_profiles')):
                l_1_tmp_cert = missing
                _loop_vars = {}
                pass
                yield '| '
                yield str(t_1(environment.getattr(l_1_ssl_profile, 'name'), '-'))
                yield ' | '
                yield str(t_1(environment.getattr(l_1_ssl_profile, 'tls_versions'), '-'))
                yield ' | '
                yield str(t_1(environment.getattr(environment.getattr(l_1_ssl_profile, 'certificate'), 'file'), '-'))
                yield ' | '
                yield str(t_1(environment.getattr(environment.getattr(l_1_ssl_profile, 'certificate'), 'key'), '-'))
                yield ' | '
                yield str(t_1(environment.getattr(l_1_ssl_profile, 'cipher_list'), '-'))
                yield ' |\n'
                l_1_tmp_cert = {}
                _loop_vars['tmp_cert'] = l_1_tmp_cert
                if t_5(environment.getattr(l_1_ssl_profile, 'trust_certificate')):
                    pass
                    l_1_tmp_cert = {'trust_certificate': environment.getattr(l_1_ssl_profile, 'trust_certificate')}
                    _loop_vars['tmp_cert'] = l_1_tmp_cert
                if t_5(environment.getattr(l_1_ssl_profile, 'chain_certificate')):
                    pass
                    context.call(environment.getattr((undefined(name='tmp_cert') if l_1_tmp_cert is missing else l_1_tmp_cert), 'update'), {'chain_certificate': environment.getattr(l_1_ssl_profile, 'chain_certificate')}, _loop_vars=_loop_vars)
                if (t_4((undefined(name='tmp_cert') if l_1_tmp_cert is missing else l_1_tmp_cert)) > 0):
                    pass
                    context.call(environment.getattr((undefined(name='tmp_cert') if l_1_tmp_cert is missing else l_1_tmp_cert), 'update'), {'name': environment.getattr(l_1_ssl_profile, 'name')}, _loop_vars=_loop_vars)
                    context.call(environment.getattr((undefined(name='ssl_profiles_certs') if l_0_ssl_profiles_certs is missing else l_0_ssl_profiles_certs), 'append'), (undefined(name='tmp_cert') if l_1_tmp_cert is missing else l_1_tmp_cert), _loop_vars=_loop_vars)
            l_1_ssl_profile = l_1_tmp_cert = missing
            for l_1_ssl_profile in t_2((undefined(name='ssl_profiles_certs') if l_0_ssl_profiles_certs is missing else l_0_ssl_profiles_certs), 'name'):
                l_1_trust_certs = resolve('trust_certs')
                l_1_requirement = resolve('requirement')
                l_1_tmp_requirement = resolve('tmp_requirement')
                l_1_policy = resolve('policy')
                l_1_system = resolve('system')
                l_1_chain_certs = resolve('chain_certs')
                _loop_vars = {}
                pass
                yield '\n### SSL profile '
                yield str(environment.getattr(l_1_ssl_profile, 'name'))
                yield ' Certificates Summary\n'
                if t_5(environment.getattr(l_1_ssl_profile, 'trust_certificate')):
                    pass
                    yield '\n| Trust Certificates | Requirement | Policy | System |\n| ------------------ | ----------- | ------ | ------ |\n'
                    l_1_trust_certs = t_3(context.eval_ctx, t_1(environment.getattr(environment.getattr(l_1_ssl_profile, 'trust_certificate'), 'certificates'), '-'), ', ')
                    _loop_vars['trust_certs'] = l_1_trust_certs
                    l_1_requirement = '-'
                    _loop_vars['requirement'] = l_1_requirement
                    if t_5(environment.getattr(environment.getattr(l_1_ssl_profile, 'trust_certificate'), 'requirement')):
                        pass
                        l_1_tmp_requirement = []
                        _loop_vars['tmp_requirement'] = l_1_tmp_requirement
                        if t_5(environment.getattr(environment.getattr(environment.getattr(l_1_ssl_profile, 'trust_certificate'), 'requirement'), 'basic_constraint_ca'), True):
                            pass
                            context.call(environment.getattr((undefined(name='tmp_requirement') if l_1_tmp_requirement is missing else l_1_tmp_requirement), 'append'), 'Basic Constraint CA', _loop_vars=_loop_vars)
                        if t_5(environment.getattr(environment.getattr(environment.getattr(l_1_ssl_profile, 'trust_certificate'), 'requirement'), 'hostname_fqdn'), True):
                            pass
                            context.call(environment.getattr((undefined(name='tmp_requirement') if l_1_tmp_requirement is missing else l_1_tmp_requirement), 'append'), 'Hostname must be FQDN', _loop_vars=_loop_vars)
                        if (t_4((undefined(name='tmp_requirement') if l_1_tmp_requirement is missing else l_1_tmp_requirement)) > 0):
                            pass
                            l_1_requirement = t_3(context.eval_ctx, (undefined(name='tmp_requirement') if l_1_tmp_requirement is missing else l_1_tmp_requirement), ', ')
                            _loop_vars['requirement'] = l_1_requirement
                    l_1_policy = '-'
                    _loop_vars['policy'] = l_1_policy
                    if t_5(environment.getattr(environment.getattr(l_1_ssl_profile, 'trust_certificate'), 'policy_expiry_date_ignore'), True):
                        pass
                        l_1_policy = 'Ignore Expiry Date'
                        _loop_vars['policy'] = l_1_policy
                    if t_5(environment.getattr(environment.getattr(l_1_ssl_profile, 'trust_certificate'), 'system'), True):
                        pass
                        l_1_system = 'Enabled'
                        _loop_vars['system'] = l_1_system
                    else:
                        pass
                        l_1_system = '-'
                        _loop_vars['system'] = l_1_system
                    yield '| '
                    yield str((undefined(name='trust_certs') if l_1_trust_certs is missing else l_1_trust_certs))
                    yield ' | '
                    yield str((undefined(name='requirement') if l_1_requirement is missing else l_1_requirement))
                    yield ' | '
                    yield str((undefined(name='policy') if l_1_policy is missing else l_1_policy))
                    yield ' | '
                    yield str((undefined(name='system') if l_1_system is missing else l_1_system))
                    yield ' |\n'
                if t_5(environment.getattr(l_1_ssl_profile, 'chain_certificate')):
                    pass
                    yield '\n| Chain Certificates | Requirement |\n| ------------------ | ----------- |\n'
                    l_1_chain_certs = t_3(context.eval_ctx, t_1(environment.getattr(environment.getattr(l_1_ssl_profile, 'chain_certificate'), 'certificates'), '-'), ', ')
                    _loop_vars['chain_certs'] = l_1_chain_certs
                    l_1_requirement = '-'
                    _loop_vars['requirement'] = l_1_requirement
                    if t_5(environment.getattr(environment.getattr(l_1_ssl_profile, 'chain_certificate'), 'requirement')):
                        pass
                        l_1_tmp_requirement = []
                        _loop_vars['tmp_requirement'] = l_1_tmp_requirement
                        if t_5(environment.getattr(environment.getattr(environment.getattr(l_1_ssl_profile, 'chain_certificate'), 'requirement'), 'basic_constraint_ca'), True):
                            pass
                            context.call(environment.getattr((undefined(name='tmp_requirement') if l_1_tmp_requirement is missing else l_1_tmp_requirement), 'append'), 'Basic Constraint CA', _loop_vars=_loop_vars)
                        if t_5(environment.getattr(environment.getattr(environment.getattr(l_1_ssl_profile, 'chain_certificate'), 'requirement'), 'include_root_ca'), True):
                            pass
                            context.call(environment.getattr((undefined(name='tmp_requirement') if l_1_tmp_requirement is missing else l_1_tmp_requirement), 'append'), 'Root CA Included', _loop_vars=_loop_vars)
                        if (t_4((undefined(name='tmp_requirement') if l_1_tmp_requirement is missing else l_1_tmp_requirement)) > 0):
                            pass
                            l_1_requirement = t_3(context.eval_ctx, (undefined(name='tmp_requirement') if l_1_tmp_requirement is missing else l_1_tmp_requirement), ', ')
                            _loop_vars['requirement'] = l_1_requirement
                    yield '| '
                    yield str((undefined(name='chain_certs') if l_1_chain_certs is missing else l_1_chain_certs))
                    yield ' | '
                    yield str((undefined(name='requirement') if l_1_requirement is missing else l_1_requirement))
                    yield ' |\n'
            l_1_ssl_profile = l_1_trust_certs = l_1_requirement = l_1_tmp_requirement = l_1_policy = l_1_system = l_1_chain_certs = missing
        yield '\n### Management Security Configuration\n\n```eos\n'
        template = environment.get_template('eos/management-security.j2', 'documentation/management-security.j2')
        for event in template.root_render_func(template.new_context(context.get_all(), True, {'ssl_profiles_certs': l_0_ssl_profiles_certs})):
            yield event
        yield '```\n'

blocks = {}
debug_info = '2=43&10=46&11=49&13=51&14=54&16=56&17=59&19=61&20=64&22=66&28=69&29=72&30=77&31=87&32=89&33=91&35=93&36=95&38=96&39=98&40=99&43=101&45=111&46=113&50=116&51=118&52=120&53=122&54=124&55=126&57=127&58=129&60=130&61=132&64=134&65=136&66=138&68=140&69=142&71=146&73=149&75=157&79=160&80=162&81=164&82=166&83=168&84=170&86=171&87=173&89=174&90=176&93=179&101=185'