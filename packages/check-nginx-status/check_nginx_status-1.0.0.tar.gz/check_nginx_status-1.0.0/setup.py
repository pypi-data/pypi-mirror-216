import setuptools

setuptools.setup(
    name="check_nginx_status",
    python_requires=">=3.9",
    url="https://gitlab.ics.muni.cz/perun-proxy-aai/python/check_nginx_status.git",
    description="Script to check nginx status",
    include_package_data=True,
    packages=["check_nginx_status"],
    package_dir={
        "check_nginx_status": ".",
    },
    install_requires=[],
)
