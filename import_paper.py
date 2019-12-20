# %%
import os
import pandas as pd
from pprint import pprint
from shutil import copyfile
from local_toolbox import save_imgs, pdf_title

# %%
class Paper():
    def __init__(self, rawpath, collection_name='collection', verbose=2):
        # Init issue
        self.verbose = verbose
        # rawpath is the path of raw pdf
        # It should be ending with .pdf
        assert(rawpath.endswith('.pdf'))
        self.rawpath = rawpath
        # Try to fetch title,
        # note that it may fail
        self.title = pdf_title(rawpath)
        self.collection_name = collection_name
        self.update_info()

    def update_info(self):
        # Make path:
        # newdirpath is the new home path of the paper
        # imagespath is the new path of images
        self.newdirpath = os.path.join(self.collection_name, self.title)
        self.imagespath = os.path.join(self.newdirpath, 'images')
        self.introspath = os.path.join(self.newdirpath, 'intro.md')
        # Update info
        self.info = dict(
            rawpath = self.rawpath,
            title = self.title,
            newdirpath = self.newdirpath,
            imagespath = self.imagespath,
            introspath = self.introspath,
        )

    def log(self, message):
        if self.verbose:
            print('[{}]'.format(message))

    def save(self):
        self.log('-' * 80)
        self.log('[Saving paper: {}]'.format(self.title))
        # Make new dir
        os.mkdir(self.newdirpath)
        # Copy pdf file
        self.log('[Saving paper in {}]'.format(self.newdirpath))
        copyfile(self.rawpath, os.path.join(self.newdirpath, self.title+'.pdf'))
        # Save images in pdf file
        self.log('[Saving images in {}]'.format(self.imagespath))
        save_imgs(self.rawpath, self.imagespath)


# %%
for filename in os.listdir('buffer'):
    print(filename)
    if not filename.endswith('.pdf'):
        continue
    print(pdf_title(os.path.join('buffer', filename)))



# %%
