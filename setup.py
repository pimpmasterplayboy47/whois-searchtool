from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="whois-search-tool",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple, pure Python WHOIS lookup tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/whois_search_tool",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: Name Service (DNS)",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "whois=whois_search.whois:whois_lookup",
        ],
    },
)