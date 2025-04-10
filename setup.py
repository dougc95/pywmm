from setuptools import setup, find_packages

setup(
    name="pywmm",
    version="0.2.1",
    description="World Magnetic Model (WMM) calculations",
    author="Douglas Rojas",
    author_email="dougcr95@gmail.com",
    packages=find_packages(include=["pywmm", "pywmm.*"]),
    package_data={
        "pywmm.data": ["*.COF"],
    },
    install_requires=[
        "numpy",
    ],
)