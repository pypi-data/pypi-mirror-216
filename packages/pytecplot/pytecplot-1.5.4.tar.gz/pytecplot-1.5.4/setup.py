from setuptools import setup
import struct


if __name__ == '__main__':
    pointer_size = struct.calcsize('P')
    if pointer_size != 8:
        err = '{} bit architecture detected.\n'.format(pointer_size * 8)
        err += 'PyTecplot must be used with a 64-bit version of Python.'
        raise Exception(err)

    setup()
