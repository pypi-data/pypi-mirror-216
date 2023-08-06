"""
image signal processings
"""
import cv2
import base64
import numpy as np


def img_to_b64str(img, mode='jpg',quality=95):
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    if mode == 'jpg':
        return base64.b64encode(cv2.imencode(
            '.jpg',
            img,
            encode_param)[1]).decode()
    if mode == 'png':
        return base64.b64encode(cv2.imencode(
            '.png',
            img)[1]).decode()     

def b64str_to_img(string):
    jpg_original = base64.b64decode(string)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)
    return img



def sim_img_artifact(img, quality, mode="jpg"):
    """ compress image and reload to give image compress aritfact

    Args:
        img (_type_): _description_
        jpg_compress_rate (_type_): _description_

    Returns:
        _type_: _description_
    """
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    _, encimg = cv2.imencode('.jpg', img, encode_param)
    im = cv2.imdecode(encimg, 0)
    return im