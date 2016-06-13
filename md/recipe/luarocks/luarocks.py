import os
import subprocess
import zc.buildout


def whereis(program):
    for path in os.environ.get('PATH', '').split(':'):
        if os.path.exists(os.path.join(path, program)) and \
                not os.path.isdir(os.path.join(path, program)):
            return os.path.join(path, program)
    return None


class LuaRocks(object):

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        self.verbose = int(buildout['buildout'].get('verbosity', 0))

    def install(self):
        if whereis('luarocks') is None:
            raise zc.buildout.UserError(
                "luarocks wasn't found in your system's PATH environment "
                "variable.\nMake sure luarocks is installed and set on your "
                "PATH."
            )

        rocks_to_install = self.options.get('rocks', '').split('\n')
        for rock in rocks_to_install:
            command = ' '.join(['luarocks', 'install', '--local'] +
                               [r.strip() for r in rock.split(' ')])
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True
            )
            output, error = process.communicate()
            if process.returncode:
                raise zc.buildout.UserError(
                    "Command failed: {}\n{}".format(command, error))

    update = install
