import logging

import humanize as humanize
import librosa as librosa
from humanize import naturalsize
from moviepy.editor import AudioFileClip

import subprocess
import os
from tqdm import tqdm
dest_dir = "/Volumes/CRAIG/öäå/AUDIO"
source_dir = "/Volumes/Hi/Dropbox/ableton_workspace/sample"
file_paths = [
    "JAKE REED SUPER DEAD DRUMS SAMPLE PACK 48/24",
    "Jersey Club Vox",
    "Dreamland drum kit [by San]",
    "MED 2021 SAMPLES",
    "montesounds3",
    "Mojo Pianos",
    "monte sorted",
    "BB - Brushed Drum Sample Pack",
    "Donkey Kong 64 (SFX Kit)"
]

dest_dir = "/Volumes/SP404MKII/IMPORT"
logging.getLogger("ffmpeg").setLevel(logging.ERROR)
logging.basicConfig(level=logging.WARN)

def get_audio_frequency(audio_path):
    # Load audio file
    audio, _ = librosa.load(audio_path)

    # Compute the mel-frequency cepstral coefficients (MFCCs)
    mfcc = librosa.feature.mfcc(y=audio)

    # Calculate the mean MFCC values across time
    mean_mfcc = mfcc.mean(axis=1)

    # Return the average frequency as a representative value
    return mean_mfcc.mean()

def sort_audio_files_by_frequency(file_paths):
    sorted_files = sorted(file_paths, key=get_audio_frequency)

    # Create a dictionary to store the sorted files
    sorted_dict = {}

    # Define the number of bins and generate the thresholds
    num_bins = 8  # Adjust the number of bins as needed
    max_frequency = max(get_audio_frequency(file_paths[-1]), 1)  # Ensure non-zero maximum frequency
    thresholds = [max_frequency * (i+1) / num_bins for i in range(num_bins-1)]

    # Define the bin names
    bin_names = [f"bin{i+1}" for i in range(num_bins)]

    # Iterate over the sorted files and group them into frequency bins
    for file_path in sorted_files:
        frequency = get_audio_frequency(file_path)

        # Find the appropriate bin for the frequency
        bin_index = 0
        for threshold in thresholds:
            if frequency < threshold:
                break
            bin_index += 1

        # Assign the file path to the appropriate frequency bin in the dictionary
        bin_name = bin_names[bin_index]
        if bin_name in sorted_dict:
            sorted_dict[bin_name].append(file_path)
        else:
            sorted_dict[bin_name] = [file_path]

    return sorted_dict
def get_sd_card_size(sd_card_path):
    if os.path.exists(sd_card_path):
        total_size = os.statvfs(sd_card_path).f_frsize * os.statvfs(sd_card_path).f_blocks
        total_size_gb = total_size / (1024 ** 3)  # Convert bytes to gigabytes
        return total_size_gb
    else:
        return None

def get_total_file_size_bytes(file_paths):
    total_size = 0

    for file_path in file_paths:
        if os.path.isfile(file_path):
            total_size += os.path.getsize(file_path)

    return total_size

def get_total_file_size_humanized(file_paths):
    total_size = 0

    for file_path in file_paths:
        if os.path.isfile(file_path):
            total_size += os.path.getsize(file_path)

    total_size_humanized = naturalsize(total_size, binary=True)

    return total_size_humanized

def convert_audio_to_sp404_wav(input_file, output_file):
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', input_file,
        '-ar', '44100',
        '-ac', '1',
        '-acodec', 'pcm_s16le',
        '-f', 'wav',
        output_file
    ]
    # Access the output of ffmpeg
    _ = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def convert_audio_to_octatrack_wav(input_file, output_file):
    if os.path.isfile(output_file):
        try:
            _ = AudioFileClip(input_file)
        except Exception as e:
            os.remove(output_file)
        else:
            return False
    try:
        clip = AudioFileClip(input_file)
        clip.write_audiofile(output_file, codec='pcm_s16le', fps=44100, nbytes=2)
        return True
    except Exception as e:
        print("Error with: os.path.basename(input_file)")

    return False


def real_file(file_path):
    if file_path.startswith("._"):
        return False
    ext = [".wav", ".mp3", ".mp4", ".m4a", ".aiff", ".aif"]
    for e in ext:
        if file_path.endswith(e):
            return True
    else:
        return False


def gather():
    for folder in file_paths:
        dir_path = os.path.join(source_dir, folder)
        for root, folders, files in os.walk(dir_path):
            for file in [os.path.join(root, file) for file in files if real_file(os.path.join(root, file))]:
                rel = str(file).split(source_dir)[1].strip('/')
                dest = os.path.join(dest_dir, rel)
                yield file, dest


pairs = list(gather())
files = [file for file, dest in pairs]
bins = sort_audio_files_by_frequency(files)
# print(get_total_file_size_humanized(files))
with tqdm(total=len(files)) as progress_bar:
    for key, file_list in bins.items():
        dest_dir = os.path.join(dest_dir, key)
        os.makedirs(os.path.dirname(dest_dir), exist_ok=True)
        for src in file_list:
            dest = os.path.join(dest_dir, os.path.basename(src))
            convert_audio_to_sp404_wav(src, dest)
            progress_bar.update(1)

