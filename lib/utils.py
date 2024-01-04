import os
import sys

sys.path.append(os.path.dirname(sys.path[0]))
LEMMA = "#lemma"

# already ignored in tactician
ignored_coq_constructors = [
    "coq_int",
    "coq_float",
    "coq_app",
    "coq_case",
    "coq_fix",
    "coq_cofix",
    "coq_letin",
    "coq_cast",
    "coq_proj",
    "coq_sort",
]

coq_identifier = ['coq_var', 'coq_const', 'coq_constructor', 'coq_ind']

def under_max_arity(a):
    a = int(a)
    if a < 4:
        return a
    else:
        return 4


def output_lemma_aux(lemma, data, file):
    with open(file, "a") as writer:
        writer.write(f"#lemma\t{lemma}\n")
        for state in data:
            writer.write(state + "\n")


def lemma_name(l):
    return l.split("\t")[1]


# The names of hypotheses are much more flexible than identifiers; thus, we them convert to strings.
def hyp_name(n):
    if n[0].isupper():
        n = "coq_" + n
    return f'"{n}"'


## For predicates
def to_predc_name(s):
    s = s.replace(".", "_")
    if s.startswith("Coq_"):
        s = s[0].lower() + s[1:]
    if not s.startswith("coq_"):
        s = "coq_" + s
    s = s.replace("'", "_quote")
    s = s.replace("₁", "_under1_")
    s = s.replace("₂", "_under2_")
    s = s.replace("₃", "_under3_")
    return s


def to_ident(ident, typ):
    if typ == "coq_var":
        return hyp_name(ident)
    else:
        return to_predc_name(ident)


def goal_idx(idx):
    idx = ",".join([str(i) for i in idx])
    idx = "[" + idx + "]"
    return idx


def hyp_idx(name, kind, idx):
    idx = [name, kind] + [str(i) for i in idx]
    idx = ",".join(idx)
    idx = "[" + idx + "]"
    return idx


def ignore_arity(id, art):
    return (id in ["coq_var", "coq_rel", "coq_evar"]) | (art == 0)


def mk_anonym_predc(typ, ident):
    # additional constants other than them during the dataset generation
    if ident in [
        "Coq.Init.Logic.False",
        "Coq.Init.Logic.True",
        "Coq.Init.Logic.and",
        "Coq.Init.Logic.iff",
        "Coq.Init.Logic.or",
        "Coq.Init.Logic.not",
        "Coq.Init.Logic.eq",
        "Coq.Init.Datatypes.true",
        "Coq.Init.Datatypes.false",
    ]:
        return ident
    else:
        return typ


def pr_hyps_predc(i, l, writer):
    for ident, name, kind, idx in l:
        if ident not in ["coq_app"]:
            ident = to_predc_name(ident)
            name = hyp_name(name)
            idx = hyp_idx(name, kind, idx)
            writer.write(f"hyp_node({ident},{i},{name},{idx}).\n")


def pr_hyps_anonym_predc(i, l, writer):
    for typ, ident, _arity, name, kind, idx in l:
        predc = mk_anonym_predc(typ, ident)
        predc = to_predc_name(predc)
        ident = to_ident(ident, typ)
        name = hyp_name(name)
        idx = hyp_idx(name, kind, idx)
        if predc in ["coq_case"]:
            continue
        else:
            # if predc in coq_identifier:
            #     writer.write(f"hyp_node(coq_identifier,{i},{name},{idx},{ident}).\n")
            writer.write(f"hyp_node({predc},{i},{name},{idx},{ident}).\n")


def pr_goal_predc(i, l, writer):
    for ident, idx in l:
        if ident not in ["coq_app"]:
            ident = to_predc_name(ident)
            writer.write(f"goal_node({ident},{i},{goal_idx(idx)}).\n")


def pr_goal_anonym_predc(i, l, writer):
    for typ, ident, _arity, idx in l:
        predc = mk_anonym_predc(typ, ident)
        predc = to_predc_name(predc)
        idx = goal_idx(idx)
        ident = to_ident(ident, typ)
        if predc in ["coq_case"]:
            continue
        else:
            # if predc in coq_identifier:
            #     writer.write(f"goal_node(coq_identifier,{i},{idx},{ident}).\n")
            writer.write(f"goal_node({predc},{i},{idx},{ident}).\n")


def add_hyps_predc(l, predc_set):
    for ident, _, _, _ in l:
        if ident not in ["coq_app"]:
            predc_set.add(to_predc_name(ident))
    return predc_set


def add_hyps_anonym_predc(l, predc_set, ident_set):
    for typ, ident, _arity, _, _, _ in l:
        predc = mk_anonym_predc(typ, ident)
        predc = to_predc_name(predc)
        if predc in ["coq_case"]:
            continue
        else:
            # if predc in coq_identifier:
            #     predc_set.add('coq_identifier')
            predc_set.add(predc)
            ident_set.add(to_ident(ident, typ))
    return predc_set, ident_set


def add_goal_predc(l, predc_set):
    for ident, _ in l:
        if ident not in ["coq_app"]:
            predc_set.add(to_predc_name(ident))
    return predc_set


def add_goal_anonym_predc(l, predc_set, ident_set):
    for typ, ident, _arity, _ in l:
        predc = mk_anonym_predc(typ, ident)
        predc = to_predc_name(predc)
        if predc in ["coq_case"]:
            continue
        else:
            # if predc in coq_identifier:
            #     predc_set.add('coq_identifier')            
            predc_set.add(predc)
            ident_set.add(to_ident(ident, typ))
    return predc_set, ident_set


def safe_tac(t):
    t = t.replace("\\", "bkslash")
    # t = t.replace("'", 'quote')
    return t


def not_lemma(l):
    return not l.startswith(LEMMA)


def feat_reader(label_f, label_encoder, feat_f, feat_encoder):
    labels = []
    feats = []
    with open(label_f, "r") as reader:
        for l in reader:
            l = l.strip()
            if not_lemma(l):
                labels.append(l)
        labels = label_encoder.transform(labels)

    with open(feat_f, "r") as reader:
        for l in reader:
            l = l.strip()
            if not_lemma(l):
                fs = l.split()
                fs = [int(f) for f in fs]
                feats.append(fs)
        feats = feat_encoder.transform(feats)
    return feats, labels


def load_file(f, dat):
    lemma_states = []
    with open(f, "r") as reader:
        for line in reader:
            if not_lemma(line):
                lemma_states.append(line)
            else:
                if lemma_states != []:
                    dat[lemma] = lemma_states
                lemma = line
                lemma_states = []
        dat[lemma] = lemma_states
    return dat

def valid_dat_f(f):
    return f.endswith(".json") & (("plugins/" in f) | ("theories/" in f))


def file_order():
    forder = "/home/zhangliao/ilp_out_coq/ilp_out_coq/data/file_order"
    with open(forder, "r") as r:
        files = r.readlines()
        files = [f.strip() for f in files]
    return files


def load_dataset(dir):
    dat = {}
    for root, _, files in os.walk(dir):
        for file in files:
            path = os.path.join(root, file)
            if valid_dat_f(path):
                dat = load_file(path, dat)
    return dat


def load_dataset_no_lemma(dir):
    dat = []
    orders = file_order()
    i = 0
    for f in orders:
        path = os.path.join(dir, f)
        if not os.path.exists(path):
            raise FileNotFoundError(f)
        with open(path, "r") as r:
            for l in r:
                if not_lemma(l):
                    dat.append((i, l))
                i += 1
    return dat



def load_subdir_no_lemma(dir, subdir):
    dat = []
    orders = file_order()
    i = 0
    for f in orders:
        path = os.path.join(dir, f)
        if not os.path.exists(path):
            raise FileNotFoundError(f)
        if subdir in f:
            with open(path, "r") as r:
                for l in r:
                    if not_lemma(l):
                        dat.append((i, l))
                    i += 1
    return dat


def update_dic(dic, new_item, default, key):
    if key not in dic.keys():
        dic[key] = default
    else:
        dic[key].update(new_item)


THEORIES = [
    "theories/Sorting",
    "theories/NArith",
    # "theories/Numbers",
    "theories/Init",
    "theories/Vectors",
    "plugins/setoid_ring",
]

IGNORED_TACS = ["intros", "split"]
