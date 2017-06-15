import os
import re
import textgrid as tg
import sys 
annotation_types = ["phone","word","mute","Errors"]

num_gex = re.compile("^\d+\.\d+$")
header1_gex = re.compile("File type =.*")
header2_gex = re.compile('"TextGrid".*')
existence_gex = re.compile("<exists>")
single_num_gex = re.compile("^\d$")
interval_tier_gex = re.compile('^"IntervalTier"$')
annotation_type_gex = re.compile("|".join(annotation_types))

fixed_path="/Volumes/data/corpora/AudioBNC/AudioBNCTextGrids_for_PG/"

def fix_tg(path, filename):
    """ 
    original tgs have no xmin, xmax labels
    convert them to real textgrids, readable by the textgrid module
    Parameters
    ----------
    path: str
        path to the original textgrid
    filename: str
        desired name for the new textgrid
    """
    with open(path) as f1:
        lines = f1.readlines()


    textgrid = tg.TextGrid()
    i = 7

    while i<len(lines):
        if interval_tier_gex.match(lines[i]):
            if i > 10 and len(tier) > 0:
                textgrid.append(tier)
            tier = tg.IntervalTier(name = "A - " + re.sub('"', '', lines[i+1].strip()))
            i += 5
        else:
            try:
                tier.add(float(lines[i]), float(lines[i+1]), re.sub('"', '', lines[i+2].strip()))
                i+=3
            except ValueError:
                difference = float(lines[i-2])-float(lines[i])
                if difference < .00001:
                    tier.add(float(lines[i])+difference, float(lines[i+1]), re.sub('"', '', lines[i+2].strip()))
                    i+=3
                else:
                    i+=3

    textgrid.write(os.path.join(fixed_path,filename))

 




if __name__ == '__main__':
    already_done  = set()
    # don't do textgrids twice
    for root, dirs, files in os.walk("/Volumes/data/corpora/AudioBNC/AudioBNCTextGrids_for_PG/"):
        already_done |= set(files)


    for root, dirs, files in os.walk("/Volumes/data/corpora/AudioBNC/AudioBNCTextGrids/"):
        for file in files:
            if file.endswith(".TextGrid") and file not in already_done:
                path = os.path.join(root, file)
                # try:
                print(path)
                fix_tg(path, file)
                # except ValueError:
                    # print(os.path.join(path, file))