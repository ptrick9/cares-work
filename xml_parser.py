import xml.etree.ElementTree as ET
import traceback

def xml_parse(f_name):
    try:
        tree = ET.parse('%s' % (f_name))
        root = tree.getroot()
        object = root.find('object')
        #name = object.find('name').text
        #print(name)
        box = []
        box.append(float(object.find('bndbox').find('xmin').text))
        box.append(float(object.find('bndbox').find('ymin').text))
        box.append(float(object.find('bndbox').find('xmax').text))
        box.append(float(object.find('bndbox').find('ymax').text))
        del tree
        return box
    except:
        print(f_name)
	print(traceback.format_exc())
        return None
