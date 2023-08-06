from setuptools import find_packages
from setuptools import setup


version = '3.0'

form_requires = [
    'grokcore.formlib >= 1.4',
    'five.formlib',
    'zope.formlib',
]
layout_requires = [
    'grokcore.layout',
]
test_requires = form_requires + layout_requires + [
]

setup(name='five.grok',
      version=version,
      description="Grok-like layer for Zope",
      long_description=open("README.rst").read() + "\n" +
      open("CHANGES.rst").read(),
      classifiers=[
          "Environment :: Web Environment",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: Zope Public License",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Framework :: Zope :: 5",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Programming Language :: Python :: 3.11",
      ],
      keywords='zope grok',
      author='Lennart Regebro, Godefroid Chapelle',
      author_email='zope-dev@zope.dev',
      url='https://github.com/zopefoundation/five.grok',
      license='ZPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['five'],
      include_package_data=True,
      zip_safe=False,
      python_requires='>=3.7',
      install_requires=[
          'setuptools',
          'martian',
          'Zope >= 4',
          'five.localsitemanager >= 2.0',
          'grokcore.annotation',
          'grokcore.component >= 2.5',
          'grokcore.security >= 1.6.1',
          'grokcore.site',
          'grokcore.view >= 1.12.1',
          'grokcore.viewlet >= 1.3',
          'zope.annotation',
          'zope.component',
          'zope.container',
          'zope.contentprovider',
          'zope.interface',
          'zope.location',
          'zope.pagetemplate',
          'zope.publisher',
          'zope.traversing',
      ],
      extras_require={
          'form': form_requires,
          'layout': layout_requires,
          'test': test_requires},
      )
