import lmdb
import cv2
from tqdm import tqdm
import numpy as np
import lmdb
import os
import pickle
import zlib

###### LMDB IO ######
# NOTICE: LMDB is not space efficent if per line data is less than 10K, 

def export_lmdb(data_list, export_path, encoder, batch_size=1000):
    """
    encode list of dicts into lmdb file at export_path,
    dict keys can not contain '_'
    if dict key includes 'img', img will be encoded using jpg.
    other keys should have values that's encodeable.
    """
    cache = {}
    cnt = 1
    def write_cache(env, cache):
        with env.begin(write=True) as txn:
            for k, v in cache.items():
                txn.put(k, v)
    
    os.makedirs(export_path, exist_ok=True)
    env = lmdb.open(export_path, map_size=2**40)
    for i, data in enumerate(data_list):
        data_id = str(i).zfill(13)
        data = encoder(data)
        for key,value in data.items():
            if "_" in key:
                raise ValueError("_ can not be in key, to avoid loading errors")
            cache[f"{data_id}_{key}".encode('utf-8')] = value

        # dump batch
        if cnt % batch_size == 0:
            write_cache(env, cache)
            cache = {}
        cnt += 1
    write_cache(env, cache)
    env.close()


def import_lmdb(data_dir,decoder):
    """
    Load lmdb into list of dict, suitable for projects that single lmdb can fit into memory.
    
    Args:
        data_dir (string): path to lmdb dir

    Returns:
        list of dict: recovered data
    """

    # init dataloader
    lmdb_env = lmdb.open(data_dir)
    lmdb_txn = lmdb_env.begin()
    lmdb_cursor = lmdb_txn.cursor()

    # start loading
    data_list = []
    current_data_id = ""
    for key, value in lmdb_cursor:
        data_id,key = key.decode().split("_")
        
        if data_id != current_data_id: # new data line
            if current_data_id:
                data = decoder(data)
                data_list.append(data)
            current_data_id = data_id
            data = {}
        data[key] = value
    # last line
    data_list.append(data)
    return data_list

# smart encoder/decoder

def smart_encode_from_key(data_dict, img_quality=95):
    """encode dict of various types into dict of bytes, automatically detect:
    * numpy images: dict key should contain img

    Args:
        data_dict (dict): input data, dict of encodeables or numpy images
    Returns:
        list of dict: recovered data, dict of bytes
    """
    encoded_dict = {}
    for key,value in data_dict.items():
        if 'img' in key:
            value = cv2.imencode('.jpg',value,
                                     [int(cv2.IMWRITE_JPEG_QUALITY), img_quality])[1]
            encoded_dict[key] = value
        else:
            encoded_dict[key]=value.encode('utf-8')

    return encoded_dict

def smart_decode_from_key(data_dict):
    """decode dict of various types of bytes into original format, automatically detect:
    * numpy images: dict key should contain img

    Args:
        data_dict (dict): input data, dict of bytes
    Returns:
        list of dict: recovered data, dict of original data
    """
    decoded_dict = {}
    for key,value in data_dict.items():
        if 'img' in key:
            decoded_dict[key] = np.frombuffer(value, dtype=np.uint8)
            decoded_dict[key] = cv2.imdecode(decoded_dict[key], flags=1)
        else:
            decoded_dict[key]=value.decode()

    return decoded_dict

# generalized encoder/decoder




# msgpack
import msgpack
import msgpack_numpy as msg_np

def serialize_message(message):
    ser_message = msgpack.dumps(message)
    return ser_message

def deserialize_message(message):
    des_message = msgpack.loads(message)
    return des_message

def serialize_np(arr):
    """
    fast serialize np array into latin string
    """
    return msgpack.packb(arr, default=msg_np.encode).decode('latin-1')

def deserialize_np(arr):
    """
    fast serialize np array into latin string
    """
    return msgpack.unpackb(arr.encode('latin-1'), object_hook=msg_np.decode)

### notes



# def main(args):
#     # parse task ids
#     tasks = [line.strip() for line in open(args.batch_image_id_csv).readlines()]
#     batchs = as_batchs(tasks, batch_size=256)

#     env = lmdb.open(args.db_path, map_size=int(1e12))
#     metas = []
#     for res in p_umap(partial(process_cb, args), batchs, num_cpus=args.workers):
#         txn = env.begin(write=True)
#         for meta, data in res:
#             txn.put(meta['uuid'].encode('utf-8'), data)
#             metas.append(meta)
#         txn.commit()
#     env.close()
#     df = pd.DataFrame(metas, columns=metas[0].keys())
#     df.to_csv(args.index_path, index=False)
#     print(f'done, total: {len(metas)}')

def save_list_of_dict_to_lmdb(data_list, export_path, batch_size=10000,img_quality=95):
    """
    encode list of dicts into lmdb file at export_path,
    dict keys can not contain '_'
    if dict key includes 'img', img will be encoded using jpg.
    other keys should have values that's encodeable.
    """
    cache = {}
    cnt = 1
    def write_cache(env, cache):
        with env.begin(write=True) as txn:
            for k, v in cache.items():
                txn.put(k, v)
    
    os.makedirs(export_path, exist_ok=True)
    env = lmdb.open(export_path, map_size=2**40)
    for i, data in enumerate(tqdm(data_list)):
        data_id = data['id']
        for key,value in data.items():
            if "_" in key:
                raise ValueError("_ can not be in key, to avoid loading errors")
            if 'img' in key:
                value = cv2.imencode('.jpg',value,
                                     [int(cv2.IMWRITE_JPEG_QUALITY), img_quality])[1]
                cache[f"{data_id}_{key}".encode('utf-8')] = value
            else:
                cache[f"{data_id}_{key}".encode('utf-8')]=value.encode('utf-8')
    
        # dump batch
        if cnt % batch_size == 0:
            write_cache(env, cache)
            cache = {}
        cnt += 1
    write_cache(env, cache)
    env.close()

