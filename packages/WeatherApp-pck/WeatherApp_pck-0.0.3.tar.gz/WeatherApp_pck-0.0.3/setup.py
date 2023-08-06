import setuptools

setuptools.setup(
    name="WeatherApp_pck",
    version="0.0.3",
    author="Jan Osredkar",
    author_email="jo6434@student.uni-lj.si",
    description="Package WeatherApp with whl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # python_requires='greaterthan=3.6',
    python_requires='>=3.6'
)