
from os import unlink
from os.path import exists
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED


def read_strings(path, names=[], pwd=None):
    """
    Read a list of files from a zip file.
    Return a dictionary of the requested
    files and their byte strings.
    """
    items = {}
    with ZipFile(path, 'r') as zf:
        if pwd:
            zf.setpassword(pwd)
        if names == []:
            names = zf.namelist()
        for name in names:
            items[name] = zf.read(name)
    return items


def write_strings(path, items, pwd=None, compression=ZIP_DEFLATED):
    """
    Write a dictionary of strings to a zip file.
    If it already exsits, only append the new
    strings or over write what is already there.
    """
    old_items = {}
    if exists(path):
        old_items = read_strings(path)
        unlink(path)
    old_items.update(items)
    with ZipFile(path, mode='w', compression=compression) as zf:
        if pwd:
            zf.setpassword(pwd)
        for name, bytes in items.items():
            zi = ZipInfo(name)
            zi.external_attr = 0777 << 16L
            zf.write(zi, bytes)


if __name__ == "__main__":
    from sys import argv
    for name, bytes in read_strings(argv[1]).items():
        print name
        print bytes[:80]
        print 