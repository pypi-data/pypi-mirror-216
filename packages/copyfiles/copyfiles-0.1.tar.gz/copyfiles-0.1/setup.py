from setuptools import setup

readme = open("./README.md","r")

setup(
    name='copyfiles',
    packages=['copyfiles'],
    version='0.1',
    description='Esta es la direccion de mi paquete',
    long_description=readme.read(),
    long_description_content_type="text/markdown",
    author='Wendy Espinoza',
    author_email='wendy.espinoza013@gmail.com',
    install_requires=['os','shutil'],
    url='https://github.com/Wendy013/copy_files',
    license = 'MIT',
    include_package_data=True
)




