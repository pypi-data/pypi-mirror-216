import setuptools

setuptools.setup(
    name="setupdoc",
    install_requires=["setuptools"],
    packages=['setupdoc'],
    entry_points={"console_scripts": ['setupdoc = setupdoc.__main__:main']}
    )