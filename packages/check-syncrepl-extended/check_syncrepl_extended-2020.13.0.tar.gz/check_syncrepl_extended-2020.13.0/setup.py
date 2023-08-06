import setuptools

setuptools.setup(
    name="check_syncrepl_extended",
    python_requires=">=3.9",
    url="https://gitlab.ics.muni.cz/perun-proxy-aai/python/check_syncrepl_extended.git",
    description="Script to check LDAP syncrepl replication state between two servers",
    include_package_data=True,
    packages=["check_syncrepl_extended"],
    package_dir={
        "check_syncrepl_extended": ".",
    },
    install_requires=["python-ldap~=3.4"],
)
