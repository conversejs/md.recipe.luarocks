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
        self.target = os.path.join(
            buildout['buildout']['parts-directory'],
            name)
        self.verbose = int(buildout['buildout'].get('verbosity', 0))

    def install(self):
        executable = self.options.get('executable', 'luarocks').strip()
        if whereis(executable) is None:
            raise zc.buildout.UserError(
                "{} wasn't found in your system's PATH environment "
                "variable.\nMake sure luarocks is installed and on your "
                "PATH.".format(executable)
            )

        rocks_to_install = self.options.get('rocks', '').split('\n')
        for rock in rocks_to_install:
            command = ' '.join([executable, 'install', '--local'] +
                               [r.strip() for r in rock.split(' ')])
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True
            )
            output, error = process.communicate()
            if process.returncode:
                raise zc.buildout.UserError(
                    "Command failed: {}\n{}".format(command, error))
            if self.verbose:
                print output
        return [self.target]

    update = install