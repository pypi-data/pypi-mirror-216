from setuptools import find_packages, setup

setup(
    name="load_resnet",
    version="0.0.1",
    description="A package to load resnet, made using PyTorch",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description="long_description",
    long_description_content_type="text/markdown",
    url="https://github.com/33-Papers/Deep-Residual-Learning-for-Image-Recognition",
    author="Mridul Sharma",
    author_email="mridulsharma3301@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=["bson >= 0.5.10", "torch==2.0.1", "torchinfo==1.8.0", "torchvision==0.15.2"],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.10",
)