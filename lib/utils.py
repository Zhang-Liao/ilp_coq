import os
import sys

sys.path.append(os.path.dirname(sys.path[0]))
lemma_delimiter = "#lemma"

def output_lemma_aux(lemma, data , file):
    with open(file, 'a') as writer:
        writer.write(f"#lemma\t{lemma}\n")
        for state in data:
            writer.write(state + '\n')

def lemma_name(l):
    return l.split('\t')[1]

## For predicates
def to_predc_name(s):
    s = s.replace('.', '_')
    if s.startswith('Coq_'):
        s = s[0].lower() + s[1:]
    if not s.startswith('coq_'):
        s = 'coq_' + s
    s = s.replace('\'', '_quote')
    s = s.replace('₁', '_under1_')
    s = s.replace('₂', '_under2_')
    s = s.replace('₃', '_under3_')
    return s

def goal_idx(idx):
    idx = ",".join([str(i) for i in idx])
    idx = "[" + idx +"]"
    return idx

def hyp_idx(name, kind, idx):
    idx = [name, kind] + [str(i) for i in idx]
    idx = ",".join(idx)
    idx = "[" + idx +"]"
    return idx

def hyp_name(n):
    if n[0].isupper():
        n = 'coq_' + n
    return f"\"{n}\""

def pr_hyps_predc(i, l, writer):
    for ident, name, kind, idx in l:
        ident = to_predc_name(ident)
        name = hyp_name(name)
        idx = hyp_idx(name, kind, idx)
        if ident.startswith('coq_var_'):
            var = hyp_name(ident[8:])
            writer.write(f"hyp_coq_var({i}, {var}, {name},{idx}).\n")
        elif ident != 'coq_app':
            writer.write(f"{ident}({i}, {name},{idx}).\n")

def pr_goal_predc(i, l, writer):
    for ident, idx in l:
        if ident.startswith('coq_var_'):
            # var = ident[8:]
            var = hyp_name(ident[8:])
            writer.write(f"goal_coq_var({i},{var},{goal_idx(idx)}).\n")
        elif ident != 'coq_app':
            ident = to_predc_name(ident)
            writer.write(f"{ident}({i},{goal_idx(idx)}).\n")

def add_hyps_predc(l, predc_set):
    for ident, _, _, _ in l:
        if (ident != 'coq_app') & (not ident.startswith('coq_var')):
            predc_set.add(to_predc_name(ident))
    return predc_set

def add_goal_predc(l, predc_set):
    for ident, _, in l:
        if (ident != 'coq_app') & (not ident.startswith('coq_var')):
            predc_set.add(to_predc_name(ident))
    return predc_set

def safe_tac(t):
    t = t.replace('\\', 'bkslash')
    # t = t.replace("'", 'quote')
    return t

def not_lemma(l):
    return not l.startswith(lemma_delimiter)

def feat_reader(label_f, label_encoder, feat_f, feat_encoder):
    labels = []
    feats = []
    with open(label_f, 'r') as reader:
        for l in reader:
            l = l.strip()
            if not_lemma(l):
                labels.append(l)
        labels = label_encoder.transform(labels)

    with open(feat_f, 'r') as reader:
        for l in reader:
            l = l.strip()
            if not_lemma(l):
                fs = l.split()
                fs = [int(f) for f in fs]
                feats.append(fs)
        feats = feat_encoder.transform(feats)
    return feats, labels
