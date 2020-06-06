from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='craid',
    url='https://github.com/HausReport/ClubRaiders',
    author='Erlaed',
    author_email='Erlaed2@fdev.not',
    # Needed to actually package something
    # packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    packages=['assets', 'craid', 'craid.eddb', 'craid.eddb.loader', 'craid.eddb.util', 'craid.edbgs',
              'craid.dashbd', 'craid.dashbd.assets', 'craid.dashbd.queries', 'craid.dashbd.text',
              'craid.club', 'craid.club.regions'],
    # Needed for dependencies
    install_requires=['dash', 'dash-core-components', 'dash-html-components', 'dash-table', 'dash-renderer',
                      'flask', 'pandas', 'requests', 'setuptools', 'numpy', 'python-dateutil', 'ujson', 'json-lines', 'urllib3',
                      'psutil', 'plotly'],
    include_package_data=True,
    # *strongly* suggested for sharing
    version='0.76',
    # The license can be anything you like
    license='BSD-3',
    description='Placeholder description',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)
