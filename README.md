# sp404loader
formats a sd card and loads it with samples

sp 404 template folder here: https://github.com/mknutsen/sp404loader/releases/download/main/sp_template.zip


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
