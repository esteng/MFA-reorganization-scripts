import re
import urllib.request
import os
import subprocess
import sys
import time

"""
scrape the audio off of the audioBNC webpage
"""

def get_one_file(url, dest):
    if urllib.request.urlretrieve(url, dest):
        return 1
    return 0


with open("/Volumes/data/corpora/AudioBNC/wavs/filelist-wav.txt") as f1:
    files = list(map(lambda x: x.strip(), f1.readlines()))
with open("finished.txt") as f1:
    done = set(map(lambda x: x.strip(), f1.readlines()))

dest_path = "/Volumes/data/corpora/AudioBNC/wavs/"
url_start = "http://bnc.phon.ox.ac.uk/data/"
# get_one_file("http://bnc.phon.ox.ac.uk/data/021A-C0897X0189XX-AAZZP0.wav", "/Volumes/data/corpora/AudioBNC/wavs/021A-C0897X0189XX-AAZZP0.wav")
with open("finished.txt","a+") as f2:
    num_processed = 0
    t0 = time.time()
    for i,file in enumerate(files):
        wav_name = file
        if wav_name not in done:
            url = wav_name
            filename = url.split("/")[-1]
            f2.write(url+"\n")
            dest = os.path.join(dest_path, filename)
            try:
                num_processed += get_one_file(url, dest)
            except:
                print("error on ", url)
                f2.write("error: "+ url)
                continue
            
        if i%10 == 0:
            print("finished {} percent, took: {}".format(float(i)/float(len(files)), time.time()-t0))
            t0 = time.time()
            if i> 0:
                print("processed {} out of {}".format(num_processed+len(done), len(files)))