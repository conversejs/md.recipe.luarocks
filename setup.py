from setuptools import setup, find_packages

version = '0.1'

setup(name='md.recipe.luarocks',
      version=version,
      description="A zc.buildout recipe for installing luarocks dependencies",
      long_description=open('CHANGES.rst').read(),
      package_dir={'': 'src'},
      packages=find_packages('src'),
      classifiers=[],
      keywords='lua luarocks',
      author='JC Brand (Minddistrict)',
      author_email='jcbrand@minddistrict.com',
      url='',
      license='',
      namespace_packages=['md', 'md.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'zc.buildout',
          'setuptools',
      ],
      entry_points={
          'zc.buildout': [
              'default= md.recipe.luarocks:LuaRocks']
      })
