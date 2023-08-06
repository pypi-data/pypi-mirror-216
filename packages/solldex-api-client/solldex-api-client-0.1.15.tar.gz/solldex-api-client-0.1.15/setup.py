from setuptools import setup, find_packages

setup(
    name='solldex-api-client',
    version='0.1.15',
    packages=find_packages(),
    url='https://github.com/filterfeed/solldex-api-client',
    author='Victor Figueredo',  # replace with your name
    author_email='cto@filterfeed.com.br',
    description='Python client for the Solldex API',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
        'requests',
        'tenacity',
    ],
    python_requires='>=3.6'
)
