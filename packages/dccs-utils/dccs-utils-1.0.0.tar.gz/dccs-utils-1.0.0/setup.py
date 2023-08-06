from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dccs-utils",
    version="1.0.0",
    author="Md Saimun",
    author_email="teamdccs@gmail.com",
    description="Utility library for making HTTP requests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dccs-team/DCCSUtils",
    packages=["dccs_utils"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    install_requires=[
        'requests',
        'beautifulsoup4',
        # Add more required modules here
    ],
    zip_safe=False
)
