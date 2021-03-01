"""
python-for-android recipe for pyksolve.
"""

from multiprocessing import cpu_count
from os.path import join

from pythonforandroid.recipe import CppCompiledComponentsPythonRecipe


class PyksolveRecipe(CppCompiledComponentsPythonRecipe):
    version = 'master'
    url = 'https://github.com/tcdude/py-klondike-solver/archive/{version}.zip'
    site_packages_name = 'pyksolve'

    depends = ['python3', 'setuptools']

    def get_recipe_env(self, arch=None, with_flags_in_cc=True):
        env = super().get_recipe_env(arch, with_flags_in_cc)
        if self.need_stl_shared:
            env['CFLAGS'] += f' -I{self.stl_include_dir}'
            env['CFLAGS'] += ' -frtti -fexceptions'

            env['LDFLAGS'] += f' -L{self.get_stl_lib_dir(arch)}'
            env['LDFLAGS'] += f' -l{self.stl_lib_name}'
        return env

#    def build_compiled_components(self, arch):
#        self.setup_extra_args = ['-j', str(cpu_count())]
#        super(PyksolveRecipe, self).build_compiled_components(arch)
#        self.setup_extra_args = []
#
#    def rebuild_compiled_components(self, arch, env):
#        self.setup_extra_args = ['-j', str(cpu_count())]
#        super(PyksolveRecipe, self).rebuild_compiled_components(arch, env)
#        self.setup_extra_args = []

recipe = PyksolveRecipe()
