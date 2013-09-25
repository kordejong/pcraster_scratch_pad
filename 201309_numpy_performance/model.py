#!/usr/bin/env python
import numpy
import pcraster

try:
    from PCRaster.NumPy import numpy2pcr
except ImportError:
    from pcraster import numpy2pcr


pcraster.setclone("clone.map")
nr_rows = 30000
nr_cols = 2000

numpy_types = [
    numpy.int8,
    numpy.int16,
    numpy.int32,
    numpy.int64,
    numpy.uint8,
    numpy.uint16,
    numpy.uint32,
    numpy.uint64,
    numpy.float32,
    numpy.float64
]


def create_array(
        numpy_type):
    return numpy.fromfunction(function=lambda row, col: row-row+1,
        shape=(nr_rows, nr_cols), dtype=numpy_type)


def test(
        array):
    numpy2pcr(pcraster.Scalar, array, mv=6)


if __name__ == '__main__':
    import timeit

    def name_of_type(
            numpy_type):
        return str(numpy_type)[13:-2]

    number = 3

    for numpy_type in numpy_types:
        type_name = name_of_type(numpy_type)
        nr_seconds = timeit.timeit(stmt="test(array)", number=number,
            setup=
                "import numpy;"
                "from __main__ import create_array, test;"
                "array = create_array(numpy.{})".format(type_name))
        print("{}".format(nr_seconds))
