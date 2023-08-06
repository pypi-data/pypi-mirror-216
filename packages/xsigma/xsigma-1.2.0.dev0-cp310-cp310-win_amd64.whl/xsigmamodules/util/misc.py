"""Miscellaneous functions and classes that don't fit into specific
categories."""

import sys, os

# ----------------------------------------------------------------------
# the following functions are for the xsigma regression testing and examples


def xsigmaGetDataRoot():
    """xsigmaGetDataRoot() -- return xsigma example data directory"""
    dataRoot = None
    for i, argv in enumerate(sys.argv):
        if argv == "-D" and i + 1 < len(sys.argv):
            dataRoot = sys.argv[i + 1]

    if dataRoot is None:
        dataRoot = os.environ.get("XSIGMA_DATA_ROOT", "../../../../XSIGMAData")

    return dataRoot


def xsigmaGetTempDir():
    """xsigmaGetTempDir() -- return xsigma testing temp dir"""
    tempDir = None
    for i, argv in enumerate(sys.argv):
        if argv == "-T" and i + 1 < len(sys.argv):
            tempDir = sys.argv[i + 1]

    if tempDir is None:
        tempDir = "."

    return tempDir
