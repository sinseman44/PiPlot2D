import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PiPlot2D",
    version="0.0.1",
    author="sinseman44",
    author_email="sinseman44@gmail.com",
    description="Control PiPlot2D system",
    long_description="Control PiPlot2D system",
    long_description_content_type="text/markdown",
    url="https://github.com/sinseman44/PiPlot2D",
    packages=setuptools.find_packages(where='piplot'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
    install_requires=[
        'RPi.GPIO',
        'RPLCD',
        'PyCNC<=2.0.0'
    ],
    dependency_links=[
        "https://github.com/sinseman44/PyCNC/archive/v2.0.0.zip#egg=pycnc-2.0.0",
    ],
    python_requires='>=3.6',
    scripts=['piplotter']
)
