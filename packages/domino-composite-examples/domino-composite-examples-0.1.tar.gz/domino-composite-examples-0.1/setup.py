import setuptools

with open("/data/ox5324/Domino_Examples/readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='domino-composite-examples',
    version='0.1',
    author='Josh Dorrington',
    author_email='joshua.dorrington@kit.edu',
    description='Datasets for running domino worked examples',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/joshdorrington/domino_examples',
    license='bsd-3-clause',
    packages=setuptools.find_packages(),
)