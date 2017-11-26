import os
from os import listdir
from os.path import isfile, join, isdir, dirname

# For the config file
import json

# Module to export images to pdf
import img2pdf

# Module to make zip file
import zipfile

# Module to get the leaf from the path
import ntpath

# Module to make the script multiprocessing
from mpipe import UnorderedWorker, Stage, Pipeline


'''
 Returns the folder parent to the one pass in argument
'''
def get_parent_from_path(path):
    return dirname(path)

'''
 Returns the leaf from a given path
'''
def get_leaf_from_path(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

'''
 Return all subdirectories from a path
'''
def get_subdiretories(directory):
    return [x[0] for x in os.walk(directory) if (x[0] != directory and 'BACKUP' not in x[0])]

'''
 Returns all immmediate subdirecotries
'''
def get_immediate_subdirectories(a_dir):
    return [a_dir + '\\' + name for name in listdir(a_dir) if isdir(join(a_dir, name))]

'''
 Delete directory in list
'''
def delete_dirs(lt_dir):
    import shutil
    for dire in lt_dir:
        shutil.rmtree(dire)
#<------------------------------------->#
#<------------------------------------->#
#<------------------------------------->#

'''
 Class to multiprocess a folder containing images
 Takes the name of the directory for the filename

 Returns a tuple containing :
 filename.pdf, [images1.jpg, ..., imagesN.png]
'''
class GetImages(UnorderedWorker):
    def doTask(self, folderpath):
        return (folderpath + '.pdf', [folderpath + '\\' + f for f in listdir(folderpath) if (isfile(join(folderpath, f)) and ".pdf" not in f)])

'''
 Class to multiprocess a list of images and
 to make them into a pdf.

 Returns the filename given to the pdf
'''
class MakePdf(UnorderedWorker):
    def doTask(self, tup):
        with open(tup[0],"wb") as f:
            f.write(img2pdf.convert(tup[1]))
        return tup[0]

'''
 Class to multiprocess the compressing of the images

 Returns the filename of the zipfile
'''
class MakeBackup(UnorderedWorker):
    def doTask(self, tup):
        fold_n = tup[0][:-4]
        filename = get_parent_from_path(fold_n) + '\\BACKUP\\' + get_leaf_from_path(fold_n) + '.zip'
        with zipfile.ZipFile(filename, 'w') as zfile:
            for f in tup[1]:
                zfile.write(f, get_leaf_from_path(f), compress_type = zipfile.ZIP_DEFLATED)

        return filename

#<------------------------------------->#
#<------------------------------------->#
#<------------------------------------->#
'''
 Pipeline creation

 The Pipeline contains 2 or 3 stages

 First Stage : GetImages
 Second Stage : MakePdf
 Third Stage (optional) : MakeBackup

'''
def sub2Pdf(path, backup, remove_dir, debug):
    stage1 = Stage(GetImages,2)
    stage2 = Stage(MakePdf,7)

    if backup:
        stage3 = Stage(MakeBackup,7)
        stage1.link(stage3)
        if not os.path.exists(path + '\\BACKUP'):
            os.makedirs(path + '\\BACKUP')

    stage1.link(stage2)

    pipe = Pipeline(stage1)
    lt_dir = get_subdiretories(path)
    for folder in lt_dir:
        pipe.put(folder)

    pipe.put(None)

    if debug:
        print("Converting to pdf :\n%s\n" % ('Backup activated' if backup else 'Backup deactivated'))

    # This allows to wait until all task are done
    for res in pipe.results():
        try:
            if debug:
                print('    Done :=> ' + res)
        except Exception:
            pass

    if remove_dir:
        delete_dirs(lt_dir)

    print('\nFinished treating : %s' % get_leaf_from_path(path))

'''
Fonction for the mode : collectionToPdf
Config options:
   - 'backup' : boolean
   - 'path' : string
   - 'remove_dir' : boolean
   - 'debug' : boolean
   - 'mode' : "collectionToPdf"
'''
def collectionToPdf(config):
    subdirectories = get_immediate_subdirectories(config['path'])

    for sub in subdirectories:
        if config['debug']:
                print("\nTreating subdirectory : %s\n" % get_leaf_from_path(sub))
        sub2Pdf(sub, config['backup'], config['remove_dir'], config['debug'])

    print('\nDONE')

'''
 Fonction for the mode : subdirectoriesToPdf

 Config options:
    - 'backup' : boolean
    - 'path' : string
    - 'remove_dir' : boolean
    - 'debug' : boolean
    - 'mode' : "subdirectoriesToPdf"
'''
def subdirectoriesToPdf(config):
    sub2Pdf(config['path'], config['backup'], config['remove_dir'],config['debug'])

'''
 Fonction that makes the pdf for
 the mode : directoryToPdf

 No pipeline needed for this.

 Config options:
    - 'backup' : boolean
    - 'path' : string
    - 'remove_dir' : boolean
    - 'debug' : boolean
    - 'mode' : "directoryToPdf"
    - 'name' : string

 If name is not specify, the .pdf and .zip
 is given the same name as the directory
'''
def directoryToPdf(config):
    getImg = GetImages()
    tup = getImg.doTask(config['path'])

    if 'name' in config:
        tup = (get_parent_from_path(config['path']) + '\\' +  config['name'] + '.pdf', tup[1])

    if config['backup']:
        par_path = get_parent_from_path(config['path'])
        if not os.path.exists(par_path + '\\BACKUP'):
            os.makedirs(par_path + '\\BACKUP')

        mk_back = MakeBackup()
        mk_back.doTask(tup)

    mk_pdf = MakePdf()
    res = mk_pdf.doTask(tup)

    if config['debug']:
        print(res)

    if config['remove_dir']:
        import shutil
        shutil.rmtree(config['path'])

#<------------------------------------->#
#<------------------------------------->#
#<------------------------------------->#

if __name__ == '__main__':
    try:
        with open('config.json') as f:
            config = json.load(f)

    except Exception as e:
        print('Error detected while reading the config file :\n\n%s ' % e)
        import sys
        sys.exit()

    try:
        if not 'mode' in config:
            raise Exception('Mode must be specified')

        mode = config['mode']
        if mode == 'directoryToPdf':
            directoryToPdf(config)
        elif mode == 'subdirectoriesToPdf':
            subdirectoriesToPdf(config)
        elif mode == 'collectionToPdf':
            collectionToPdf(config)
        else:
            raise Exception("Invalid Mode")

    except Exception as e:
        print('%s' % e)
        import sys
        sys.exit()
