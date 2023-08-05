import setuptools

setuptools.setup(
    name="contextplot",
    version="0.0.4",
    author="Josh Burkart",
    description=
    "Context manager-based API for making Matplotlib plots in Jupyter notebooks",
    packages=setuptools.find_packages(),
    install_requires=[
        'IPython',
        'matplotlib',
        'numpy',
    ],
)
