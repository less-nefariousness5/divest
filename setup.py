from setuptools import setup, find_packages

setup(
    name="ps-simc-parser",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'PyYAML>=5.1',
        'click>=7.0',
    ],
    entry_points={
        'console_scripts': [
            'ps-simc-parser=ps_simc_parser.__main__:cli',
        ],
    },
    author="Project Sylvanas",
    author_email="",
    description="A SimulationCraft APL to Project Sylvanas Lua converter",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/less-nefariousness5/ps-simc-parser",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)