import setuptools
import kwollect

def get_pip_version():
    from pkg_resources import get_distribution
    return tuple(int(s) for s in get_distribution("pip").version.split("."))

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kwollect",
    version=kwollect.__version__,
    author="Simon Delamare",
    author_email="simon.delamare@ens-lyon.fr",
    description="Kwollect framework for metrics collection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.inria.fr/delamare/kwollect",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pyonf",
        "psycopg2-binary==2.9.3",
        "PyJWT>=2",
        "pyyaml",
        "asyncpg",
        "aiohttp",
        "aiosnmp",
    ] + (["orjson"] if get_pip_version() >= (19, 3) else []),
    include_package_data=True,
    package_data={"kwollect": ["db/*", "grafana/*"]},
    entry_points={
        "console_scripts": [
            "kwollector = kwollect.kwollector:main",
            "kwollector-wattmetre = kwollect.kwollector_wattmetre:main",
            "kwollect-setup-db = kwollect.db.kwollect_setup_db:main",
            "kwollect-setup-db-oar = kwollect.db.kwollect_setup_db_oar:main",
        ]
    },
)
