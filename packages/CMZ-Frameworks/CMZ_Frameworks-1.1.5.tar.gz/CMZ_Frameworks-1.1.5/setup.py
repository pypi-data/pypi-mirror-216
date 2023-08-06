from setuptools import setup, find_packages

setup(
    name='CMZ_Frameworks',
    version='1.1.5',
    author='Sandesh Vanwadi',
    author_email='Svanwadi@slb.com',
    description='This package will be use to clone any version of the automation frameworks available under CMZ',
    packages=find_packages(),
    py_modules=['QA_Practice_Frameworks'],
    install_requires=[
        'requests'  # Add any dependencies your package requires
    ],
    entry_points={
        'console_scripts': [
            'CMZ_Frameworks = QA_Practice_Frameworks:callAPI',
        ],
    },
)
