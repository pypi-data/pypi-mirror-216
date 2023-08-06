from setuptools import setup, find_packages

setup(
    name="polylog",
    version="0.1.1",
    description="A custom python logging package",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    author="lvlcn-t",
    author_email="75443136+lvlcn-t@users.noreply.github.com",
    url="https://github.com/lvlcn-t/PolyLog",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
