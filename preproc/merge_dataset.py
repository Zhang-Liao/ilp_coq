import shutil
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--dir", type=str)
# parser.add_argument("--dest_dir", type=str)
opts = parser.parse_args()


source_dirs = [
    os.path.join(opts.dir, "theories"),
    os.path.join(opts.dir, "plugins"),
]
dest = os.path.join(opts.dir, "merge")
for source_dir in source_dirs:
    for root, dir, files in os.walk(source_dir):
        # print("root", root, "dir", dir)
        path_in_dir = root.removeprefix(opts.dir)
        # print(path_in_dir)
        for file in files:
            if file.endswith(".json"):
                dir_obj = os.path.join(dest, path_in_dir)
                if os.path.exists(dir_obj) == False:
                    os.makedirs(dir_obj)
                shutil.copyfile(root + "/" + file, os.path.join(dir_obj, file))
