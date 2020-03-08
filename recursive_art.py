"""
ComputationalArt project for Software Design Spring 2020

@author: Lilo Heinrich
"""

import random
from PIL import Image
import math

funcs0 = [('x', (lambda x, y: x)), ('y', (lambda x, y: y)),
        ('-x', (lambda x, y: -x)), ('-y', (lambda x, y: -y))]
funcs = [('prod', (lambda x, y: x*y)),
        ('avg', (lambda x, y: (x+y)/2)),
        ('navg', (lambda x, y: (x-y)/2)),
        ('cosxy', (lambda x, y: math.cos(math.pi*x*y))),
        ('sinxy', (lambda x, y: math.sin(math.pi*x*y))),
        ('cosx', (lambda x, y: math.cos(math.pi*x))),
        ('sinx', (lambda x, y: math.sin(math.pi*x)))]

def build_random_function(min_depth, max_depth):
    """Builds a random function of depth at least min_depth and depth at most.
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
    """Helper function which recurses to build a random function.
    Args:
        depth: the depth of the random function
    Returns:
        The randomly generated function represented both as a lamda and
        as a nested list.
    """
    if depth == 0:
        i = random.randint(0, len(funcs0)-1)
        return funcs0[i][1], [funcs0[i][0]]
    elif depth > 0:
        i = random.randint(0, len(funcs)-1)
        lam1, name1 = build_random_function_helper(depth-1)
        lam2, name2 = build_random_function_helper(depth-1)
        return lambda x, y: funcs[i][1](lam1(x,y), lam2(x,y)), [funcs[i][0], name1, name2]

def evaluate_random_function(f, x, y, lambdas=True):
    """Evaluate the random function f with inputs x,y.
    The representation of the function f is defined in the assignment write-up.
    Args:
        f: the function to evaluate, represented as both a nested list and lambda
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        lambdas: whether to use lambda or list form of functions
    Returns:
        The function value
    Examples:
        >>> evaluate_random_function((None, ["x"]),-0.5, 0.75, False)
        -0.5
        >>> evaluate_random_function((None, ["y"]),0.1,0.02, False)
        0.02
        >>> evaluate_random_function((None, ["-y"]),0.5,1.0, False)
        -1.0
    """
    if lambdas:
        return f[0](x, y)
    elif f[0] == None:
        f = f[1]

    if len(f) == 3:
        x2 = evaluate_random_function(f[1], x, y, lambdas)
        y2 = evaluate_random_function(f[2], x, y, lambdas)

        for i in range(len(funcs)):
            if f[0] == funcs[i][0]:
                return funcs[i][1](x2, y2)
    else:
        for i in range(len(funcs0)):
            if f[0] == funcs0[i][0]:
                return funcs0[i][1](x, y)

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

def test_image(filename, x_size=350, y_size=350):
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

def generate_multi_art(filename="myart", num_images=1, index=0, min_depth=7, max_depth=9,
        lambdas=True, x_size=350, y_size=350, write_funcs=True, func_filename="myfunc"):
    """Generate multiple computational art and save all as sequential image files.
    Args:
        filename: optional arg filename for image (default: "myart")
        num_images: optional arg how many images to generate
        index: starting index to label images from
        min_depth, max_depth: optional args to set function depth (default: [7, 9])
        lambdas: optional arg whether to use string or lambda functions representation
        x_size, y_size: optional args to set image dimensions (default: 350)
        write_funcs: optional arg to print out functions in string format
        func_filename: optional arg filename for function (default: "myfunc")
    """
    for j in range(num_images):
        generate_art(filename+str(index+j), min_depth, max_depth, lambdas,
                x_size, y_size, write_funcs, func_filename+str(index+j))

def generate_art(filename="myart", min_depth=7, max_depth=9, lambdas=True,
        x_size=350, y_size=350, write_funcs=True, func_filename="myfunc"):
    """Generate computational art and save as an image file.
    Args:
        filename: optional arg filename for image (default: "myart")
        min_depth, max_depth: optional args to set function depth (default: [7, 9])
        lambdas: optional arg whether to use string or lambda functions representation
        x_size, y_size: optional args to set image dimensions (default: 350)
        write_funcs: optional arg to print out functions in string format
        func_filename: optional arg filename for function(default: "myfunc")
    """
    # Functions for red, green, and blue channels - where the magic happens!
    functions = [build_random_function(min_depth, max_depth) for i in range(3)]
    regenerate_art(functions, filename, lambdas, x_size, y_size)
    write_func(functions, func_filename)

def regenerate_art(functions, filename="recreated", lambdas=False, x_size=350, y_size=350):
    """ Generate computational art from text file of the nested list representation
    of functions and save as an image file. Can specify the input functions,
    including ones that were already generated and recorded, to recreate images
    Args:
        functions: the functions to recreate the image of
        filename: string filename for image (default: "recreated")
        lambdas: optional arg whether to use string or lambda functions representation
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

def write_func(functions, filename="myfunc"):
    """ Writes functions into a text file
    Args:
        functions: the functions, in terms of tuples of lambda and nested list format
        filename: the file name nder which to save the functions
    """
    file = open(filename + ".txt", "w")
    for i in range(3):
        line = str(functions[i][1])
        file.write(line+'\n')
    file.close()

def read_func(filename="myfunc", index=0):
    """ Reads in lines from a function file, returning the nested list
    representation of one function
    Args:
        filename: optional arg filename to read from (default: "myfunc")
        index: the number added to the filename (default: 0)
    Returns:
        functions: nested list representation of a function
    """
    file = open(filename+str(index)+".txt", "r")
    functions = []
    for i in range(3):
        line = file.readline()
        line = line.replace('\'', '').strip()
        functions.append((None, parse_line(line)))
    return functions

def assemble_line(line):
    """ Helper function assembling a list of all the function blocks from the
    lowest level of the tree.
    Args:
        line: string representation of the top n levels of the tree function
    Returns:
        n: a list of the function blocks on the lowest level of the tree
    """
    stack = []
    n = []
    count = 0
    i = 0
    while i < len(line):
        if line[i] == '[':
            stack.append(i)
            prev = False
            count = 0
        elif line[i] == ']' and count < 1:
            j = stack.pop()
            n.append([line[j+1:i]])
            line = line[0:j-2] + line[i+1:]
            i = j-2
            count += 1
        i += 1
    return line, n

def parse_line(line):
    """ Takes the function in string form and reintegrates
    it into the nested list representation.
    Args:
        l: string of one line from a function text file
    Returns:
        n: nested list representation of the function specified in string l
    """
    line, n = assemble_line(line)
    while ']' in line:
        line, n2 = assemble_line(line)
        for i in range(len(n2)):
            n2[i].append(n[2*i])
            n2[i].append(n[2*i+1])
        n = n2
    return n[0]

if __name__ == '__main__':
    # import doctest
    # doctest.testmod()

    # Test that PIL is installed correctly
    # test_image("noise.png")

    # Create some computational art!
    generate_multi_art(num_images=3)
    print('images created')

    # Recreate the art from the function files
    functions = read_func(index=1)
    regenerate_art(functions)
    print('image regenerated')
