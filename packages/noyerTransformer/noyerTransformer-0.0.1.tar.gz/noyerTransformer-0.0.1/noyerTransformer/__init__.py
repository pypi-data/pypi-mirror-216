from .convertNoyer import run
import argparse

argparser = argparse.ArgumentParser(
    description='Convertit un fichier .tex en un fichier .md')

argparser.add_argument('input', metavar='input', type=str,
                          help='le fichier .tex à convertir')

def main():
    args = argparser.parse_args()
    run(filename=args.input)