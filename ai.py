import cv2
from numpy import *
import PIL.Image as I
from chainercv.links.model import faster_rcnn


def segmentation(input_image_path, output_image_path):
    model = faster_rcnn.FasterRCNNVGG16(pretrained_model='voc07')

    im_raw = I.open(input_image_path)
    w, h = im_raw.size
    r = h / w
    rgb = array(im_raw.resize((int(800), int(r * 800))).convert("RGB"))

    img = asarray(rgb, dtype = float32).transpose((2, 0, 1))
    bbox, c, acc = model.predict([img])
    for b in bbox[0]:
        y_min, x_min, y_max, x_max = b
        rgb  = cv2.rectangle(rgb, (x_min, y_min), (x_max, y_max), (255, 0, 0))
    I.fromarray(rgb).resize(im_raw.size).save(output_image_path)
    print("Prosess has been done successfully!")

