from setuptools import setup, find_packages

version = '1.1.dev0'

setup(name='md.recipe.luarocks',
      version=version,
      description="A zc.buildout recipe for installing luarocks dependencies",
      long_description=open('CHANGES.rst').read(),
      package_dir={'': 'src'},
      packages=find_packages('src'),
      classifiers=[
          'Framework :: Buildout',
          'Intended Audience :: Developers',
          'Programming Language :: Python :: 2',
          'Topic :: Software Development :: Build Tools',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'License :: OSI Approved :: BSD License',
      ],
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
