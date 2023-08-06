import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Heterogeneous_Highway_Env",
    version="0.0.2",
    author="Xiyang Wu",
    author_email="wuxiyang1996@gmail.com",
    description="Codebase for for our version of highway-way modified for iPLAN paper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wuxiyang1996/HighwayEnv_iPLAN",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)