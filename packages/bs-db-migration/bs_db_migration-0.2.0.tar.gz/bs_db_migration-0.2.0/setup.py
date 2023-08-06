from setuptools import setup, find_packages

long_description = """BS DB Migration"""

INSTALL_REQUIRES = ["psycopg2", "pymssql", "pyyaml"]

setup(
    name="bs_db_migration",
    version="0.2.0",
    author="Jinwon Choi",
    author_email="jinwon@hatiolab.com",
    url="https://github.com/vincent841/ms2postgres.git",
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(
        where="src", include=["bs_db_migration", "bs_db_migration.*"]
    ),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={
        "": ["LICENSE", "README.md", "requirements.txt"],
    },
    license="MIT",
    description="BS DB Migration",
    long_description=long_description,
    keywords=[
        "database migration",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
