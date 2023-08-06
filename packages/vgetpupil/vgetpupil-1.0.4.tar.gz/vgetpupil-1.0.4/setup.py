from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

long_description = 'Command line program to write the pupil positions data from input videos.'

setup(
    name='vgetpupil',
    version='1.0.4',
    author='Zaw Lin Tun',
    author_email='zawlintun1511@gmail.com',
    url='https://github.com/jtur044/vgetpupil.git',
    description='pupil positions generator program',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache Software",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'vgetpupil = vgetpupil.vget:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    keywords='pupil positions generator program vgetpupil',
    install_requires=requirements,
    zip_safe=False
)
