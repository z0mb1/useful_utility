import os, shutil
import time

''' программа копирует необходимые таблицы из заданных директорий, удаляет старые версии '''

# settings for first table (wdb)
wdb_dir_1 = r"dirname 1"
wdb_dir_2 = r"dirname2"
wdb_filename = r'wdb_filename.xlsb'

# settings for second table
dirname = r"dirname2"
filename = r'filename.xlsb'


def get_file_date(path_to_file):
    tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst = time.strptime(time.ctime(os.path.getmtime(path_to_file)))
    return '{:02}.{:02}.{} {:02}:{:02}'.format(tm_mday, tm_mon, tm_year, tm_hour, tm_min)

def delete_old_file(filename, dirname):
    file_path = os.path.join(dirname, filename)
    if not os.path.exists(file_path):
        print("файл '{}' в папке '{}' отсутствует".format(filename, dirname))
        return
    print("Удаление файла '{}' от {}".format(filename, get_file_date(file_path)))
    try:
        os.remove(file_path)
        print('Удаление завершено\n')
    except PermissionError:
        print("Закройте файл '{}' и повторите попытку".format(filename))

def get_new_table(filename, dirname, tables_dir):
    '''копирует файл из папки в заданную директорию, предыдущую версию файла удаляет'''
    file_path = os.path.join(dirname, filename)

    if os.path.exists(file_path):
        old_file_path = os.path.join(tables_dir, filename)
        delete_old_file(filename, tables_dir)

        print("Копирование файла '{}' от {}".format(filename, get_file_date(file_path)))
        shutil.copy2(file_path, os.path.join(tables_dir, filename))
        print('Копирование завершено\n')

def get_new_wdb(filename, dirnames):
    '''
    копирует файл из папки в заданную директорию, предыдущую версию файла удаляет
    upd выполняет поиск в нескольких директориях и выбирает последний измененный файл
    '''
    files_and_dirs = []
    for dirname in dirnames:
        file_path = os.path.join(dirname, filename)
        if os.path.exists(file_path):
            files_and_dirs.append((filename, dirname))
    if files_and_dirs:
        dirname = sorted(files_and_dirs, key = lambda x: os.path.getmtime(os.path.join(x[1], x[0])))[-1][1]
        get_new_table(filename, dirname, os.getcwd())
    else:
        print("файл '{}' не найден в директориях: '{}'".format(filename, "', '".join(dirnames)))


get_new_wdb(wdb_filename, [wdb_dir_1, wdb_dir_2])
get_new_table(filename, dirname, os.getcwd())

input('press enter to exit')
