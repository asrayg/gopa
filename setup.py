from setuptools import setup, find_packages
from pathlib import Path

readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="gopa-lang",
    version="0.2.0",
    description="Gopa Programming Language - A kid-friendly programming language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Gopa Contributors",
    url="https://gopa.dev",
    project_urls={
        "Documentation": "https://gopa.dev/docs",
        "Source": "https://github.com/gopa-lang/gopa",
        "Issues": "https://github.com/gopa-lang/gopa/issues",
    },
    packages=find_packages(),
    package_data={
        "gopa_lang": ["stdlib/*.gopa"],
    },
    python_requires=">=3.11",
    install_requires=[],
    extras_require={
        "network": ["requests>=2.28.0"],
    },
    entry_points={
        "console_scripts": [
            "gopa=gopa_lang.gopa:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Education",
        "Topic :: Software Development :: Interpreters",
    ],
    keywords=["programming-language", "education", "beginner-friendly", "kids-coding"],
)

