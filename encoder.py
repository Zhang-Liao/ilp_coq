import joblib

from sklearn.preprocessing import LabelEncoder

label_encoder = joblib.load('/home/zhangliao/ilp_out_coq/ilp_out_coq/data/json/neg/ten_split/label_encoder.gz')

assert(isinstance(label_encoder, LabelEncoder))

id = label_encoder.transform(['simpl'])
print(id[0])