"""
Setup script for Analysis Dashboard
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="analysis-dashboard",
    version="1.0.0",
    author="Zagros Pro Technical Team",
    author_email="info@zagrospro.com",
    description="BI Management Dashboard for Google Analytics 4 and Microsoft Clarity",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mhmdhosn821/analysis_dashboard_program",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "analysis-dashboard=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["assets/*", "locales/*"],
    },
)
