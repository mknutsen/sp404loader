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

from helper import remove_leading_trailing_silence, write_sample, load_sd_card
from main import list_samples_in_directory

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

sample_list_list.append(load_kicks())  # page a
sample_list_list.append(load_snares())  # page b
sample_list_list.append(load_hats_cymbals())  # page c
sample_list_list.append(load_percs_fx())  # page d
sample_list_list.append(load_loops_breaks())  # page e
sample_list_list.append(load_synth())  # page f
sample_list_list.append(load_808s_basses())  # page g
sample_list_list.append(load_dk())  # page h
sample_list_list.append(load_foley())  # page i
sample_list_list.append(load_vox_adlibs())  # page j

load_sd_card(sample_list_list=sample_list_list, sd_card_sample_destination=sd_card_sample_destination)

os.system(f"open {sd_card_sample_destination}")
