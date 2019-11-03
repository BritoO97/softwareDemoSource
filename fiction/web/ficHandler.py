import subprocess
import shutil
import os

def start(url):
    # because the fiction.py file must run under python 3.7, while the Flask Api from which this file is run is running under python 2 a subprocess is used to allow this.
    result = subprocess.check_output('/var/www/flaskapps/optionone/fiction.py ' + url, shell=True)

    # the results variable will have the name of the directory just created, which we then cd into
    os.chdir(result)

    # compress the resulting directory using zip compression
    shutil.make_archive(result, 'zip')
    
    # remove the original, unzipped directory
    shutil.rmtree(result)

    # return the path to the zip file.
    return (result + '.zip')
