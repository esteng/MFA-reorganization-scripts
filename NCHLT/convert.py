import xml.etree.ElementTree as ET
import re
import os
import sys
from shutil import copy, move

def read_xml(path_to_xml):
    """return dict of format: {filename: sentence}"""
    recs = {}
    tree = ET.parse(path_to_xml)
    root = tree.getroot()
    for speaker in root:
        for recording in speaker:
            audio = recording.attrib['audio'].split("/")[-1].split(".")[0]
            orth = recording.find("orth").text
            recs.update({audio:orth})

    return recs




def convert_all(lang):
    path_to_current = os.path.dirname(os.path.realpath(__file__))
    if not os.path.exists(os.path.join(path_to_current, lang)):
        os.mkdir(os.path.join(path_to_current, lang))
    audio_dir = "/Volumes/data/corpora/NCHLT/{}/audio".format(lang) 
    
    xml_dict = read_xml("/Volumes/data/corpora/NCHLT/{}/transcriptions/{}.tst.xml".format(lang, lang) )

    for folder in os.walk(audio_dir):
        for filename in folder[2]:
            abs_path = os.path.join(audio_dir, folder[0], filename)
            name = filename.split(".")[0]

            with open(os.path.join(path_to_current, lang, name+".lab"),"w")as f1:
                try:
                    # f1.write(xml_dict[name])
                    copy(abs_path, os.path.join(path_to_current, lang, filename))

                except:
                    print("issue with {}".format(abs_path))




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
    folder_regex = re.compile(".*\d{3}\w")
    for folder in os.walk(lang_dir):
        for filename in folder[2]:
            if filename.endswith(".wav") and not folder_regex.match(folder[0]):
                just_name = filename.split(".")[0]
                speaker = filename.split("_")[2]

                try:
                    print("move {} to {}".format(os.path.join(lang_dir, folder[0], filename), os.path.join(lang_dir, folder[0], speaker, filename)))
                    move(os.path.join(lang_dir, folder[0], filename), os.path.join(lang_dir, folder[0], speaker, filename))
                    move(os.path.join(lang_dir, folder[0], just_name+".lab"), os.path.join(lang_dir, folder[0], speaker, just_name+".lab"))
                except FileNotFoundError:
                    os.mkdir(os.path.join(lang_dir, folder[0], speaker))
                    print("made folder: {}".format(os.path.join(lang_dir, folder[0], speaker)))
                    move(os.path.join(lang_dir, folder[0], filename), os.path.join(lang_dir, folder[0], speaker, filename))
                    move(os.path.join(lang_dir, folder[0], just_name+".lab"), os.path.join(lang_dir, folder[0], speaker, just_name+".lab"))



make_speaker_folders("nchlt_afr")

# convert_all("nchlt_afr")    