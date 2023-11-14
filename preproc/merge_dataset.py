import shutil
import os
import argparse


def is_theory(path):
    path = path.strip("/")
    splits = path.split("/")
    if (len(splits) == 2) & (splits[0] in ["theories", "plugins"]):
        return True
    else:
        return False


def get_theory_files(theory):
    theory_files = []
    for root, _, files in os.walk(theory):
        for f in files:
            if f.endswith(".json"):
                theory_files.append(os.path.join(root, f))
    theory_files.sort()
    return theory_files


def merge_files(dest, files):
    # print(dest)
    if os.path.exists(dest):
        os.remove(dest)
    w = open(dest, "a+")
    for f in files:
        r = open(f, "r")
        dat = r.readlines()
        w.writelines(dat)


parser = argparse.ArgumentParser()
parser.add_argument("--dir", type=str)
# parser.add_argument("--dest_dir", type=str)
opts = parser.parse_args()


source_dirs = [
    os.path.join(opts.dir, "theories"),
    os.path.join(opts.dir, "plugins"),
]
for kind in ["theories", "plugins"]:
    dest_dir = os.path.join(opts.dir, "merge", kind)
    dir = os.path.join(opts.dir, kind)
    for theory in os.listdir(dir):
        files = get_theory_files(os.path.join(dir, theory))
        if os.path.exists(dest_dir) == False:
            os.makedirs(dest_dir)
        dest_f = os.path.join(dest_dir, f"{theory}.json")
        merge_files(dest_f, files)
    # print(files)
    # exit()
    # for root, dir, files in os.walk(source_dir):
    #     path_in_dir = root.removeprefix(opts.dir)
    #     for file in files:
    #         if file.endswith(".json"):
    #             dir_obj = os.path.join(dest, path_in_dir)
    #             if os.path.exists(dir_obj) == False:
    #                 os.makedirs(dir_obj)
    #             shutil.copyfile(root + "/" + file, os.path.join(dir_obj, file))
