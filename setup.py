from pathlib import Path
from setuptools import setup, find_packages

VERSION = "0.1.3"
DESCRIPTION = "Automatically generates Django admin actions based on your model's fields"
this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / "README.md").read_text()

setup(
    name='django-auto-actions',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    version=VERSION,
    author='Félix Gravel',
    author_email="felix.gravel@tlmgo.com",
    url="https://github.com/Flexonze/django-auto-actions",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.10",
    install_requires=[
        'Django>=4.2',
    ],
    license="MIT",
    classifiers=[
      "License :: OSI Approved :: MIT License",
      "Intended Audience :: Developers",
      "Operating System :: OS Independent",
      "Programming Language :: Python",
      "Programming Language :: Python :: 3.10",
      "Programming Language :: Python :: 3.11",
      "Programming Language :: Python :: 3.12",
      "Topic :: Software Development :: Libraries :: Python Modules",
      "Framework :: Django",
      "Framework :: Django :: 4.2",
      "Framework :: Django :: 5.1",
    ]
)
