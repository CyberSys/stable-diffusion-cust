"""
Two helper classes for dealing with PNG images and their path names.
PngWriter -- Converts Images generated by T2I into PNGs, finds
             appropriate names for them, and writes prompt metadata
             into the PNG.

Exports function retrieve_metadata(path)
"""
import os
import re
import json
from PIL import PngImagePlugin, Image
import time

# -------------------image generation utils-----


class PngWriter:
    def __init__(self, outdir):
        self.outdir = outdir
        os.makedirs(outdir, exist_ok=True)

    # gives the next unique prefix in outdir
    def unique_prefix(self):
        return f"{time.time_ns()}"

    # saves image named _image_ to outdir/name, writing metadata from prompt
    # returns full path of output
    def save_image_and_prompt_to_png(self, image, dream_prompt, name, metadata=None):
        path = os.path.join(self.outdir, name)
        info = PngImagePlugin.PngInfo()
        info.add_text('Dream', dream_prompt)
        if metadata: # TODO: merge command line app's method of writing metadata and always just write metadata
          info.add_text('sd-metadata', json.dumps(metadata))
        image.save(path, 'PNG', pnginfo=info)
        return path

    def retrieve_metadata(self,img_basename):
        '''
        Given a PNG filename stored in outdir, returns the "sd-metadata"
        metadata stored there, as a dict
        '''
        path = os.path.join(self.outdir,img_basename)
        all_metadata = retrieve_metadata(path)
        return all_metadata['sd-metadata']

def retrieve_metadata(img_path):
    '''
    Given a path to a PNG image, returns the "sd-metadata"
    metadata stored there, as a dict
    '''
    im = Image.open(img_path)
    md = im.text.get('sd-metadata', '{}')
    dream_prompt = im.text.get('Dream', '')
    return {'sd-metadata': json.loads(md), 'Dream': dream_prompt}

