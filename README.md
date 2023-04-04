# sp404loader
formats a sd card and loads it with samples

sp 404 template folder here: https://github.com/mknutsen/sp404loader/releases/download/main/sp_template.zip

assembles a memory card for the Roland SP404-SX/AThe samples are also trimmed and formatted to wav

The SD card is erased and the template is replaced. When booting the sp 404 hit import all and it will auto load the samples into the banks.

Takes a directory. Each subdirectory of that will be considered a category. 120 samples will be selected, an equal number of each category.

## TL;DR
```
python3 -m pip install requirnments.txt
python3 main.py --directory {{directory of your samples}}
```
