import fire
import re

FILES = ['circ6', 'circ8', 'circ10', 'circ12',
         'N4', 'N6', 'N8', 'N10', 'N12', 'N14']


def parse_all_files():
    for file in FILES:
        print(f"Started parsing {file}.txt")
        parseInstance(f"../instances/{file}.txt", f"../instances/{file}.dat")
        print("Done!")


def parseInstance(input_file: str = '../instances/input.txt', output_file: str = '../instances/output.dat', all_files: bool = False):
    if all_files:
        parse_all_files()
    else:
        with open(input_file, 'r') as in_file:
            input_data = [[int(n) for n in re.split(' +', l.strip())]
                          for l in in_file.readlines()]
            numTeams = len(input_data)

        with open(output_file, 'w') as out_file:
            out_file.write("data;\n")

            out_file.write(f"param numTeams := {numTeams};\n\n")

            out_file.write("param dist := \n")
            for idx_r, row in enumerate(input_data):
                for idx_c, num in enumerate(row):
                    out_file.write(
                        f"\t{idx_r + 1} {idx_c + 1} {num}\n")

            out_file.write(";\n\n")
            out_file.write("end;\n")


if __name__ == "__main__":
    fire.Fire(parseInstance)
