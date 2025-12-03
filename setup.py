from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="jarvis-v2",
    version="2.0.0",
    author="Aptik Pandey",
    author_email="aptikpandey9@gmail.com",
    description="JARVIS v2.0 - Your Personal AI Assistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Aptik09/jarvis-v2",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "jarvis=main:main",
        ],
    },
    include_package_data=True,
    keywords="ai assistant jarvis voice chatbot automation",
    project_urls={
        "Bug Reports": "https://github.com/Aptik09/jarvis-v2/issues",
        "Source": "https://github.com/Aptik09/jarvis-v2",
        "Documentation": "https://github.com/Aptik09/jarvis-v2/docs",
    },
)
