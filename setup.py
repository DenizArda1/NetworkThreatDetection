from setuptools import find_packages, setup
from typing import List

E_DOT = '-e .'

def get_requirements(file_path:str)->List[str]:
    """
    Returns the list of requirements
    """
    try:
        requirements = []
        with open(file_path) as file_obj:
            requirements = file_obj.readlines()
            requirements = [requirement.replace("\n", "") for requirement in requirements]

            if E_DOT in requirements:
                requirements.remove(E_DOT)
            return requirements
    except FileNotFoundError:
        print("Requirements file not found")

print(get_requirements('requirements.txt'))

setup(
    name="NetworkSecurity",
    version='0.0.1',
    author="Deniz Arda",
    author_email="denizarda.sanal@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)