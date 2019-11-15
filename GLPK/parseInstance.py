import fire
import re

def parseInstance(input_file, output_file: str = '../instances/output.dat'):
    with open(input_file, 'r') as in_file:
        with open(output_file, 'w') as out_file:
            input_data = [[int(n) for n in re.split(' +', l.strip())] for l in in_file.readlines()]
            T_size = len(input_data)

            out_file.write("data;\n")
            out_file.write(f"param T_size := {T_size}\n\n")
            out_file.write("param dist :=\n")

            for idx_r, row in enumerate(input_data):
                for idx_c, num in enumerate(row):
                    out_file.write(f"\t{idx_r + 1} {idx_c + 1} {num}\n")
            
            out_file.write("\nend;")


            

if __name__ == "__main__":
    fire.Fire(parseInstance)