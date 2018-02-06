

def collide(a, b):
    if a[0] >= b[0] and a[0] <= b[2]:
        if a[1] >= b[1] and a[1] <= b[3]:
            return True
        if a[3] >= b[1] and a[3] <= b[3]:
            return True
    if a[2] >= b[0] and a[0] <= b[2]:
        if a[1] >= b[1] and a[1] <= b[3]:
            return True
        if a[3] >= b[1] and a[3] <= b[3]:
            return True

    if b[0] >= a[0] and b[0] <= a[2]:
        if b[1] >= a[1] and b[1] <= a[3]:
            return True
        if b[3] >= a[1] and b[3] <= a[3]:
            return True
    if b[2] >= a[0] and b[0] <= a[2]:
        if b[1] >= a[1] and b[1] <= a[3]:
            return True
        if b[3] >= a[1] and b[3] <= a[3]:
            return True
    return False


def IOU(truth, propose):
    if collide(truth, propose):
        xmin = max(truth[0], propose[0])
        ymin = max(truth[1], propose[1])
        xmax = min(truth[2], propose[2])
        ymax = min(truth[3], propose[3])

        intersection = (xmax-xmin+1)*(ymax-ymin+1)

        truthArea = (truth[2]-truth[0]+1)*(truth[3]-truth[1]+1)
        proposedArea = (propose[2]-propose[0]+1)*(propose[3]-propose[1]+1)

        union = truthArea + proposedArea - intersection

        return float(intersection/union)
    return 0.0