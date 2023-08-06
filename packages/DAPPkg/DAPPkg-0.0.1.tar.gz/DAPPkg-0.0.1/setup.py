from setuptools import setup, find_packages

setup(
    name='DAPPkg',
    version='0.0.1',
    description='Data Analysis Platform package',
    author='ksr8308',
    author_email='',
    url='',
    install_requires=['numpy','pandas', 'scikit-learn', 'scipy', 'statsmodels', 'requests'],
    packages=find_packages(exclude=[]),
    keywords=['Data Analysis Platform', 'DAP', 'data analysis'],
    python_requires='>=3.9',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
