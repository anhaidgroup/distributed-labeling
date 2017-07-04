#!/usr/bin/env python
import pandas as pd
import json
import os
import sqlite3
from pandas.io import sql



sql_path = os.path.join(os.path.dirname(__file__), 'data/data.sqlite')
table_name = 'mfc_label'

def read_data(filename = sql_path, filter_label_str=None, l_prefix='ltable.', r_prefix='rtable.',
              id_col='_id', label_col='Label'):
    cnx = sqlite3.connect(sql_path)
    data = pd.read_sql('select * from mfc_label', con=cnx)
    #data = pd.read_csv(filename)
    if filter_label_str != None:
        filter_label_list = _parse_label_types(filter_label_str)
        data = data[data['Label'].isin(filter_label_list)]

    (ltable, rtable) = _process_data(data, l_prefix='ltable.', r_prefix='rtable.',
                  id_col='_id', label_col='Label')
    cols = list(ltable.columns)
    ltable = ltable.T.to_dict().values()
    rtable = rtable.T.to_dict().values()
    d = {}
    d['id'] = id_col
    d['columns'] = cols
    d['label'] = label_col
    d['ltable'] = ltable
    d['rtable'] = rtable
    return json.dumps(d)


def save_data(label_str, filename=sql_path, lid_col='ltable.DRUG_ID',
              rid_col='rtable.DRUG_ID', label_col='Label'):
    cnx = sqlite3.connect(sql_path)
    data = pd.read_sql('select * from mfc_label', con=cnx)
    ids_chopped = _parse_label_str(label_str)
    data = _update_tbl_labels(data, ids_chopped)

    #data.to_csv(sql_path, index=False)
    sql.to_sql(data, name='mfc_label', con=cnx, index=False, index_label='_id', if_exists='replace')
    #name=table_name, con=cnx, index=False, index_label='_id', if_exists='replace'



def _update_tbl_labels(data, ids_chopped):
    data.set_index('_id', drop=False, inplace=True)
    for ids in ids_chopped:
        idx, lid, rid, label = ids
        assert lid == data.ix[idx, 'ltable.DRUG_ID'], 'ltable drugids donot match'
        assert rid == data.ix[idx, 'rtable.DRUG_ID'], 'rtable drugids donot match'
        data.ix[idx, 'Label'] = label
    data.reset_index(drop=True, inplace=True)
    return data

def _parse_label_str(x):
    x = x.encode('ascii','ignore')
    x_splitted = map(str.strip, x.split(','))
    ids_chopped = [] # chop and convert to int
    for t in x_splitted:
        tmp = map(int, map(str.strip, t.split('_')))
        ids_chopped.append(tmp)
    return ids_chopped


def _parse_label_types(x):
    x = x.encode('ascii', 'ignore')
    x_splitted = map(int, map(str.strip, x.split(',')))
    return x_splitted

def _process_data(data, l_prefix='ltable.', r_prefix='rtable.',
                  id_col='_id', label_col='Label'):
    d1 = get_one_table_data(data, l_prefix, id_col, label_col)
    d2 = get_one_table_data(data, r_prefix, id_col, label_col)
    return (d1, d2)



def get_one_table_data(data, prefix='ltable.', id_col='_id', label_col='Label'):
    l = list(data.columns)
    cols = [x.startswith(tuple([prefix, id_col, label_col])) for x in l]


    req_cols = data.columns[cols]
    d = data[req_cols]
    if prefix+'NDC_CODE' in d.columns:
        d.drop(prefix+'NDC_CODE', inplace=True, axis=1)
    col_vals = remove_prefixes(d.columns, prefix)
    col_vals = replace_char(col_vals, '_', ' ', ['_id'])
    d.columns = col_vals
    return d


def remove_prefixes(cols, prefix):
    y = []
    for col in cols:
        if col.startswith(prefix):
            y.append(col[len(prefix):])
        else:
            y.append(col)
    return y

def replace_char(cols, old, new, exp_list):
    for idx in range(0, len(cols)):
        if cols[idx] not in exp_list:
            cols[idx] = cols[idx].replace(old, new)
    return cols


def get_summary(filename=sql_path):
    dlist = []
    # data = pd.read_csv(filename)
    cnx = sqlite3.connect(sql_path)
    data = pd.read_sql('select * from mfc_label', con=cnx)

    v = data.Label.values
    label_list = ['Unlabeled', 'User-Yes', 'User-No',
                  'User-Unsure', 'Expert-Yes', 'Expert-No', 'Expert-Unsure']
    for i in range(0, len(label_list)):
        cnt = sum(v == i)
        d = {}
        d['label'] = label_list[i]
        d['value'] = cnt
        dlist.append(d)
    dd = {}
    dd['foo'] = dlist
    dd = json.dumps(dd)
    return dd
