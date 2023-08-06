from setuptools import setup

setup(
    name='django-sso-client',
    version='0.0.9',
    author='TIT CS',
    author_email='contato@titcs.com.br',
    packages=['django_client_sso','django_azure','django_client_db','django_client_mail','django_utils'],
    description='Client for Django Apps - TIT/Hyper by P&D',
    long_description='Client for Django Apps - TIT/Hyper by P&D',
    url='https://TITBrasil@dev.azure.com/TITBrasil/TITCS%20-%20Live4Safe/_git/DJANGO_CLIENT',
    project_urls={
        'Código fonte': 'https://TITBrasil@dev.azure.com/TITBrasil/Gamefica/_git/DJANGO_CLIENT',
        'Download': 'https://TITBrasil@dev.azure.com/TITBrasil/Gamefica/_git/DJANGO_CLIENT'
    },
    license='MIT',
    keywords='django_client_sso django_azure django_client_db django_client_mail django_utils',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Scientific/Engineering :: Physics'
    ]
)
