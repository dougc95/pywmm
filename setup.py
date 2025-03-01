from setuptools import setup, find_packages

setup(
    name="pywmm",
    version="0.1.0",
    description="World Magnetic Model (WMM) calculations",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "pywmm": ["data/WMM.COF"],
    },
    install_requires=[
        "numpy",
    ],
)
