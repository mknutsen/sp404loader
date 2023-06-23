import os

from moviepy.editor import AudioFileClip

dest_dir = "/Volumes/CRAIG/öäå/AUDIO"
source_dir = "/Volumes/Hi/Dropbox/ableton_workspace/sample"
file_paths = [
    # "JAKE REED SUPER NATURAL DRUMS SAMPLE PACK",
    # "JAKE REED SUPER DEAD DRUMS SAMPLE PACK 48/24",
    # "Jersey Club Vox",
    # "kenny rewards",
    # "Jungle Jungle - 1989 to 1999 Samplepack",
    # "Dreamland drum kit [by San]",
    # "MED 2021 SAMPLES",
    # "montesounds3",
    # "Mojo Pianos",
    # "Zero-G Jungle Warfare Complete"
    # # "monte sorted",
    # "soul acappelas",
    # "LSD Vocal Samples",
    # "BB - Brushed Drum Sample Pack",
    # "bo jackson acapellea",
    # "breakcore is not a good way to get laid",
    # "1000 gecs + TOC stems",
    # "Night Falls Over Kortedala",
    # "Mandalorian Sound FX",
    # "Donkey Kong 64 (SFX Kit)"
    "soul wav"
]

import subprocess

def convert_audio_to_sp404_wav(input_file, output_file):
    ffmpeg_cmd = [
        'ffmpeg',                     # Command
        '-i', input_file,             # Input file
        '-ar', '44100',               # Sample rate (44.1 kHz)
        '-ac', '1',                   # Number of channels (mono)
        '-acodec', 'pcm_s16le',       # Audio codec (16-bit PCM, little-endian)
        '-f', 'wav',                  # Output format (WAV)
        output_file                   # Output file
    ]

    subprocess.run(ffmpeg_cmd)

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
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                yield file, dest


pairs = list(gather())
for index, (src, dest) in enumerate(pairs):
    if index % 100 == 0:
        print(index)
    if convert_audio_to_octatrack_wav(src, dest):
        print(index / len(pairs) * 100, "%   complete")

# input_file = "input.mp3"
# output_file = "output.wav"
#
