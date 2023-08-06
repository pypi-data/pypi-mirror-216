from setuptools import setup, find_packages

setup(
    name='py_brainage',
    version='0.0.22',
    description='Description of your package',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'scikit-learn',
        'numpy'
    ],
)

