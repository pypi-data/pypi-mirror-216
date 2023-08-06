from setuptools import find_packages, setup

with open("app/JustScan/README.md", "r") as f:
    long_description = f.read()
with open("requirements.txt", "r") as f:
    install_requires = [line.strip() for line in f if line.strip()]
setup(
    name="JustScan",
    version="1.1.24",
    description="E-kyc for Industries application",
    package_dir={"": "app"},
    packages=find_packages(where="./app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.itcgroup.io/Theodore.vo",
    author="Theodore",
    author_email="theodore.v@itcgroup.io",
    keywords=["ITC", "AI", "E-kyc", "Deep Learning", "Computer Vision", "Yolov5",
              "Interface"],

    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'itc_service = JustScan.api.itc_cli:main',
        ],
    },
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.7"
)
