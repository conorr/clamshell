from distutils.core import setup, Extension
setup(name='clamshellrl', version='1.0',  \
      ext_modules=[Extension('clamshellrl',
                             ['clamshellrl.c'],
                             extra_link_args=['-lreadline'])])
