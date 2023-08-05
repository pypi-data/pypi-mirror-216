import numpy as np

def get_euclidean_distance(p1, p2):
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def overlap(rect1, rect2):
    # rect1 and rect2 are tuples in the form ((x1, y1), (x2, y2))
    # representing the upper left and lower right points of each rectangle

    upper1, lower1 = rect1
    upper2, lower2 = rect2
    
    return lower1[0] >= upper2[0] and upper1[0] <= lower2[0] and lower1[1] >= upper2[1] and upper1[1] <= lower2[1]  

def get_bounding_box(rect1, rect2):
    # rect1 and rect2 are tuples in the form ((x1, y1), (x2, y2))
    # representing the upper left and lower right points of each rectangle

    upper_left = np.array((min(rect1[0][0], rect2[0][0]), min(rect1[0][1], rect2[0][1])))
    lower_right = np.array((max(rect1[1][0], rect2[1][0]), max(rect1[1][1], rect2[1][1])))

    return np.array((upper_left, lower_right))

def get_rect_distance(upper_a, lower_a, upper_b, lower_b):
    x1, y1 = upper_a
    x1b, y1b = lower_a
    x2, y2 = upper_b
    x2b, y2b = lower_b

    left = x2b < x1
    right = x1b < x2
    bottom = y2b < y1
    top = y1b < y2
    if top and left:
        return get_euclidean_distance((x1, y1b), (x2b, y2))
    elif left and bottom:
        return get_euclidean_distance((x1, y1), (x2b, y2b))
    elif bottom and right:
        return get_euclidean_distance((x1b, y1), (x2, y2b))
    elif right and top:
        return get_euclidean_distance((x1b, y1b), (x2, y2))
    elif left:
        return x1 - x2b
    elif right:
        return x2 - x1b
    elif bottom:
        return y1 - y2b
    elif top:
        return y2 - y1b
    else:             # rectangles intersect
        return 0.

def crop_image(img, startx, starty, endx, endy):
    """
    @param img array of image
    @param startx
    @param starty
    @param endx 
    @param endy
    @returns a cropped image of img[startx:endx, starty:endy] 
    """
    h, w, _ = img.shape

    startx = max(0, startx)
    starty = max(0, starty)

    endx = min(endx, w)
    endy = min(endy, h)
    
    return img[starty:endy, startx:endx]