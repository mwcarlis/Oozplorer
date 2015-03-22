""" Insert docstring here

- Matthew Carlis
- Chris Nguyen
- Shunt Balushian
"""
import sys


def run_game(number):
    """
    Args:
        number (int): The integer 
    """
    pass


def parse_arguments(arguments):
    """ 
    Args: 
        arguments (list): sys.argv object.
    Returns:
        number (int): The integer command line argument.
    """
    def bail_out():
        print 'Invalid Command line arguments.  Use Integers only.'
        sys.exit(1)
    try:
        number = int(arguments[1])
    except IndexError:
        bail_out()
    except ValueError:
        bail_out()
    return number


if __name__ == '__main__':
    ARGS = sys.argv
    NUMBER = parse_arguments(ARGS)
    run_game(NUMBER)
    print NUMBER
