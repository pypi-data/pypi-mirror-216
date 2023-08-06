from setuptools import setup

setup(
    name='bitbucket-pipes-toolkit',
    version='3.3.0',
    packages=['bitbucket_pipes_toolkit', ],
    url='https://bitbucket.org/bitbucketpipelines/bitbucket-pipes-toolkit',
    author='Atlassian',
    author_email='bitbucketci-team@atlassian.com',
    description='This package contains various helpers for developing bitbucket pipelines pipes',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=['colorama>=0.4.3',
                      'colorlog>=4.0,<7.0',
                      'pyyaml>=5.4',
                      'Cerberus>=1.2,<2.0',
                      'docker[tls]>=4.2,<5.0.0',
                      'GitPython==3.*']
)
