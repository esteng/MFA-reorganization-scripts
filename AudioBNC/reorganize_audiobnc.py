import os
import re
import sys
from shutil import copyfile

new_dir = "/Volumes/data/corpora/AudioBNC/AudioBNC/"
c = 0
for root,dirs,files in os.walk("/Volumes/data/corpora/AudioBNC/AudioBNCTextGrids_for_PG/"):
    for file in files:
        if file.endswith(".wav"):
            filename = file.split(".")[0]
            c+=1
            # for tg_file in files:
            #     if filename in tg_file and tg_file.endswith(".TextGrid"):
            #         try:
            #             os.rename(os.path.join(root,file), os.path.join(new_dir, file))
            #         except FileNotFoundError:
            #             print("wav not found", filename)
            #         try:
            #             new_tg_filename = filename + ".TextGrid"
            #             os.rename(os.path.join(root,tg_file), os.path.join(new_dir, new_tg_filename))

            #         except FileNotFoundError:
            #             print("textgrid not found", filename)

print("left over: ",c)