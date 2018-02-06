from xml_parser import xml_parse
from IOU import IOU
from get_files import get_files_in_folder

files = get_files_in_folder('truth')

print(files)
scores = []
for file in files:
    end = file.split('/')[-1]
    print(file)
    print(end)
    truth_box = xml_parse('%s.xml' % file)
    propose = xml_parse('test_images/result/xml/CARES/%s.xml' % (end))
    print(truth_box)
    print(propose)
    scores.append(IOU(truth_box, propose))
print(float(sum(scores)/len(scores)))
