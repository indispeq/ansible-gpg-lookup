# (c) 2016, Aron Szekely <aron(at)indispeq.com>
#
# Ansible GPG lookup plugin
#
# USAGE: {{ lookup('gpg', 'secrets.yml.gpg', passphrasefile='pp.txt', gpgbinary='gpg2') }}
#
# passphrasefile can be used to avoid gpg passphrase prompts in automation scenarios (optional)
#
# gpgbinary can be used to specify a different binary for python-gnupg than the default 'gpg'
# it will take just a command or a path just like the python module (optional)
#
# Requires python-gnupg library. Install with pip.
#
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase

import yaml
import gnupg

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        ret = []

        passphrase = None

        passphrasefile = kwargs.get('passphrasefile', None)
        gpgbinary = kwargs.get('gpgbinary', None)

        if passphrasefile:
            try:
                pf = self.find_file_in_search_path(variables, 'files', passphrasefile)
                passphrase, show_data = self._loader._get_file_contents(pf)
                display.vvvv(u"Using passphrase file %s" % passphrasefile)
            except AnsibleParserError:
                raise AnsibleError("Could not locate file containing GPG passphrase: %s" % passphrasefile)

        for term in terms:
            display.debug("GPG file to decrypt: %s" % term)

            # Find the file in the expected search path
            lookupfile = self.find_file_in_search_path(variables, 'files', term)
            display.vvvv(u"GPG lookup using %s as source file" % lookupfile)

            if gpgbinary:
                display.vvvv(u"Using GPG binary %s" % gpgbinary)
            else:
                display.vvvv(u"Using default system GPG")

            try:
                if lookupfile:
                    contents, show_data = self._loader._get_file_contents(lookupfile)

                    if gpgbinary:
                        gpg = gnupg.GPG(gpgbinary=gpgbinary)
                    else:
                        gpg = gnupg.GPG()

                    d = gpg.decrypt(contents.rstrip(),passphrase=passphrase)
                    y = yaml.load(d.data)
                    ret.append(y)
                else:
                    raise AnsibleParserError()
            except AnsibleParserError:
                raise AnsibleError("could not locate file in lookup: %s" % term)

            return ret
