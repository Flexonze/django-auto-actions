from pathlib import Path
from setuptools import setup, find_packages

VERSION = "0.1.0"
DESCRIPTION = "Generates Django admin actions based on your model's fields"
this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / "README.md").read_text()

setup(
    name='django-auto-actions',
    description=DESCRIPTION,
    version=VERSION,
    author='Félix Gravel',
    author_email="felix.gravel@tlmgo.com",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'Django>=4.2',
    ],
    # url=""  # TODO: Add Github URL
)
