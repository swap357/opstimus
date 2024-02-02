from setuptools import setup, find_packages

setup(
    name='Opstimus',
    version='1.0',
    packages=find_packages(),
    description='gpt for server cluster management',
    author='Swapnil Patel',
    author_email='swapnilpatel357@gmail.com',
    url='https://github.com/swap357/opstimus',  # if applicable
    entry_points={
        'console_scripts': [
            'opstimus=ops:main',  # Adjust according to your package structure
        ],
    },
    install_requires=[
        # List your project's dependencies here
        # 'requests',
    ],
)