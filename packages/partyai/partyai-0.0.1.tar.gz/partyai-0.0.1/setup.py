from setuptools import find_packages, setup

setup(
    name="partyai",
    version="0.0.1",
    packages=find_packages(),
    description="Community functions for ChatGPT",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/partyai/partyai",
    author="Imad Bouziani",
    author_email="imad.a.bouziani@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=[
        'requests',
    ],
    include_package_data=True,
)
