"""
ComputationalArt project for Software Design Spring 2020

@author: Lilo Heinrich
"""

import random
from PIL import Image
import math

funcs = [lambda x, y: x * y, lambda x, y: (x + y)/2, lambda x, y: (x - y)/2,
        lambda x, y: math.cos(math.pi * x * y), lambda x, y: math.sin(math.pi * x * y),
        lambda x, y: math.cos(math.pi * x), lambda x, y: math.sin(math.pi * x)]
funcs0 = [lambda x, y: x, lambda x, y: y, lambda x, y: -x, lambda x, y: -y]
names = ["prod", "avg", "navg", "cosxy", "sinxy", "cosx", "sinx"]
names0 = ["x", "y", "nx", "ny"]

def build_random_function(min_depth, max_depth):
    """Builds a random function of depth at least min_depth and depth at most.

    Args:
        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function

    Returns:
        The randomly generated function represented as a nested list.
    """
    depth = random.randint(min_depth, max_depth)
    lam, name = build_random_function_helper(depth)
    return lam, name

def build_random_function_helper(depth):
    """Helper function which recurses to build a random function.

    Args:
        depth: the depth of the random function

    Returns:
        The randomly generated function represented as a nested list.
    """
    if depth == 0:
        i = random.randint(0, len(funcs0)-1)
        return funcs0[i], [names0[i]]
    elif depth > 0:
        i = random.randint(0, len(funcs)-1)
        lam1, name1 = build_random_function_helper(depth-1)
        lam2, name2 = build_random_function_helper(depth-1)
        return lambda x, y: funcs[i](lam1(x,y), lam2(x,y)), [names[i], name1, name2]

def evaluate_random_function(f, x, y):
    """Evaluate the random function f with inputs x,y.
    The representation of the function f is defined in the assignment write-up.
    Args:
        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
    Returns:
        The function value
    Examples:
        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """
    if len(f) == 3:
        x2 = evaluate_random_function(f[1], x, y)
        y2 = evaluate_random_function(f[2], x, y)

        if f[0] == names[0]:
            return x2 * y2
        elif f[0] == names[1]:
            return (x2 + y2)/2
        elif f[0] == names[2]:
            return (x2 - y2)/2
        elif f[0] == names[3]:
            return math.cos(math.pi * x2 * y2)
        elif f[0] == names[4]:
            return math.sin(math.pi * x2 * y2)
        elif f[0] == names[5]:
            return math.cos(math.pi * x2)
        elif f[0] == names[6]:
            return math.sin(math.pi * x2)
    else:
        if f[0] == names0[0]:
            return x
        elif f[0] == names0[1]:
            return y
        elif f[0] == names0[2]:
            return -x
        elif f[0] == names0[3]:
            return -y

def remap_interval(val, in_start, in_end, out_start, out_end):
    """Remap a value from one interval to another.

    Given an input value in the interval [input_interval_start,
    input_interval_end], return an output value scaled to fall within
    the output interval [output_interval_start, output_interval_end].

    Args:
        val: the value to remap
        in_start: the start of the interval that contains all
                              possible values for val
        in_end: the end of the interval that contains all possible
                            values for val
        out_start: the start of the interval that contains all
                               possible output values
        out_end: the end of the interval that contains all possible
                            output values

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
    pass

def color_map(val):
    """Maps input value between -1 and 1 to an integer 0-255, suitable for use as an RGB color code.

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

def run_color_funcs(functions, x, y, lambdas=True):
    """Applies the three color component functions to the given x, y pixel

    Args:
        functions: list of red, green, and blue functions as tuples of each in
        both the lambda and string format
        x: the x index of a given pixel in the image
        y: the y index of a given pixel in the image
        lambdas: whether to use the lambda functions or evaluate the nested list of strings

    Returns:
        Tuple of the three color component outputs on the interval [-1, 1]
    """
    list = []
    for i in range(3):
        if lambdas:
            list.append(color_map(functions[i][0](x, y)))
        else:
            list.append(color_map(evaluate_random_function(functions[i][1], x, y)))
    return tuple(list)

def generate_multi_art(filename="myart", num=1, index=0, min_depth=7, max_depth=9,
        lambdas=True, x_size=350, y_size=350, write_funcs=True, func_filename="myfunc"):
    """Generate multiple computational art and save all as sequential image files.

    Args:
        filename: string filename for image (should be .png)
        num: how many images to generate
        index: starting index to label images from
        x_size, y_size: optional args to set image dimensions (default: 350)
        min_depth, max_depth: optional args to set function depth (default: [7, 9])
        print_funcs: optional arg to print out functions in string format
        lambdas: optional arg whether to use string or lambda functions representation
    """
    for j in range(num):
        generate_art(filename+str(index+j), min_depth, max_depth, lambdas,
                x_size, y_size, write_funcs, func_filename+str(index+j))

def generate_art(filename, min_depth=7, max_depth=9, lambdas=True,
        x_size=350, y_size=350, write_funcs=True, func_filename="myfunc"):
    """Generate computational art and save as an image file.

    Args:
        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
        min_depth, max_depth: optional args to set function depth (default: [7, 9])
        print_funcs: optional arg to print out functions in string format
        lambdas: optional arg whether to use string or lambda functions representation
    """
    # Functions for red, green, and blue channels - where the magic happens!
    functions = [build_random_function(min_depth, max_depth) for i in range(3)]
    regenerate_art(filename, functions, lambdas, x_size, y_size)
    write_func(functions, func_filename)

def regenerate_art(filename, functions, lambdas=True, x_size=350, y_size=350):
    """ Generate computational art from functions and save as an image file.
    Can specify the input functions, incluing ones that were already generated
    and recorded, to recreate images

    Args:
        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
        min_depth, max_depth: optional args to set function depth (default: [7, 9])
        lambdas: optional arg whether to use string or lambda functions representation
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = run_color_funcs(functions, x, y, lambdas)
    im.save(filename+".png")

def write_func(functions, filename="myfunc"):
    file = open(filename + ".txt", "w")
    for i in range(3):
        line = str(functions[i][1])
        file.write(line+'\n')
    file.close()

def read_func(filename="myfunc"):
    file = open(filename+".txt", "r")
    lines = []
    for i in range(3):
        line = file.readline()
        lines.append(line)
    return lines

if __name__ == '__main__':
    # import doctest
    # doctest.testmod()

    # Test that PIL is installed correctly
    # test_image("noise.png")

    # Create some computational art!
    i = 0
    generate_multi_art(num=1, index=i)
    lines = read_func("myfunc"+str(i))

    # functions = [(0, ['navg', ['navg', ['navg', ['nx'], ['nx']], ['cosxy', ['y'], ['x']]], ['sinx', ['navg', ['ny'], ['x']], ['sinx', ['ny'], ['nx']]]]), (0, ['navg', ['navg', ['cosxy', ['x'], ['y']], ['avg', ['nx'], ['y']]], ['prod', ['prod', ['nx'], ['ny']], ['navg', ['ny'], ['x']]]]), (0, ['prod', ['avg', ['prod', ['nx'], ['nx']], ['cosxy', ['ny'], ['nx']]], ['cosx', ['sinx', ['nx'], ['x']], ['sinxy', ['y'], ['x']]]])]
    # regenerate_art("replica", functions, lambdas=False)
