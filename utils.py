import sys


def to_name(title):
    title = title.replace('\\', ' ', sys.maxsize)
    title = title.replace('/', ' ', sys.maxsize)
    title = title.replace(':', ' ', sys.maxsize)
    title = title.replace('*', ' ', sys.maxsize)
    title = title.replace('?', ' ', sys.maxsize)
    title = title.replace('"', ' ', sys.maxsize)
    title = title.replace('<', ' ', sys.maxsize)
    title = title.replace('>', ' ', sys.maxsize)
    title = title.replace('|', ' ', sys.maxsize)

    return title
