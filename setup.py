import setuptools

setuptools.setup(
    name='mylibtest',
    packages=setuptools.find_packages(include=['mylibtest']),
    version='0.0.1',
    python_requires='>=3.6',
    install_requires=['numpy'],
    description='My first Python library',
    author='Duong Vu',
    author_email="duongvv.uet@gmail.com",
    license='VDV',
)
