# from https://www.programmersought.com/article/39744038966/
import os
import xml.etree.ElementTree as ET

dirpath = r'G:/Git/Lazuli-Cross-Object-Detection-Dataset/labels/val'  # The directory where the xml file was originally stored
newdir = r'G:/Git/Lazuli-Cross-Object-Detection-Dataset/labels/val'  # The txt directory formed after modifying the label

if not os.path.exists(newdir):
    os.makedirs(newdir)

dict_info = {'Undefined Area': 0,
             'High GSM': 1,
             'Low GSM': 2}
# There are several attributes fill in several

for fp in os.listdir(dirpath):
    if fp.endswith('.xml'):
        root = ET.parse(os.path.join(dirpath, fp)).getroot()

        xmin, ymin, xmax, ymax = 0, 0, 0, 0
        sz = root.find('size')
        width = float(sz[0].text)
        height = float(sz[1].text)
        filename = root.find('filename').text
        for child in root.findall('object'):  # Find all the boxes in the picture

            sub = child.find('bndbox')  # Find the label value of the box and read it
            label = child.find('name').text
            label_ = dict_info.get(label)
            if label_:
                label_ = label_
            else:
                label_ = 0
            xmin = float(sub[0].text)
            ymin = float(sub[1].text)
            xmax = float(sub[2].text)
            ymax = float(sub[3].text)
            try:  # Convert to yolov3's label format, which needs to be normalized to (0-1)
                x_center = (xmin + xmax) / (2 * width)
                x_center = '%.6f' % x_center
                y_center = (ymin + ymax) / (2 * height)
                y_center = '%.6f' % y_center
                w = (xmax - xmin) / width
                w = '%.6f' % w
                h = (ymax - ymin) / height
                h = '%.6f' % h
            except ZeroDivisionError:
                print(filename, 'There is a problem with the width')
            with open(os.path.join(newdir, fp.split('.xml')[0] + '.txt'), 'a+') as f:
                f.write(' '.join([str(label_), str(x_center), str(y_center), str(w), str(h) + '\n']))
print('ok')
