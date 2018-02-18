from setuptools import setup

setup(
    name='seaborn-recorder',
    version='0.0.1',
    description='SeabornRecorder will proxy an object and record all'
                ' all getattr, setattr, method calls, and instantiations',
    long_description='',
    author='Ben Christenson',
    author_email='Python@BenChristenson.com',
    url='https://github.com/SeabornGames/SeabornRecorder',
    install_requires=[],
    extras_require={
    },
    packages=['seaborn_recorder'],
    license='MIT License',
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: Other/Proprietary License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5'),
)
