import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='rowSumExplorer',
    version='1.5',
    author='Leonidas Dosas',
    author_email='liontas76@gmail.com',
    description='Testing installation of Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    donwload_url='https://github.com/oLiontas/RowSumExplorer/blob/main/dist/rowSumExplorer-1.5.tar.gz',
    url='https://github.com/oLiontas/RowSumExplorer',
    project_urls = {
        ""
    },
    license='MIT',
    packages=['rowSumExplorer'],
    install_requires=['pandas','openpyxl']
)
