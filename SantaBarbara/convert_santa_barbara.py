import shutil
import os
import re
from collections import defaultdict
import textgrid as tg
import sys

def get_utterances(file, textgrid_file):
    """ 
    read utterance from .trn file and write them to textgrid format
    collapses utterances with <.15s pauses between them into 1 utterance
    textgrid tiers are based on speakers (each speaker |-> 1 tier)
    
    Parameters
    ----------
    file : str
        path to .trn file
    textgrid_file : str
        path to textgrid file
    """

    with open(file) as f1:
        lines = f1.readlines()
    
    ordered_tups = []
    speakers = defaultdict(list)
    skipped = 0
    
    for i,line in enumerate(lines):
        try:
            splitline = re.split("\t+", line)
            subsplit = re.split("\s",splitline[0])

            start = subsplit[0]
            end = subsplit[1]
            speaker = splitline[1]

            if re.match("\s+", speaker) is not None:
                speaker = ordered_tups[i-1][2]
            try:
                label = splitline[2] 
            except:
                label = ""
            
            label = re.sub("[=_%]","", label)
            speaker = re.sub("[:\s]","",speaker)
            
            ordered_tups.append( (start, end, speaker, label) )
            speakers[speaker.lower()].append( (start, end, label))
        except IndexError:
            try:
                splitline = re.split("\t+", line)

                start = splitline[0]
                end = splitline[1]
                speaker = splitline[2]
                if re.match("\s+", speaker) is not None:
                    speaker = ordered_tups[i-1][2]
                try:
                    label = splitline[2]
                except:
                    label = ""
                label = re.sub("[=_%]","", label)
                ordered_tups.append( (start, end, speaker, label) )
                speakers[speaker.lower()].append( (start, end, label))
            except IndexError:
                skipped +=1 
    speakers = clean(speakers)

    textgrid = tg.TextGrid()
    for i,speaker in enumerate(speakers.keys()):
        tier = tg.IntervalTier(name = "{}".format(speaker.strip()))
        for j, tup in enumerate(speakers[speaker]):
            try:
                if float(tup[0]) == float(tup[1]):
                    continue
            except ValueError:
                pass
            try:
                tier.add(float(tup[0]), float(tup[1]), tup[2].strip())
            except ValueError:
                try:
                    previous = tier[-1]
                except IndexError:
                    skipped +=1
                    continue
                previous_end = previous.maxTime
                difference = previous.maxTime - float(tup[0])
                if difference < 0 :
                    skipped +=1
                    continue
                if float(tup[0]) + difference == float(tup[1]):
                    skipped +=1
                    continue
                tier.add(float(tup[0]) + difference, float(tup[1]), tup[2].strip())
        if len(tier.intervals)>0:
            textgrid.append(tier)
    
    textgrid.write(textgrid_file)

    print("skipped: {}".format(skipped))

def clean(speakers):
    """
    clean the speakers dictionary
    this is where the collapsing of utterances takes place
    default boundary is .15 seconds

    Parameters
    ----------
    speakers : defaultdict(list)
        dictionary of speakers and their utterances as separated in .trn file

    Returns
    -------
    new_speakers : defaultdict(list)
        same keys as input, but the utterances for each speaker are compressed
    """

    new_speakers = defaultdict(list)
    for speaker,tups in speakers.items():
        new_tups = []
        i =1
        new_tup = list(tups[0])
        while i < len(tups):
            old_tup = list(tups[i-1])
            current_tup = list(tups[i])
            # if difference between new and old < .15 collapse
            if float(current_tup[0]) - float(old_tup[1])  < .15:
                new_tup[1] = current_tup[1] 
                new_tup[2] = new_tup[2].strip()+  " " + current_tup[2].strip()
            #otherwise add the current and start over
            else:
                new_tups.append(new_tup)
                new_tup = list(current_tup)
            i+=1

        new_speakers[speaker] = new_tups
    return new_speakers

def convert_all(source_dir, destination_dir, exclude, move_wav = False):
    """
    walk throught source dir, convert all .trn files to .textgrids
    copy wav files to destination dir
    assumes .wav and .trn files share a filename and are in the same directory

    Parameters
    ----------
    source_dir : str
        the location of .trn and .wav files
    destination_dir : str
        the desired location for the resulting textgrids/.wav files
    """

    for root, dirs, files in os.walk(source_dir, topdown = True):
        for file in files:
            if file.endswith('.trn'):
                just_name = file.split(".")[0]
                num = "".join(just_name[-3:])
                print(num)
                if str(int(num)) not in exclude:
                    if move_wav:
                        wav_name = just_name+ ".wav"
                        shutil.copy(os.path.join(root,wav_name), os.path.join(destination_dir, wav_name))
                        print('copied')
                    get_utterances(os.path.join(root,file), os.path.join(destination_dir, just_name+".textgrid"))

if __name__ == '__main__':
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    exclude = sys.argv[3].split(',')
    print(exclude)
    move_wav = sys.argv[4]
    if move_wav in ["True", True]:
        convert_all(input_dir, output_dir, exclude, True)
    else:
        convert_all(input_dir, output_dir, exclude)

    # convert_all("/Volumes/data/corpora/SantaBarbara/Part1/speech", 
    # "/Volumes/data/corpora/Santa_Barbara_textgrids/Part1")