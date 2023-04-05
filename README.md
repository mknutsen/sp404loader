# sp404loader
formats a sd card and loads it with samples

assembles a memory card for the Roland SP404-SX/AThe samples are also trimmed and formatted to wav

The SD card is erased and the template is replaced. When booting the sp 404 hit import all and it will auto load the samples into the banks.

Takes a directory. Each subdirectory of that will be considered a category. 120 samples will be selected, an equal number of each category.

## TL;DR
```
python3 -m pip install requirements.txt
python3 main.py --directory {{directory of your samples}}
```

Sample Dir:
These are the sub directories I have. It doesn't matter what they're called but each subdirectory will be treated equally.
```
00 dk             03 hats & cymbals 06 808s & basses  09 synth
01 kicks          04 percs & fx     07 vox & adlibs
02 snares         05 loops & breaks 08 foley
```
`120 / 10 = 12` - each folder will have `12 samples` selected in this case. The leftover slots, should they exist, will be filled in at random.

The contents of each top level directory (eg `01 kicks`) will have all its files including subdirectories all included.

When they are loaded on the SD card they will be loaded in alphabetical order of the file path, which means samples in the same folder will be next to eachother.

It should accept any audio file type and convert it to .wav as well as remove the leading silence.


sp 404 template folder here: https://github.com/mknutsen/sp404loader/releases/download/main/sp_template.zip
