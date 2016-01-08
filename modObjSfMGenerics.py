
# # #
# 1 - generic functions
# # #

def pyGrep(in1, in2):
    import re
    import sys

    file = open(in2, "r")

    for line in file:
        if re.search(sys.argv[1], line):
            print line,

def extractFloat(inputString):
    x = map(float, re.findall(r'[+-]?[0-9.]+', inputString))
    return x

def remove_values_from_list(the_list, val):
    '''  Remove the <val> from <the_list> '''
    return [value for value in the_list if value != val]

def calculate_EPSG(utmZone, south):
    """Calculate and return the EPSG"""
    if south:
        return 32700 + utmZone
    else:
        return 32600 + utmZone

def mkdir_p(path):
    '''Make a directory including parent directories.
    '''
    try:
        os.makedirs(path)
    except os.error as exc:
        if exc.errno != errno.EEXIST or not os.path.isdir(path):
            raise
        
