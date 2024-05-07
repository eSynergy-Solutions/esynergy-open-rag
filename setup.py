from setuptools import find_packages, setup

with open("src/requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="esynergy-open-rag",
    version="0.1.3",
    author="Edwin",
    author_email="genai@esynergy.co.uk",
    packages=find_packages("src", include=["components", "models", "streamlit_components", "*"]),
    package_dir={"": "src"},
    url="https://esynergy.co.uk",
    license="LICENSE.txt",
    description="Open RAG",
    long_description=open("README.md").read(),
    install_requires=required,
)
