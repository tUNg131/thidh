import minify_html
import argparse

parser = argparse.ArgumentParser(description="Minify HTML files.")
parser.add_argument('-i')
parser.add_argument('-o')
args = vars(parser.parse_args())

with open(args['i'], 'r') as input:
    input_str = input.read()
    minified = minify_html.minify(input_str)
    with open(args['o'], 'w') as output:
        output.write(minified)