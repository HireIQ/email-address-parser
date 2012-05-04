from setuptools import setup


setup(
    name="eparser",
    version="0.0.1",
    description="Generic Email-Address List Parser",
    url="https://github.com/HireIQ/email-address-parser",
    author="Alex Milstead",
    author_email="alex@amilstead.com",
    license="MIT License",
    package_dir={"": "src"},
    packages = ["eparser"],
    py_modules=["parsers"],
    install_requires=[ ]
)