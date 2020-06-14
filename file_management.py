from pathlib import Path
import re
import shutil

def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

def manage_file(directory, keyword, new_directory):
    """
    Organize files by the filename pattern
    ---------
    Parameters :
    directory = directory with file need to be organised. example D:/folder
    keyword = any char or combination of char that filename might contain
    new_directory = any file that meet condition from keyword will be moved in new_directory
    """
    if not(Path(directory).exists()):
        return print('source path doesn\'t exist')
    elif not(Path(new_directory).exists()):
        Path(new_directory).mkdir()
        print('destination path doesn\'t exist, created new folder in {}'.format(new_directory))

    p = Path(directory)
    files = []
    for i in p.glob('**/*'):
        files.append(i)    
    
    regexp = re.compile(r'.*({}).*'.format(keyword), re.IGNORECASE)
    count = 0
    for i in files:
        if (regexp.search(str(i))):
            count += 1
            shutil.move(str(i), new_directory)

    return print('{} files that contain keyword \'{}\' have been moved to {}'.format(count, keyword, new_directory))

"""Usage
directory = 'some path'
keyword = 'some path'
new_directory = ''
manage_file(directory, keyword, new_directory)
"""