from setuptools import setup, find_packages, find_namespace_packages

with open('README.rst', mode='r', encoding='utf-8') as f:
    long_description = f.read()

author = 'am230'
name = 'strinpy'
py_modules = [name]

setup(
    name=name,
    version="0.0.2",
    keywords=["string"],
    description="React like string builder",
    long_description=long_description,
    license="MIT Licence",
    long_description_content_type='text/x-rst',
    packages=find_packages(),
    url=f"https://github.com/{author}/{name}",
    author=author,
    py_modules=py_modules,
    platforms="any",
)
