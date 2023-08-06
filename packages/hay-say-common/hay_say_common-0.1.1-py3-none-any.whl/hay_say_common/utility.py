import librosa

import base64
import io
import os

"""Methods that are useful across multiple Hay Say coding projects and are not necessarily related to file integration
or specific to servers"""


def get_audio_from_src_attribute(src, encoding):
    _, raw = src.split(',')
    b64_output_bytes = raw.encode(encoding)
    output_bytes = base64.b64decode(b64_output_bytes)
    buffer = io.BytesIO(output_bytes)
    return librosa.load(buffer, sr=None)


def read_audio(path):
    return librosa.load(path, sr=None)


def get_singleton_file(folder):
    """Given a folder, return the full path of the single file within that folder. If there is no file in that folder,
    or if there is more than one file in that folder, raise an Exception."""
    potential_filenames = [file for file in os.listdir(folder)]
    if len(potential_filenames) > 1:
        raise Exception('more than one file was found in the indicated folder. Only one was expected.')
    elif len(potential_filenames) == 0:
        raise Exception('No file was found in the indicated folder.')
    return os.path.join(folder, potential_filenames[0])
