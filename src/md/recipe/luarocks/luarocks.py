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
            buildout['buildout']['parts-directory'], name)
        self.verbose = int(buildout['buildout'].get('verbosity', 0))

    def get_existing_rocks(self):
        executable = self.options.get('executable', 'luarocks').strip()
        cmd = '{} list --porcelain --tree={}'.format(executable, self.target)
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        if error:
            print(error)
        if process.returncode:
            raise zc.buildout.UserError(
                "Command failed: {}\n{}".format(cmd, error))
        if output:
            output = output.decode()
            return [l.split('\t') for l in output.split('\n')]
        else:
            return []

    def install(self):
        executable = self.options.get('executable', 'luarocks').strip()
        if whereis(executable) is None:
            raise zc.buildout.UserError(
                "{} wasn't found in your system's PATH environment "
                "variable.\nMake sure luarocks is installed and on your "
                "PATH.".format(executable))

        existing_rocks = self.get_existing_rocks()
        rocks_to_install = self.options.get('rocks', '').splitlines()
        for line in rocks_to_install:
            rock_and_version = [r for r in line.strip().split(' ')]
            rock = rock_and_version[0]
            if not rock:
                continue
            version = len(rock_and_version) > 1 and rock_and_version[1] or None
            already_installed = \
                [x for x in existing_rocks if
                 rock in x and
                 (version is None or (version is not None and version in x))
                 and x[2] == 'installed']
            if already_installed:
                print("Skipping \"{}\"; it's already installed".format(line))
                continue
            cmd = '{} install {} --tree={} {}'.format(
                executable,
                self.options.get('install_options', ''),
                self.target,
                ' '.join(rock_and_version))
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, error = process.communicate()
            if process.returncode:
                raise zc.buildout.UserError(
                    "Command failed: {}\n{}".format(cmd, error))
            if self.verbose:
                print(output)
        return [self.target]

    update = install
