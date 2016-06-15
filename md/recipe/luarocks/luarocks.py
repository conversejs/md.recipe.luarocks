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

    def get_existing_rocks(self):
        command = ['luarocks', 'list', '--porcelain']
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, error = process.communicate()
        if process.returncode:
            raise zc.buildout.UserError(
                "Command failed: {}\n{}".format(command, error))
        return [l.split('\t') for l in output.split('\n')]

    def install(self):
        executable = self.options.get('executable', 'luarocks').strip()
        if whereis(executable) is None:
            raise zc.buildout.UserError(
                "{} wasn't found in your system's PATH environment "
                "variable.\nMake sure luarocks is installed and on your "
                "PATH.".format(executable)
            )

        existing_rocks = self.get_existing_rocks()

        rocks_to_install = self.options.get('rocks', '').split('\n')
        for line in rocks_to_install:
            rock_and_version = [r.strip() for r in line.split(' ')]
            rock = rock_and_version[0]
            version = len(rock_and_version) > 1 and rock_and_version[1] or None
            already_installed = \
                filter(lambda x: rock in x
                       and (version is None or
                            (version is not None and version in x))
                       and x[2] == 'installed',
                       existing_rocks)

            if already_installed:
                print "Skipping \"{}\"; it's already installed".format(line)
                continue

            command = ' '.join([executable, 'install', '--local'] +
                               rock_and_version)
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
