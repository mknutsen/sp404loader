from math import floor
import os
from pydub import AudioSegment
from random import choices, choice
from zipfile import ZipFile
import shutil
from tempfile import TemporaryDirectory
import tempfile
import urllib.request
instrument_sample_dir = "/Volumes/ssd/test"
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

def select_samples():
    dir_names = [dirname for dirname in os.listdir(instrument_sample_dir) if "._" not in dirname]
    print("dir names", dir_names)
    # sp404 has 120 sample slots
    samples_per = floor(120 / len(dir_names))
    leftovers = 120 % len(dir_names)
    leftovers_list = choices(dir_names, k=leftovers)

    # want the leftover list to not have duplicates
    def leftover_needed(name):
        return name in leftovers_list
    
    samples_selected = []

    for dir_name in dir_names:
        dir_path = os.path.join(instrument_sample_dir, dir_name)
        k = samples_per
        if leftover_needed(dir_name):
            k += 1
        samples_selected += choices(list(list_samples_in_directory(dir_path)), k=k)

    print("num samples: ", len(samples_selected))
    return samples_selected
    
sample_list =  list(select_samples())

for index, sample in enumerate(sorted(sample_list)):
    dest = os.path.join(sd_card_sample_destination, f"{index:03d}.wav")
    print(sample, f"{index:03d}.wav")

    # need to convert to wav
    sound = remove_leading_trailing_silence(AudioSegment.from_file(sample))
    sound.export(dest, format="wav")

os.system(f"open {sd_card_sample_destination}")

