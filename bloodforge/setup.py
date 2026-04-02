from setuptools import setup, find_packages

setup(
    name="bloodforge",
    version="0.1.0",
    description="Entropy-driven cognitive combat simulator (BF-CCSF v6.0)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Steven Lanier-Egu",
    author_email="your.email@example.com",  # Change to your actual email if you want
    url="https://github.com/Maxbanker/BloodForge",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy",
        "scipy",
        "pandas",
        "matplotlib",
        "seaborn",
        "streamlit",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment :: Simulation",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)