from setuptools import setup

setup(
    name='nmecpy',
    version='1.3.7',    
    description='An implementation of peer-reviewed energy data analysis algorithms in Python for site-specific M&V',
    url='https://github.com/kW-Labs/nmecpy',
    author='Maggie Jacoby, Deter Luu, Devan Johnson',
    author_email='dbardin@kw-engineering.com',
    license='MIT',
    packages=['nmecpy'],
    install_requires=['scikit-learn',
                      'pandas', 
                      'seaborn',                    
                      ],

    classifiers=[
        
    ],
)