import os


def make_struct(name, ispackage):
    os.mkdir(name)
    os.chdir(name)
    open("setup.py", "w").close()
    open("setup.cfg", "w").close()
    if ispackage:
        os.mkdir(name)
        open(name + "/__init__.py", "w").close()
    else:
        open(name+".py", "w").close()

def make_setup_cfg(name, version, author, author_email, description):
    with open("setup.cfg", "w") as fout:
        fout.write("[metadata]\n")
        fout.write("name = %s\n" % name)
        fout.write("version = %s\n" % version)
        fout.write("author = %s\n" % author)
        fout.write("author_email = %s\n" % author_email)
        fout.write("description = %s\n" % description)
def make_setup_py(name, ispackage):
    with open("setup.py", "w") as fout:
        fout.write("import setuptools\n")
        fout.write("setuptools.setup(name='%s'," % name)
        fout.write(" %s=%s)\n" % ("packages" if ispackage else "py_modules", "['"+name+"']"))