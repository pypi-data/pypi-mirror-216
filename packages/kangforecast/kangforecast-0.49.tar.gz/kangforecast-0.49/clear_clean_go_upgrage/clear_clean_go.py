#!/usr/bin/env python3

import os
import shutil
import subprocess

def print_tree(directory, level=2):
    print(f"\nDirectory structure ({directory}):")
    subprocess.run(['tree', '-L', str(level), directory])

def delete_certain_files_and_dirs(start_path):
    for dirpath, dirnames, filenames in os.walk(start_path):
        if '__pycache__' in dirnames:
            print(f"Delete directory: {os.path.join(dirpath, '__pycache__')}")
            shutil.rmtree(os.path.join(dirpath, '__pycache__'))
        for filename in filenames:
            if filename.endswith(('.png', '.log')):
                print(f"Delete file: {os.path.join(dirpath, filename)}")
                os.remove(os.path.join(dirpath, filename))

def delete_contents_in_specific_dirs(specific_dirs):
    for dir in specific_dirs:
        if os.path.exists(dir):
            for item in os.listdir(dir):
                item_path = os.path.join(dir, item)
                if os.path.isfile(item_path):
                    print(f"Delete file: {item_path}")
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    print(f"Delete directory: {item_path}")
                    shutil.rmtree(item_path)

def delete_specific_dirs(specific_dirs):
    for dir in specific_dirs:
        if os.path.exists(dir):
            print(f"Delete directory: {dir}")
            shutil.rmtree(dir)

def main():
    print_tree('.')
    print("\nclear - clean - go..... process...")
    delete_certain_files_and_dirs('.')
    delete_contents_in_specific_dirs(['dist'])
    delete_specific_dirs(['build', 'kangforecast.egg-info', 'env_kangpypi'])
    print("\nFinished cleaning.")
    print_tree('.')

if __name__ == "__main__":
    main()
