def ask_informations():
    name = input("Name of the project: ")
    version = input("Number of version: ")
    author = input("Author: ")
    author_email = input("Author's email: ")
    description = input("Short description: ")
    ispackage = True if input("Is it a package? [yn] ") == "y" else False
    return name, version, author, author_email, ispackage, description