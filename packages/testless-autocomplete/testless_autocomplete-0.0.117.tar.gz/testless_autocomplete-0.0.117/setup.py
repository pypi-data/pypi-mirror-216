from setuptools import find_packages, setup



setup(
    name="testless_autocomplete",
    version="0.0.117",
    description="Auto Complete Package",
    packages=find_packages(),
    long_description="TestLess Auto Complete Package",
    long_description_content_type="text/markdown",
    author="TestLess",
    package_data={
        '/Auto_Complete': ['/testless_autocomplete/ngram.csv'],
    },
    include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
     install_requires=["bson >= 0.5.10"],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    }
    
)
