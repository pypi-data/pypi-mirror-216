from setuptools import find_packages, setup

from pathlib import Path

# Lee el contenido del archivo README.md
readme_path = Path(__file__).parent / "README.md"
with open(readme_path, "r", encoding="utf-8") as f:
    long_description = f.read()
    
setup(
    name="hipal_mixin_scrud",
    version="1.0.5",
    description="Libreria para crud basica.",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.9",
    install_requires=[
        "pydantic==1.10.7",
        "sqlalchemy==2.0.15",
        "fastapi==0.95.0",
    ],
    url="http://git.hipal.com.co/libraries/ms-mixins/-/tree/feature/mixins",
    author="Hipal",
    author_email="desarrollo@hipal.com.co",
)
