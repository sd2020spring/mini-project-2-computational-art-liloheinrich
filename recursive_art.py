"""
ComputationalArt project for Software Design Spring 2020

@author: Lilo Heinrich
"""

import random
from PIL import Image
import math

def_x_size, def_y_size = 350, 350
def_min_depth, def_max_depth = 7, 9
def_num_images, def_index = 1, 0
def_art_name = 'myart'
def_func_name = 'myfunc'
def_rep_name = 'recreated'
def_save = True

# arrays of the functions listed as tuples of string and lambda representation
funcs = [('prod', lambda x,y: x*y), ('avg', lambda x,y: (x+y)/2),
        ('navg', lambda x,y: (x-y)/2),
        ('cosxy', lambda x,y: math.cos(math.pi*x*y)),
        ('sinxy', lambda x,y: math.sin(math.pi*x*y)),
        ('cosx', lambda x,y: math.cos(math.pi*x)),
        ('sinx', lambda x,y: math.sin(math.pi*x)),
        ('x', lambda x,y: x), ('y', lambda x,y: y),
        ('-x', lambda x,y: -x), ('-y', lambda x,y: -y)]

def build_random_function(min_depth, max_depth):
    """Builds a random function of depth at least min_depth and at most max_depth.

    Args:
        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function

    Returns:
        The randomly generated function represented as both a lambda and
        as a nested list.
    """
    depth = random.randint(min_depth, max_depth)
    return build_random_function_helper(depth)

def build_random_function_helper(depth):
    """ Helper function which recurses to build a random function.

    Args:
        depth: the depth of the random function

    Returns:
        The randomly generated function represented both as a lamda and
        as a nested list.
    """
    random_index = random.randint(0, len(funcs)-1)
    if depth == 0:
        return [funcs[random_index][0]], funcs[random_index][1]
    elif depth > 0:
        name1, lam1 = build_random_function_helper(depth-1)
        name2, lam2 = build_random_function_helper(depth-1)

        name_func = [funcs[random_index][0], name1, name2]
        lam_func = lambda x, y: funcs[random_index][1](lam1(x,y), lam2(x,y))
        return name_func, lam_func

def evaluate_random_function(f, x, y, lambdas):
    """Evaluate the random function f with inputs x,y.
    The representation of the function f is defined in the assignment write-up.

    Args:
        f: function to evaluate as either the list and lambda form
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        lambdas: boolean whether to use lambda or list form of functions

    Returns:
        The function value

    Examples:
        >>> evaluate_random_function(['x'],-0.5, 0.75, False)
        -0.5
        >>> evaluate_random_function(['y'],0.1,0.02, False)
        0.02
        >>> evaluate_random_function(['-y'],0.5,1.0, False)
        -1.0
        >>> evaluate_random_function(['prod'],0.25,0.5, False)
        0.125
        >>> evaluate_random_function((lambda x,y: (x+y)/2),0.25,0.5, True)
        0.375
    """
    if lambdas:
        return f(x, y)

    if len(f) == 3:
        x2 = evaluate_random_function(f[1], x, y, lambdas)
        y2 = evaluate_random_function(f[2], x, y, lambdas)

        for i in range(len(funcs)):
            if f[0] == funcs[i][0]:
                return funcs[i][1](x2, y2)
    else:
        for i in range(len(funcs)):
            if f[0] == funcs[i][0]:
                return funcs[i][1](x, y)

def remap_interval(val, in_start, in_end, out_start, out_end):
    """Remap a value from one interval to another.
    Given an input value in the interval [input_interval_start,
    input_interval_end], return an output value scaled to fall within
    the output interval [output_interval_start, output_interval_end].

    Args:
        val: the value to remap
        in_start: start of the interval that contains all possible values for val
        in_end: end of the interval that contains all possible values for val
        out_start: start of the interval that contains all possible output values
        out_end: end of the interval that contains all possible output values

    Returns:
        The value remapped from the input to the output interval

    Examples:
        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
        >>> remap_interval(127.5, 0, 255, 0, 1)
        0.5
    """
    in_range = in_end-in_start
    out_range = out_end-out_start
    return (val-in_start)/in_range*out_range+out_start

def color_map(val):
    """Maps input value between -1 and 1 to an integer 0-255,
    suitable for use as an RGB color code.

    Args:
        val: value to remap, must be a float in the interval [-1, 1]

    Returns:
        An integer in the interval [0,255]

    Examples:
        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)

def test_image(filename, x_size=def_x_size, y_size=def_y_size):
    """Generate a test image with random pixels and save as an image file.

    Args:
        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel
    im.save(filename)

def generate_multi_art(filename=def_art_name, min_depth=def_min_depth, max_depth=def_max_depth,
        x_size=def_x_size, y_size=def_y_size, write_funcs=def_save,
        func_filename=def_func_name, num_images=def_num_images, index=def_index):
    """Generate multiple computational art and save all as sequential image files.

    Args:
        filename: optional arg filename for image (default: "myart")
        min_depth, max_depth: optional args to set function depth (default: [7, 9])
        x_size, y_size: optional args to set image dimensions (default: 350)
        write_funcs: optional arg to print out functions in string format,
                default is True because they are useful
        func_filename: optional arg filename for function (default: "myfunc")
        num_images: optional arg how many images to generate, (default: 1)
        index: starting index to label images from, (default: 0)
    """
    for j in range(num_images):
        generate_art(filename+str(index+j), min_depth, max_depth,
                x_size, y_size, write_funcs, func_filename+str(index+j))

def generate_art(filename=def_art_name, min_depth=def_min_depth, max_depth=def_max_depth,
        x_size=def_x_size, y_size=def_y_size, write_funcs=def_save, func_filename=def_func_name):
    """Generate computational art and save as an image file. Optionally save
    the corresponding function file.

    Args:
        filename: optional arg filename for image (default: "myart")
        min_depth, max_depth: optional args to set function depth (default: [7, 9])
        lambdas: optional arg whether to use lambda functions (default: False)
        x_size, y_size: optional args to set image dimensions (default: 350)
        write_funcs: optional arg to print out functions in string format
        func_filename: optional arg filename for function (default: "myfunc")
    """
    # Functions for red, green, and blue channels - where the magic happens!
    name_funcs = []
    lam_funcs = []
    for i in range(3):
        functions = build_random_function(min_depth, max_depth)
        name_funcs.append(functions[0])
        lam_funcs.append(functions[1])

    # generate art always uses lambdas because they are faster, while regenerate
    # art requrires use of nested lists, leading to this fixed 'True' value to specify
    make_art(lam_funcs, filename, True, x_size, y_size)
    write_func(name_funcs, func_filename)

def make_art(functions, filename, lambdas, x_size=def_x_size, y_size=def_y_size):
    """ Generate computational art from functions and save as an image file. Can
    specify the input functions, including ones that were already generated and
    recorded, to recreate images.

    Args:
        functions: the array of three sets of functions to recreate the image from
        filename: optional arg string filename for image (default: "recreated")
        lambdas: optional arg whether to use lambda functions (default: False)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (color_map(evaluate_random_function(functions[0], x, y, lambdas)),
                            color_map(evaluate_random_function(functions[1], x, y, lambdas)),
                            color_map(evaluate_random_function(functions[2], x, y, lambdas)))
    im.save(filename+".png")

def regenerate_art(filename=def_rep_name, x_size=def_x_size,
        y_size=def_y_size, func_filename=def_func_name, index=def_index):
    """ Generate computational art from text file of the nested list representation
    of functions and save as an image file. Can specify the input functions,
    including ones that were already generated and recorded, to recreate images.

    Args:
        functions: the array of three sets of functions to recreate the image from
        filename: optional arg string filename for image (default: "recreated")
        x_size, y_size: optional args to set image dimensions (default: 350)
        func_filename: optional arg filename to read from (default: "myfunc")
        index: the number added to the filename (default: 0)
    """
    functions = read_func(func_filename, index)
    make_art(functions, filename, False, x_size, y_size)

def write_func(functions, filename=def_func_name):
    """ Writes the functions given as strings into a text file.

    Args:
        functions: the functions, in terms of an array of them in nested list format
        filename: the file name under which to save the functions (default: "myfunc")
    """
    file = open(filename + ".txt", "w")
    for i in range(3):
        line = str(functions[i])
        file.write(line+'\n')
    file.close()

def read_func(filename=def_func_name, index=def_index):
    """ Reads in lines from a function file, returning the nested list
    representation of one function.

    Args:
        filename: optional arg filename to read from (default: "myfunc")
        index: the number added to the filename (default: 0)

    Returns:
        functions: array of nested list representation of three functions
    """
    file = open(filename+str(index)+".txt", "r")
    functions = []
    for i in range(3):
        line = file.readline()
        line = line.replace('\'', '').strip()
        functions.append(parse_line(line))
    return functions

def parse_line(line):
    """ Takes in one line as a string from a function file, parses it into tokens,
    and reconstructs the original nested list using a helper function.

    Args:
        line: a string of one line of a function file

    Returns:
        list: the nested list version of line
    """
    tok = line.replace('[', '').replace(']', '').split(', ')
    list = [tok[0]]
    tok = tok[1:]
    temp = list
    parse_line_helper(temp, tok)
    return list

def parse_line_helper(arr, tok):
    """ Modifies the nested list that is referenced through the parameter arr to
    repopulate the nested list with the tokens given using recursive backtracking.
    Does not return anything, instead modifying sections of the tree through arr.

    Args:
        arr: the array of the level on the tree, starting at the top and moving down
        tok: an array of tokens such as 'avg' which represent the building block functions
    """
    arr.append([tok[0]])
    arr.append([tok[(len(tok)-1)//2+1]])
    del tok[(len(tok)-1)//2+1]
    del tok[0]
    if len(tok) > 2:
        parse_line_helper(arr[1], tok[0:(len(tok)-1)//2+1])
        parse_line_helper(arr[2], tok[(len(tok)-1)//2+1:])


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Test that PIL is installed correctly
    test_image("noise.png")

    # Create some computational art
    generate_multi_art(num_images=3)
    print('images created')

    # Recreate the art from a function file. This still takes a long time unfortunately
    regenerate_art(index=1) # says to recreate image at default filename + index 1
    print('image regenerated')
