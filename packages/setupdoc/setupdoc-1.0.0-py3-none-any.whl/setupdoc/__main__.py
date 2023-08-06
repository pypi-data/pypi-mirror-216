# -*- coding: utf-8 -*-

from setupdoc import ui, generators

def main():
    name,version,author,author_email,ispackage,description = ui.ask_informations()
    generators.make_struct(name, ispackage)
    generators.make_setup_cfg(name, version, author, author_email, description)
    generators.make_setup_py(name, ispackage)

if __name__ == "__main__":
    main()