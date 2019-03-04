import shutil
import os
import re

'''
используется для переименования файлов по двум возможным паттернам к общему паттерну наименования
файл готов для компиляции в exe файл
'''

def rename_files(dirname):
    files = os.listdir(dirname)
    try:
        files.remove('rename.exe')
    except:
        pass

    for file in files:
        print('file ',file)
        pattern1 = re.compile(r'(?P<iso>[a-zA-Z]{1,3}\d{8,9})-(?P<list>\d{1,2}).*(?P<format>\.[a-zA-Z]{3})')
        # паттерн названия из pdf project пример: bd200280011_1.pdf или bd200280011_IS1.pdf
        pattern_pdf_project = re.compile(r'(?P<iso>[a-zA-Z]{1,3}\d{8,9})(?P<list>\d{1,2})_?(IS)?(?P<rev>\d?\w?\w?)(?P<format>\.[a-zA-Z]{3})')
        find_data = pattern1.search(file)
        if find_data:
            try:
                os.rename(os.path.join(dirname, file),\
                      os.path.join(dirname, '{}-{} - общ.схема + 0ред{}'.format(find_data.group('iso'),
                                    find_data.group('list'),                          
                                    find_data.group('format'))))
                print('успешно переименован\n')
            except FileExistsError:
                print('файл с таким имененем уже существует\n')
        else:
            try:
                find_data = pattern_pdf_project.search(file)
                if find_data:
                    os.rename(os.path.join(dirname, file),\
                        os.path.join(dirname, '{}-{} - общ.схема + {}ред{}'.format(find_data.group('iso'),
                                                                            find_data.group('list'),
                                                                            find_data.group('rev'),
                                                                            find_data.group('format'))))
                    print('успешно переименован\n')
                else:
                    # если не удалось переименовать
                    print('название файла "{}" не соответствует заданным паттернам\n'.format(file))
            except FileExistsError:
                print('файл с таким имененем уже существует\n')


rename_files(os.getcwd())
input('press enter to exit')
