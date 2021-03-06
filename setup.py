from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='craid',
    url='https://github.com/HausReport/ClubRaiders',
    author='Erlaed',
    author_email='Erlaed2@fdev.not',
    # Needed to actually package something
    # packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    packages=['assets', 'craid', 'craid.bgsBuddy', 'craid.eddb', 'craid.eddb.base', 'craid.eddb.faction',
              'craid.eddb.loader', 'craid.eddb.loader.strategy',
              'craid.eddb.powers', 'craid.eddb.system',
              'craid.eddb.util', 'craid.eddb.util.dataUpdate',
              'craid.history',
              'craid.dashbd', 'craid.dashbd.assets', 'craid.dashbd.queries', 'craid.dashbd.text',
              'craid.club', 'craid.club.regions'],
    # Needed for dependencies
    install_requires=['dash', 'dash-core-components', 'dash-html-components', 'dash-table', 'dash-renderer',
                      'flask', 'pandas', 'requests', 'setuptools', 'numpy', 'python-dateutil', 'ujson', 'urllib3',
                      'psutil', 'plotly', 'humanize', 'boto3', 'botocore'],
    include_package_data=True,
    # *strongly* suggested for sharing
    version='0.8693',
    # The license can be anything you like
    license='BSD-3',
    description='Club-Raiders API and application for Elite Dangerous',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)
