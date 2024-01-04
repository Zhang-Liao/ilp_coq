# Log

fix identifiers

for p in goal_predc:
    writer.write(f':- modeb(*, goal_node("{p}", +nat, -goal_idx, +coq_ident)).\n')
for p in hyp_predc:
    writer.write(
        f':- modeb(*, hyp_node("{p}", +nat, -string, -hyp_idx, +coq_ident)).\n'
    )