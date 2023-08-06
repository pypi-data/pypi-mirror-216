from setuptools import setup

setup(
    name='toodetest',
    version='0.2.0',
    author='Thibault Jaigu',
    author_email='thibault.jaigu@gmail.com',
    description='Toodetest Library',
    py_modules=["toodetest"],
    package_dir={'': 'src'},
    long_description='The best boefies library in the world',
    url='https://github.com/Thibault00/toodetest',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
)
