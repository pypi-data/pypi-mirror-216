from setuptools import setup

setup(
    name='nmecpy',
    version='0.0.3',    
    description='An implementation of peer-reviewed energy data analysis algorithms in Python for site-specific M&V',
    url='https://github.com/kW-Labs/nmecpy',
    author='Maggie Jacoby, Deter Luu, Devan Johnson',
    author_email='dbardin@kw-engineering.com',
    license='MIT',
    packages=['nmecpy'],
    install_requires=['sklearn',
                      'pandas',                     
                      ],

    classifiers=[
        
    ],
)