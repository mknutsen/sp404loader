import os
from pydub import AudioSegment
from random import choice
from zipfile import ZipFile
import shutil
from tempfile import TemporaryDirectory
instrument_sample_dir = "/Volumes/Hi/Dropbox/ableton_workspace/sample/instrument_samples/"
template_path = f"{os.path.dirname(__file__)}/sp_template.zip"
sd_card_path = "/Volumes/SP-404SX/"
sd_card_sample_destination = "/Volumes/SP-404SX/ROLAND/IMPORT"
print(template_path)
"""
assembles a memory card for the Roland SP404-SX/A
120 Samples are selected from a list of samples. Based on discernable charicteristics from the file name, we can change how we sort and filter.
parsing the name of the sample yields one or many of these charicteristics 
Intonations used: {'', 'arco-sul-ponticello', 'shaken', 'natural-harmonic', 'arco-glissando', 'staccatissimo', 'tremolo', 'non-vibrato', 'bass-drum-mallet', 'pizz-tremolo', 'minor-trill', 'glissando', 'arco-minor-trill', 'arco-portato', 'pizz-glissando', 'arco-legato', 'medium-sticks', 'arco-normal', 'harmonic-glissando', 'clean', 'arco-au-talon', 'fla', 'arco-col-legno-battuto', 'sticks', 'damped', 'vibe-mallet-undamped', 'harmonic', 'major-trill', 'undamped', 'harmonics', 'struck-together', 'without-snares', 'rhyth', 'roll', 'arco-major-trill', 'arco-spiccato', 'staccato', 'effect', 'arco-tremolo', 'arco-sul-tasto', 'double-tonguing', 'arco-harmonic', 'slap-tongue', 'nonlegato', 'tongued-slur', 'molto-vibrato', 'mute', 'hand', 'rute', 'body', 'arco-tenuto', 'arco-staccato', 'arco-col-legno-tratto', 'triple-tonguing', 'fluttertonguing', 'subtone', 'arco-martele', 'squeezed', 'snap-pizz', 'rimshot', 'artificial-harmonic', "arco-punta-d'arco", 'legato', 'tenuto', 'arco-detache', 'pizz-normal', 'struck-singly', 'with-snares', 'scraped', 'vibrato', 'pizz-quasi-guitar', 'con-sord', 'normal'}
Strength: {'pianissimo', 'mezzo-piano', 'molto-pianissimo', 'mezzo-forte', 'crescendo', 'forte', 'fortissimo', 'cresc-decresc', 'decrescendo', 'piano'}
Length: {'very-long', 'phrase', 'long', '15', '025', '05', '1'}
Note: {'', 'B2', 'Fs2', 'F7', 'As0', 'As3', 'G4', 'E2', 'Ds4', 'D6', 'C7', 'Gs3', 'Gs2', 'Fs3', 'D2', 'As1', 'Cs7', 'C4', 'As6', 'G3', 'Gs6', 'Gs7', 'D4', 'F3', 'Fs6', 'G5', 'B3', 'B6', 'Ds3', 'A1', 'B1', 'Fs7', 'G7', 'A3', 'E8', 'D3', 'B4', 'B0', 'F1', 'Cs1', 'E4', 'Gs1', 'C8', 'As2', 'D5', 'B7', 'Cs2', 'E1', 'D7', 'F2', 'A4', 'B5', 'F5', 'As5', 'Ds5', 'G2', 'Ds7', 'A2', 'Gs5', 'Cs6', 'A7', 'As7', 'G1', 'Fs5', 'E7', 'Cs5', 'Gs4', 'A5', 'E3', 'C6', 'Ds2', 'D1', 'E5', 'F6', 'G6', 'F4', 'E6', 'Cs3', 'Fs1', 'C2', 'Ds6', 'As4', 'C1', 'Fs4', 'C3', 'Ds1', 'Cs4', 'A6', 'C5'}
'struck-singly', 'with-snares', 'scraped', 'fortissimo', 'bass-drum-mallet','fla','clean','medium-sticks','sticks', 'damped','vibe-mallet-undamped', 'harmonic', 'major-trill','undamped', 'struck-together', 'without-snares', 'rhyth', 'roll', 'arco-major-trill', 'effect',  'squeezed', 'snap-pizz', 'rimshot', 'artificial-harmonic', 'struck-singly', 'with-snares', 'scraped', 'vibrato','normal'
The samples are also trimmed and formatted to wav
The SD card is erased and the template is replaced. When booting the sp 404 hit import all and it will auto load the samples into the banks.
"""
''''''
desired_note = "C"
scale_range = [1, 2, 3, 4, 5]

full_path_list = [os.path.join(instrument_sample_dir, x) for x in os.listdir(instrument_sample_dir)]
all_dir_list = [x for x in full_path_list if os.path.isdir(x)]
non_dup_list = [x for x in all_dir_list if not " " in x]
# print(non_dup_list)

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
    end_trim = detect_leading_silence(sound.reverse())

    duration = len(sound)    
    return sound[start_trim:duration-end_trim]

class Sample:
    def __init__(self, file_path, instrument_name, note, length, strength, intonation):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path).strip(".mp3")
        self.instrument_name = instrument_name
        self.note = note
        self.length = length
        self.strength = strength
        self.used = False
        self.intonation = intonation if intonation else "empty"

    def __str__(self):
        return f"instrument_name:{self.instrument_name} note:{self.note} length:{self.length} strength:{self.strength} intonation:{self.intonation}"

    def select(self):
        if self.used:
            return False

        self.used = True
        return True

def gen_sample_list():
    for dir in non_dup_list:
        mp3_in_dir = [os.path.join(instrument_sample_dir, dir, x) for x in os.listdir(dir) if x.endswith(".mp3")]
        for file in mp3_in_dir:
            mp3_attributes = os.path.basename(file).strip(".mp3").split("_")
            sample = Sample(file, *mp3_attributes)
            if sample.note != '' and not ('A' in sample.note and not 's' in sample.note):
                continue
            yield sample


def gen_attribute_dict(attribute: str):
    return_dict = dict()
    for sample in gen_sample_list():
        attribute_value = getattr(sample, attribute)
        list_of_attribute = return_dict.get(attribute_value)
        if not list_of_attribute:
            list_of_attribute = list()
        list_of_attribute.append(sample)
        return_dict[attribute_value] = list_of_attribute
    return return_dict

suf_sample = Sample(file_path="/Volumes/Hi/Dropbox/ableton_workspace/sample/000.wav", instrument_name="sufjan", note="", length=1,strength=1, intonation=None)

with ZipFile(template_path,"r") as zip_ref, TemporaryDirectory() as temp_dir:
    # get the sd card back to template status
    os.system(f"rm -r {sd_card_path}/*")
    
    zip_ref.extractall(temp_dir)

    for dirname in ["ROLAND", "BKUP"]:
        src_path = os.path.join(temp_dir, dirname)
        dest_path = os.path.join(sd_card_path, dirname)
        shutil.copytree(src=src_path, dst=dest_path)


# select how to sort the samples
options = ["instrument_name","note","length","strength","intonation"]
option = "note" # choice(options)
count = 1

# make a dictionary of the samples sorted
attribute_dict = gen_attribute_dict(option)

def select_samples():
    # sp404 has 120 sample slots
    print(f"abc123 suf suf {suf_sample.file_name}")
    yield suf_sample
    for _ in range(0, 119):
        eligable_attribute_list = []
        while len(eligable_attribute_list) == 0:
            # select one of the keys in the dictionary we created filtering by option
            attribute_selected = choice([choice(list(attribute_dict.keys())), '']) # give the drums a 50/50 shot
            # select a sample from the list that was selected previously
            eligable_attribute_list = [sample for sample in attribute_dict[attribute_selected] if sample.used is False]

        selected_sample = choice(eligable_attribute_list)
        selected_sample.select()
        yield selected_sample
    
sample_list =  list(select_samples())
for sample in sample_list:
    print(sample.file_name)

for index, sample in enumerate(sorted(sample_list, key=lambda sample: getattr(sample, option))):
    dest = os.path.join(sd_card_sample_destination, f"{index:03d}.wav")
    print(option, getattr(sample, option), sample.file_name, dest)

    # need to convert to wav
    sound = remove_leading_trailing_silence(AudioSegment.from_mp3(sample.file_path))
    sound.export(dest, format="wav")

os.system(f"open {sd_card_sample_destination}")

