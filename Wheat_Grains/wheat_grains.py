# Copyright © 2024 Charles Theetten
# Tous droits réservés.
#

################################################################################

""" Wheat Grains """

################################################################################

import argparse
import sys

################################################################################

def wheat_grains(nb_cases, verbose = 0):
    """ wheat_grains function """
    total = 0

    if verbose == 1:
        for i in range(0, nb_cases):
            total   += (2 ** i)
            mass    = total * 0.00000004
            print(f"{i:2} Total: {total:<30_} - Mass: {round(mass, 1):_} tons.")
    else:
        total   =  2 ** nb_cases - 1
        mass    = total * 0.00000004

    return total, mass

################################################################################

def check_args():
    """ check_args function """
    parser = argparse.ArgumentParser()

    parser.add_argument("NB_CASES", help = "values in {0... 64}.", type = int)
    parser.add_argument("VERBOSE",  help = "values in {0, 1}.", type = int)

    args = parser.parse_args()

    try:
        if args.NB_CASES not in range(0, 65):
            raise argparse.ArgumentTypeError(f"NB_CASES : {args.NB_CASES} is an invalid value.")
        if args.VERBOSE not in [0, 1]:
            raise argparse.ArgumentTypeError(f"VERBOSE : {args.VERBOSE} is an invalid value.")
    except argparse.ArgumentTypeError as e:
        print(f"Argument Error - {e}\n")
        parser.print_help()
        sys.exit(-1)

################################################################################

def main():
    """ main function """
    check_args()

    nb_cases    = int(sys.argv[1])
    verbose     = int(sys.argv[2])
    result      = wheat_grains(nb_cases, verbose)

    print("-" * 40)
    print(f"Number of grains : {result[0]:_}.")
    print(f"Mass of wheat    : {round(result[1], 1):_} tons.")
    print("-" * 40)

################################################################################

if __name__ == "__main__":
    main()

################################################################################
