from pathlib import Path
import shutil
import sys
import file_parser as parser
from normalize import normalize
import os


def handle_media(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_other(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_archive(filename: Path, target_folder: Path):
    # Создаем папку для архивов
    target_folder.mkdir(exist_ok=True, parents=True)
    #  Создаем папку куда распаковываем архив
    # Берем суффикс у файла и убираем replace(filename.suffix, '')
    folder_for_file = target_folder / \
        normalize(filename.name.replace(filename.suffix, ''))
    #  создаем папку для архива с именем файла

    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(filename.resolve()),
                              str(folder_for_file.resolve()))
    except shutil.ReadError:
        print(f'Обман - это не архив {filename}!')
        folder_for_file.rmdir()
        return None
    filename.unlink()


def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f'Не удалось удалить папку {folder}')


def main(folder: Path):
    parser.scan(folder)

    for file in parser.JPEG_IMAGES:
        handle_media(file, folder / 'images')
    for file in parser.JPG_IMAGES:
        handle_media(file, folder / 'images')
    for file in parser.PNG_IMAGES:
        handle_media(file, folder / 'images')
    for file in parser.SVG_IMAGES:
        handle_media(file, folder / 'images')
    for file in parser.AVI_VIDEO:
        handle_media(file, folder / 'video')
    for file in parser.MP4_VIDEO:
        handle_media(file, folder / 'video')
    for file in parser.MOV_VIDEO:
        handle_media(file, folder / 'video')
    for file in parser.MKV_VIDEO:
        handle_media(file, folder / 'video')
    for file in parser.DOC_DOCUMETS:
        handle_media(file, folder / 'documents')
    for file in parser.DOCX_DOCUMETS:
        handle_media(file, folder / 'documents')
    for file in parser.TXT_DOCUMETS:
        handle_media(file, folder / 'documents')
    for file in parser.PDF_DOCUMETS:
        handle_media(file, folder / 'documents')
    for file in parser.XLSX_DOCUMETS:
        handle_media(file, folder / 'documents')
    for file in parser.PPTX_DOCUMETS:
        handle_media(file, folder / 'documents')
    for file in parser.MP3_AUDIO:
        handle_media(file, folder / 'audio')
    for file in parser.OGG_AUDIO:
        handle_media(file, folder / 'audio')
    for file in parser.WAV_AUDIO:
        handle_media(file, folder / 'audio')
    for file in parser.AMR_AUDIO:
        handle_media(file, folder / 'audio')

    for file in parser.OTHERs:
        handle_other(file, folder / 'OTHERs')
    for file in parser.ARCHIVES:
        handle_archive(file, folder / 'archives')

    # Выполняем реверс списка для того, чтобы все папки удалить.
    for folder in parser.FOLDERS[::-1]:
        handle_folder(folder)


def start(folder_for_scan):
    if os.path.exists(folder_for_scan):
        print(f'Start in folder {folder_for_scan.resolve()}')
        main(folder_for_scan.resolve())
        print('Sort completed successfully')
    else:
        print('The wrong path or folder does not exist\nSpecify the path in the format "E:/folder1/folder2"')


if __name__ == '__main__':
    if sys.argv[1]:
        folder_for_scan = Path(sys.argv[1])
        print(f'Start in folder {folder_for_scan.resolve()}')
        main(folder_for_scan.resolve())
