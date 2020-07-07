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
    return num

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
            filename = Path(i).name
            try:
                shutil.move(str(i), new_directory)
                count += 1
            except OSError:
                print("File {} already exist in new directory. ".format(filename))
                
                old_size = convert_bytes(Path(i).stat().st_size)
                path_new = '{}{}'.format(new_directory, filename)
                new_size = convert_bytes(Path(path_new).stat().st_size)
                
                print("File size in old directory: {}. File size in new directory: {}".format(old_size, new_size))
                print("Replace it ? y/n")
                
                inp = str(input()).lower()
                if(inp == 'y'):
                    shutil.move(str(i), '{}{}.'.format(new_directory,filename))
                    count += 1
                elif(inp == 'n'):
                    print("File not moved")
                else:
                    print("Wrong input !")                    
                    
    return print('{} files that contain keyword \'{}\' have been moved to {}'.format(count, keyword, new_directory))

if __name__ == '__main__':
    print("Enter search directory ")
    directory = str(input())
    print("Enter new directory")
    new_directory = str(input())
    print("Enter keyword")
    keyword = str(input())
    manage_file(directory, keyword, new_directory)
