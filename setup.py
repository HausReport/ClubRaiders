from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='Named',
    url='https://github.com/HausReport/ClubRaiders',
    author='Erlaed',
    author_email='Erlaed@fdev.not',
    # Needed to actually package something
    packages=['named'],
    # Needed for dependencies
    #install_requires=['numpy'],
    # *strongly* suggested for sharing
    version='0.2',
    # The license can be anything you like
    license='MIT',
    description='Placeholder description',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)
