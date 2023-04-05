from math import floor
import os
from pydub import AudioSegment
from random import choices, choice
from zipfile import ZipFile
import shutil
from tempfile import TemporaryDirectory
import tempfile
import urllib.request
import argparse

SAMPLES_PER_PAGE = 12

'''
this file will organize the sp404 for you into 10 categories.
synth and bass will each have one randomly selected sample played over a full octave.
the other 8 categories will have 12 randomly selected samples.

To use this, replace the paths in the load_* functions below !
the page ordering can also be rearranged near the bottom
'''

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')
parser.add_argument('--directory', required=False)
args = parser.parse_args()
instrument_sample_dir = "/Volumes/ssd/test"
if args.directory:
    instrument_sample_dir = args.directory    

# https://github.com/mknutsen/sp404loader/releases/download/main/sp_template.zip
template_path = None
sd_card_path = "/Volumes/SP-404SX/"
sd_card_sample_destination = "/Volumes/SP-404SX/ROLAND/IMPORT"

def detect_leading_silence(sound, silence_threshold=-50.0, chunk_size=10):
    '''
    sound is a pydub.AudioSegment
    silence_threshold in dB
    chunk_size in ms

    iterate over chunks until you find the first one with sound
    '''
    trim_ms = 0 # ms

    assert chunk_size > 0 # to avoid infinite loop
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms

def remove_leading_trailing_silence(sound):

    start_trim = detect_leading_silence(sound)
    # removing trailing silence bad? 
    return sound[start_trim:]

# unpack the template
if template_path is None:
    print("fetching SP404 template zip")
    new_path = TemporaryDirectory()
    template_path = os.path.join(str(new_path.name), "sp_template.zip")
    urllib.request.urlretrieve("https://github.com/mknutsen/sp404loader/releases/download/main/sp_template.zip", template_path)
        
with ZipFile(template_path,"r") as zip_ref, TemporaryDirectory() as temp_dir:
    
    print("Clearing SD Card")
    # get the sd card back to template status
    os.system(f"rm -r {sd_card_path}/*")
    
    print("Extracting zip template")
    zip_ref.extractall(temp_dir)

    for dirname in ["ROLAND", "BKUP"]:
        src_path = os.path.join(temp_dir, dirname)
        dest_path = os.path.join(sd_card_path, dirname)
        shutil.copytree(src=src_path, dst=dest_path)

def list_samples_in_directory(dir_name):
    for root, _, files in os.walk(dir_name, topdown=False):
        for name in files:
            file_name = os.path.join(root, name)
            if ".DS_Store" in file_name:
                continue
            if "._" in file_name:
                continue
            yield os.path.join(root, name)

def _load_choices(samples, k=SAMPLES_PER_PAGE):
    return choices(list(samples), k=k)

def load_kicks():
    folder_path = "/Volumes/ssd/test/01 kicks"
    return _load_choices(list_samples_in_directory(folder_path))

def load_snares():
    folder_path = "/Volumes/ssd/test/02 snares"
    return _load_choices(list_samples_in_directory(folder_path))

def load_hats_cymbals():
    folder_path = "/Volumes/ssd/test/03 hats & cymbals"
    return _load_choices(list_samples_in_directory(folder_path))

def load_percs_fx():
    folder_path = "/Volumes/ssd/test/04 percs & fx"
    return _load_choices(list_samples_in_directory(folder_path))

def load_loops_breaks():
    folder_path = "/Volumes/ssd/test/05 loops & breaks"
    return _load_choices(list_samples_in_directory(folder_path))

def load_808s_basses():
    # only pick one sample
    folder_path = "/Volumes/ssd/test/06 808s & basses"
    return _load_choices(list_samples_in_directory(folder_path), k=1)

def load_vox_adlibs():
    folder_path = "/Volumes/ssd/test/07 vox & adlibs"
    return _load_choices(list_samples_in_directory(folder_path))

def load_foley():
    folder_path = "/Volumes/ssd/test/08 foley"
    return _load_choices(list_samples_in_directory(folder_path))

def load_synth():
    # only pick one sample
    folder_path = "/Volumes/ssd/test/09 synth"
    x = _load_choices(list_samples_in_directory(folder_path), k=1)
    print(x)
    return x

def load_dk():
    folder_path = "/Volumes/ssd/test/00 dk"
    return _load_choices(list_samples_in_directory(folder_path))

sample_list_list = []
# each list in this list is going to be a page of samples
# they should either have 12 samples or 1 sample
# if there is one sample in the list it will be pitched 12 times 
# this ordering will be preserved

sample_list_list.append(load_kicks()) # page a
sample_list_list.append(load_snares()) # page b
sample_list_list.append(load_hats_cymbals()) # page c
sample_list_list.append(load_percs_fx()) # page d
sample_list_list.append(load_loops_breaks()) # page e
sample_list_list.append(load_synth()) # page f
sample_list_list.append(load_808s_basses()) # page g
sample_list_list.append(load_dk()) # page h
sample_list_list.append(load_foley()) # page i
sample_list_list.append(load_vox_adlibs()) # page j

sample_count = 0
def write_sample(sound):
    global sample_count
    name = f"{sample_count:03d}.wav"
    dest = os.path.join(sd_card_sample_destination, name)
    sound.export(dest, format="wav")
    sample_count += 1

for sample_list in sample_list_list:
    print(sample_list)
    if len(sample_list) == 1:
        sound = remove_leading_trailing_silence(AudioSegment.from_file(sample_list[0]))
        for index in range(0, 12):        
            # shift the pitch down by half an octave (speed will decrease proportionally)
            octaves = (1 / 12) * index
            if "06 808s & basses" in sample_list[0]:
                octaves *= -1
            new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
            lowpitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
            write_sample(lowpitch_sound)

    else:
        for sample in sample_list:
            sound = remove_leading_trailing_silence(AudioSegment.from_file(sample))
            write_sample(sound)

os.system(f"open {sd_card_sample_destination}")

