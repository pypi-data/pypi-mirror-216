import os
from setuptools import setup, find_packages


def load_requirements(file: str):
    """
    Load requirements file and return non-empty, non-comment lines with leading and trailing
    whitespace stripped.
    """
    with open(os.path.join(os.path.dirname(__file__), file)) as f:
        return [
            line.strip() for line in f
            if line.strip() != '' and not line.strip().startswith('#')
        ]


setup(
    name='django-ucam-apigatewayauth',
    description='A Django module allow auth based on the headers passed from the API Gateway',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.developers.cam.ac.uk/uis/devops/django/api-gateway-auth',
    version='0.0.3',
    license='MIT',
    author='DevOps Division, University Information Services, University of Cambridge',
    author_email='devops@uis.cam.ac.uk',
    packages=find_packages(),
    include_package_data=True,
    install_requires=load_requirements('requirements.txt'),
    classifiers=[
        'Development Status :: 3 - Alpha ',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
