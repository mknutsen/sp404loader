import os
import shutil
import urllib
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from pydub import AudioSegment


def write_sample(sound, sd_card_sample_destination, sample_count):
    name = f"{sample_count:03d}.wav"
    dest = os.path.join(sd_card_sample_destination, name)
    sound.export(dest, format="wav")
    sample_count += 1
def setup_404_folder(sd_card_path, template_path=None):
    # unpack the template
    if template_path is None:
        print("fetching SP404 template zip")
        new_path = TemporaryDirectory()
        template_path = os.path.join(str(new_path.name), "sp_template.zip")
        urllib.request.urlretrieve("https://github.com/mknutsen/sp404loader/releases/download/main/sp_template.zip",
                                   template_path)

    with ZipFile(template_path, "r") as zip_ref, TemporaryDirectory() as temp_dir:
        print("Clearing SD Card")
        # get the sd card back to template status
        os.system(f"rm -r {sd_card_path}/*")

        print("Extracting zip template")
        zip_ref.extractall(temp_dir)

        for dirname in ["ROLAND", "BKUP"]:
            src_path = os.path.join(temp_dir, dirname)
            dest_path = os.path.join(sd_card_path, dirname)
            shutil.copytree(src=src_path, dst=dest_path)


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

def load_sd_card(sample_list_list, sd_card_sample_destination):
    sample_count = 0

    for sample_list in sample_list_list:
        for sample in sample_list:
            sound = remove_leading_trailing_silence(AudioSegment.from_file(sample))
            write_sample(sound, sd_card_sample_destination=sd_card_sample_destination, sample_count=sample_count)
            sample_count += 1