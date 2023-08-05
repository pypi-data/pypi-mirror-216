from setuptools import find_packages, setup

setup(
    name="gcloud-storage-manager",
    version="0.0.1",
    description="A package to manage Google Cloud Storage",
    packages=find_packages(),
    install_requires=[],
    classifiers=[  # https://pypi.org/classifiers/
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    author="Masato Emata",
    url="https://github.com/masatoEmata/gcloud_storage_manager",
    keywords="google cloud storage",
)
