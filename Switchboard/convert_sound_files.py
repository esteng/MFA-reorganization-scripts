import subprocess
import os
import re
import sys

SPH_REGEX = re.compile(".*\.sph$")

def convert_directory(input_dir, destination_dir):
    """
    convert the .sph sound files in input_dir to .wav in destination_dir
    checks first if there's a .textgrid for the sound file, since there are many 
    more sound files than textgrids
    """

    done = set()
    for root, dirs, files in os.walk(input_dir):
        for file in sorted(files):
            if SPH_REGEX.match(file) is not None:
                filename = os.path.join(root, file)
                if filename in done:
                    return
                
                just_name = file.split(".")[0]
                just_num = int(just_name[2:])
                
                if os.path.exists(os.path.join(output_dir, "sw"+"0"+str(just_num) +".textgrid")):
                    print(filename)
                    subprocess.call(['sox', filename, os.path.join(destination_dir, just_name + ".wav")])
                    done.update(filename)


if __name__ == '__main__':
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    convert_directory(input_dir, output_dir)