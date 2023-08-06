"""all kinds of convertings between data formats
"""
import zlib
import pickle
import lz4.frame



def obj_to_bin(obj,compress_level=1):
    """pickle python object to binary

    Args:
        obj (Any): any python object
        compress_level (int): 0-10, compress level, 
        if 0-1 then use lz4
    Returns:
        bin: binary
    Speed-time Trade offs:
        example 10000 images,
        * lz4:                 4s,   455MB
        * zlib lvl1:           12s,  306MB
        * zlib lvl6 (default): 39s,  260M
        * zlib lvl9:           125s, 240MB
    Examples:
        * save object to local
            bytes_to_file(obj_to_bin(data_export,compress_level=0.5),export_path)
    """
    pickled_data = pickle.dumps(obj)
    if compress_level == 0:
        pass
    elif compress_level < 1: 
        pickled_data = lz4.frame.compress(pickled_data)
    else:
        pickled_data = zlib.compress(pickled_data, level = compress_level)
    return pickled_data

def bin_to_obj(bin,decompress_algo='zlib'):
    """
    unpickle binary back to python object
    """
    if decompress_algo == 'zlib':
        depressed_pickle = zlib.decompress(bin)
    elif decompress_algo == '':
        depressed_pickle = bin
    elif decompress_algo == 'lz4':
        depressed_pickle = lz4.frame.compress(bin)
    obj = pickle.loads(depressed_pickle)
    return obj

def bytes_to_file(bytes,save_path):
    with open(save_path, 'wb') as f:
        f.write(bytes)

def file_to_bytes(path):
    with open(path,'rb') as f:
        byte = f.read()
    return byte