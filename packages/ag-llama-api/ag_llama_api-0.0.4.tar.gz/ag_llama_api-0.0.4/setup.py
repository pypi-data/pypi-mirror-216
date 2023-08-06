import setuptools


with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="ag_llama_api",                     # This is the name of the package
    version="0.0.4",                        # The initial release version
    author="AA",                     # Full name of the author
    description="ag_llama_api Test Package for Somthing",
    long_description="long_description",      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages= setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    scripts=["utils/download.py", "utils/render.py"],
    include_package_data=True,                                     # Information to filter the project on PyPi website
    python_requires='>=3.8',                # Minimum version requirement of the package
    # py_modules=["ag_llama_api"],             # Name of the python package
    # package_dir={'':'src'},     # Directory of the source code of the package
    install_requires=required                     # Install other dependencies if any
)