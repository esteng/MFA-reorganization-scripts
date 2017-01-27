import xml.etree.ElementTree as ET
import re
import os
import sys
from shutil import copy, move

def read_xml(path_to_xml):
    """return dict of format: {filename: sentence}"""

    print("path to XML is : ",path_to_xml)
    recs = {}
    tree = ET.parse(path_to_xml)
    root = tree.getroot()
    for speaker in root:
        for recording in speaker:
            audio = recording.attrib['audio'].split("/")[-1].split(".")[0]
            
            orth = recording.find("orth").text

            recs.update({audio:orth})

    return recs




def convert_all(lang, method):
    path_to_current = os.path.dirname(os.path.realpath(__file__))
    if not os.path.exists(os.path.join(path_to_current, lang)):
        os.mkdir(os.path.join(path_to_current, lang))
    audio_dir = "/Volumes/data/corpora/NCHLT/{}/audio".format(lang) 
    folder_regex = re.compile(".*\d{3}\w")
    
    if method == "train":
        suff = "trn"
    else:
        print("in test")
        suff = "tst"

    print("reading {}".format("/Volumes/data/corpora/NCHLT/{}/transcriptions/{}.{}.xml".format(lang, lang, suff)))
    xml_dict = read_xml("/Volumes/data/corpora/NCHLT/{}/transcriptions/{}.{}.xml".format(lang, lang, suff) )


    if not os.path.exists(os.path.join(path_to_current, lang, method)):
        os.mkdir(os.path.join(path_to_current, lang, method))

    for folder in os.walk(audio_dir):
        for filename in folder[2]:
            abs_path = os.path.join(audio_dir, folder[0], filename)
            name = filename.split(".")[0]
            if filename.endswith(".wav") and not folder_regex.match(folder[0]):
                just_name = filename.split(".")[0]
                speaker = filename.split("_")[2]
            if just_name in xml_dict.keys():
                try:
                    print("move {} to {}".format(abs_path,  os.path.join(path_to_current, lang, speaker, filename)))
                    copy(abs_path, os.path.join(path_to_current, lang, speaker, filename))

                except FileNotFoundError:
                    print("{} not found ".format(os.path.join(path_to_current, lang, speaker, filename)))
                    if not os.path.exists(os.path.join(path_to_current, lang, method, speaker)):
                        os.mkdir(os.path.join(path_to_current, lang, method, speaker))
                    print("made folder: {}".format(os.path.join(path_to_current, lang, method, speaker)))
                    copy(abs_path, os.path.join(path_to_current, lang, method, speaker, filename))
                with open(os.path.join(path_to_current, lang, method, speaker, name+".lab"),"w") as f1:
                    f1.write(xml_dict[name])
          




def reset(lang):
    audio_dir = "/Volumes/data/corpora/NCHLT/{}/audio/".format(lang) 
    path_to_current = os.path.dirname(os.path.realpath(__file__))
    for folder in os.walk(path_to_current):
        for filename in folder[2]:
            if filename.endswith(".wav"):
                splitname = filename.split("_")
                foldername = splitname[2][:-1]
                print(foldername)
                copy(os.path.join(path_to_current, lang, filename), audio_dir+foldername)


def make_speaker_folders(lang):
    path_to_current = os.path.dirname(os.path.realpath(__file__))
    lang_dir = os.path.join(path_to_current, lang)
    
    for folder in os.walk(lang_dir):
        for filename in folder[2]:
            if filename.endswith(".wav") and not folder_regex.match(folder[0]):
                just_name = filename.split(".")[0]
                speaker = filename.split("_")[2]

                
convert_all(sys.argv[1], sys.argv[2])
# make_speaker_folders("nchlt_eng")

# convert_all("nchlt_afr")    