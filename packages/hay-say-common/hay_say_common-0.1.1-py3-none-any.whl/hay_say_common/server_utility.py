from .file_integration import OUTPUT_DIR, model_dirs

from flask import request

import os
import traceback
import json


def create_link(existing_path, desired_link_path):
    if not os.path.exists(desired_link_path):
        os.symlink(existing_path, desired_link_path)


def get_model_path(architecture, character):
    character_dir = [os.path.join(model_dir, character)
                     for model_dir in model_dirs(architecture)
                     if os.path.exists(os.path.join(model_dir, character))]
    if len(character_dir) == 0:
        raise Exception('Character directory was not found! Expected to find a subdirectory named ' + character + ' in '
                        'one of these directories: ' + ', '.join(model_dirs(architecture)))
    elif len(character_dir) > 1:
        raise Exception('More than one character directory with the name ' + character + ' was found! Expected to '
                        'find only one subdirectory with that name among all of the following directories: ' +
                        ', '.join(model_dirs(architecture)) + '. Since more than one was found, it is '
                        'impossible to determine which one the user intended to use. All models must have unique '
                        'names.')
    else:
        return character_dir[0]


def clean_up(files_to_delete):
    if files_to_delete:
        for path in files_to_delete:
            os.remove(path)


def construct_full_error_message(architecture_root_dir, files_to_delete):
    message = construct_error_message(architecture_root_dir)
    try:
        clean_up(files_to_delete)
    except Exception:
        message += '\n\n...and failed to clean output directory, due to: \n' + traceback.format_exc(chain=False) + '\n'
    return message


def construct_error_message(architecture_root_dir):
    input_files = get_file_list(architecture_root_dir)
    output_files = get_file_list(OUTPUT_DIR)
    return 'An error occurred while generating the output: \n' + traceback.format_exc() + \
           '\n\nPayload:\n' + json.dumps(request.json) + \
           '\n\nInput Audio Dir Listing: \n' + input_files + \
           '\n\nOutput Audio Dir Listing: \n' + output_files


def get_file_list(folder):
    if os.path.exists(folder):
        return ', '.join(os.listdir(folder))
    else:
        return 'directory does not exist'
