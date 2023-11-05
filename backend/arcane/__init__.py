from setuptools import setup, find_packages

setup(
    name='ARCANE',
    version='0.0.1.dev',
    maintainer='Team Data Bytes',
    description='ARCANE API',
    keywords=[],
    packages=find_packages(exclude=["test"]),
    project_urls={},
    install_requires=[
        'pandas',
        'requests',
        'requests-toolbelt',
    ],
    python_requires='>=3.8',
)
