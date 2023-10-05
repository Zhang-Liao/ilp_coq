import glob
import os
import stat_filter

num_of_test = 10
test_dir = '/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/origin_feat/2percent_split'

for i in range(num_of_test):
    test_i = os.path.join(test_dir, f'test{i}')

    pred = os.path.join(test_dir, f'test{i}.eval')
    label = os.path.join(test_dir, f'test{i}.label')    

    for test_time in os.listdir(test_i):
        curr_dir = os.path.join(test_i, test_time) 
        reorder = os.path.join(curr_dir, f'reorder/test{i}.eval')
        good = os.path.join(curr_dir, f'good/test{i}.eval')

        stat_filter.stat(good, label, pred, reorder)
        
    # reorder = glob.glob(os.path.join(curr_dir, f'*/reorder/test{i}.eval'))
    # print(curr_dir)
    # print(os.path.join(curr_dir, f'*/reorder/test{i}.eval'))
    # print(reorder)
    # exit()
    # assert len(reorder) == 1
    # good = glob.glob(os.path.join(curr_dir, f'/*/good/test{i}.eval'))
    # assert len(good) == 1
    # pred = os.path.join(curr_dir, f'test{i}.eval')
    # label = os.path.join(curr_dir, f'test{i}.label')    
        
