#!/usr/bin/env python3
import xml.etree.ElementTree as ET
def color16(x):
    return ((x >> 8) & 0xf800) | ((x >> 5) & 0x07e0) | ((x >> 3) & 0x001f)

def get_rectangles_from_svg(svg_file_path):
    tree = ET.parse(svg_file_path)
    root = tree.getroot()

    # SVG namespaces can be present, so we need to handle them
    # A common SVG namespace is "http://www.w3.org/2000/svg"
    namespace = {'svg': 'http://www.w3.org/2000/svg'}

    # Find all <rect> elements
    r = []
    xc, yc = -1, -1
    for rect_element in root.findall('.//svg:rect', namespace):
        x = int(float(rect_element.get('x', 0)))
        y = int(float(rect_element.get('y', 0)))
        if xc < 0:
            xc, yc = x, y
            r.append(1)
        else:
            r.append(0)

        w = int(float(rect_element.get('width', 0)))
        h = int(float(rect_element.get('height', 0)))
        c = color16(int(rect_element.get('style', 0).split(';')[0].split(":")[1][1:], 16))
        r.append(x-xc)
        r.append(y-yc)
        r.append(w)
        r.append(h)
        r.append(c)
    return r

# Example usage:
r = get_rectangles_from_svg('asteroid.svg')
i = 0
print("[")
while i < len(r):
    n = map(str, r[i:i+6])
    print("    "+",".join(map(str, r[i:i+6]))+",")
#    print(",".join(r[i:i+5]))
    i += 6
print("]")
