from setuptools import setup

setup(
    name='voltage_imaging_analysis',
    version='0.1.8',    
    description='Python package used for analysing voltage imaging data.',
    url='https://github.com/rrsims21/voltage_imaging_analysis/',
    author='Ruth Sims',
    author_email='ruth.sims@inserm.fr',
    license='BSD 2-clause',
    packages=['voltage_imaging_analysis'],
    install_requires=[
                      'numpy',                     
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License', 
        'Programming Language :: Python :: 3.5',
    ],
)
