import re
import shutil
import sys
from pathlib import Path


JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
AVI_VIDEO = []
MP4_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []
DOC_FILES = []
DOCX_FILES = []
TXT_FILES = []
PDF_FILES = []
XLSX_FILES = []
PPTX_FILES = []
MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []
MY_OTHER = []
ARCHIVES = []


REGISTER_EXTENSION = {
    'JPEG': JPEG_IMAGES,
    'JPG': JPG_IMAGES,
    'PNG': PNG_IMAGES,
    'SVG': SVG_IMAGES,
    'AVI': AVI_VIDEO,
    'MP4': MP4_VIDEO,
    'MOV': MOV_VIDEO,
    'MKV': MKV_VIDEO,
    'DOC': DOC_FILES,
    'DOCX': DOCX_FILES,
    'TXT': TXT_FILES,
    'PDF': PDF_FILES,
    'XLSX': XLSX_FILES,
    'PPTX': PPTX_FILES,
    'MP3': MP3_AUDIO,
    'OGG': OGG_AUDIO,
    'WAV': WAV_AUDIO,
    'AMR': AMR_AUDIO,
    'ZIP': ARCHIVES,
    'GZ': ARCHIVES,
    'TAR': ARCHIVES
}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()

def get_extension(name: str) -> str:
    return Path(name).suffix[1:].upper()

def scan(folder: Path):
    for item in folder.iterdir():
        # робота з папкою
        if item.is_dir():
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'MY_OTHER'):
                FOLDERS.append(item)
                scan(item)
            continue

# робота з файлом
        extension = get_extension(item.name)
        full_name = folder / item.name
        if not extension:
            MY_OTHER.append(full_name)
        else:
            try:
                ext_reg = REGISTER_EXTENSION[extension]
                ext_reg.append(full_name)
                EXTENSIONS.add(extension)
            except KeyError:
                UNKNOWN.add(extension)
                MY_OTHER.append(full_name)



CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

TRANS = dict()

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(name: str) -> str:
    translate_name = re.sub(r'\W', '_', name.translate(TRANS))
    return translate_name

def handle_media(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    new_file_name = normalize(file_name.stem) + file_name.suffix
    file_name.replace(target_folder / new_file_name)

def handle_archive(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(file_name.name.replace(file_name.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(file_name.absolute()), str(folder_for_file.absolute()))
    except shutil.ReadError:
        folder_for_file.rmdir()
        return
    file_name.unlink()



def main(folder: Path):
    scan(folder)
    for file in JPEG_IMAGES:
        handle_media(file, folder / 'images' / 'JPEG')
    for file in JPG_IMAGES:
        handle_media(file, folder / 'images' / 'JPG')
    for file in PNG_IMAGES:
        handle_media(file, folder / 'images' / 'PNG')
    for file in SVG_IMAGES:
        handle_media(file, folder / 'images' / 'SVG')

    for file in AVI_VIDEO:
        handle_media(file, folder / 'video' / 'AVI')
    for file in MP4_VIDEO:
        handle_media(file, folder / 'video' / 'MP4')
    for file in MOV_VIDEO:
        handle_media(file, folder / 'video' / 'MOV')
    for file in MKV_VIDEO:
        handle_media(file, folder / 'video' / 'MKV')

    for file in DOC_FILES:
        handle_media(file, folder / 'docs' / 'DOC')
    for file in DOCX_FILES:
        handle_media(file, folder / 'docs' / 'DOCX')
    for file in TXT_FILES:
        handle_media(file, folder / 'docs' / 'TXT')
    for file in PDF_FILES:
        handle_media(file, folder / 'docs' / 'PDF')
    for file in XLSX_FILES:
        handle_media(file, folder / 'docs' / 'XLSX')
    for file in PPTX_FILES:
        handle_media(file, folder / 'docs' / 'PPTX')

    for file in MP3_AUDIO:
        handle_media(file, folder / 'audio' / 'MP3')
    for file in OGG_AUDIO:
        handle_media(file, folder / 'audio' / 'OGG')
    for file in WAV_AUDIO:
        handle_media(file, folder / 'audio' / 'WAV')
    for file in AMR_AUDIO:
        handle_media(file, folder / 'audio' / 'AMR')

    for file in MY_OTHER:
        handle_media(file, folder / 'MY_OTHER')
    for file in ARCHIVES:
        handle_archive(file, folder / 'ARCHIVES')

    for folder in FOLDERS[::-1]:
        try:
            folder.rmdir()
        except OSError:
            print(f'Error during remove folder {folder}')

def start():
    if sys.argv[1]:
        folder_process = Path(sys.argv[1])
        main(folder_process)