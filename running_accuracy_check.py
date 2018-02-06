from IOU import IOU
from darknet import *
from get_files import *
from xml_parser import *
import random
import pickle

meta= load_meta("cfg/custom.data")
#net = load_net("cfg/tiny-yolo-size.cfg", "custom_size_final.weights", 0)
#net = load_net("cfg/tiny-yolo-voc-1-1.cfg", "tiny-yolo-voc-1-1_130000.weights", 0)
#net = load_net("cfg/tiny-yolo-voc-reduction.cfg", "tiny-yolo-voc-reduction_110000.weights", 0)
net = load_net("cfg/tiny-yolo-voc-custom-size-anchors.cfg", "tiny-yolo-voc-reduction-anchor_120000.weights", 0)
#net = load_net("cfg/tiny-yolo-voc-reduction-384x192.cfg", "tiny-yolo-voc-reduction-384x192_20000.weights", 0)
files = get_base_name_files_in_folder('/home/nvidia/validation_set')
random.shuffle(files)

scores = []
data = []
miss = 0.0
for i, file in enumerate(files):
    box = xml_parse("%s.xml" % file)
    r = detect(net, meta, "%s.jpg" % file, .01)
    #print(file, r)
    result = [0, 0, 0, 0]
    iou_score = 0.0
    try:
        width = r[0][2][2] / 2
        height = r[0][2][3] / 2
        result[0] = r[0][2][0] - width  # xmin
        result[2] = r[0][2][0] + width  # xmax
        result[1] = r[0][2][1] - height  # ymin
        result[3] = r[0][2][1] + height  # ymax
        iou_score = IOU(box, result)
    except:
        miss += 1.0
    data.append([file.split('/')[-1], iou_score, result])
    #print(data[-1])
    scores.append(iou_score)
    if i % 100 == 0 and i != 0:
        print("average @ %d images: %f no_object: %f" % (i, float(sum(scores)/len(scores)), float(miss/i)))
	
f = open('statistics', 'wb')
pickle.dump(data, f)
f.close()
