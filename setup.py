from setuptools import setup

setup(
        name='LaMark',
        version='0.2.0',
        author='Alex Beal',
        author_email='alexlbeal@gmail.com',
        packages=['lamark', 'lamark.test'],
        url='http://github.com/beala/lamark',
        description='A tool to embedding LaTeX in Markdown',
        entry_points = {
            'console_scripts': [
                'lamark = lamark.lamark:main'
                ]
            }
)
