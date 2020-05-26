from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='craid',
    url='https://github.com/HausReport/ClubRaiders',
    author='Erlaed',
    author_email='Erlaed2@fdev.not',
    # Needed to actually package something
    # packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    packages=['craid', 'craid.eddb', 'craid.club', 'craid.css', 'craid.dash', 'craid.dash.queries', 'craid.dash.text',
              'craid.eddb', 'craid.club.regions'],
    # Needed for dependencies
    install_requires=['numpy', 'dash', 'pandas', 'requests', 'setuptools'],
    # *strongly* suggested for sharing
    version='0.54',
    # The license can be anything you like
    license='MIT',
    description='Placeholder description',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)
