def eval_overlapp(L, W, l, w, a, b, c, d, f, e, g, h):
    v1_x = a * l
    v1_y = b * w

    v3_x = L - e * l
    v3_y = W - f * w

    v2_x = L - c * w
    v2_y = d * l

    v4_x = g * w
    v4_y = W - h * l

    if v3_x < v1_x and v3_y < v1_y:
        overlapp = True
    elif v4_x > v2_x and v4_y < v2_y:
        overlapp = True
    else:
        overlapp = False

    return overlapp


def overlapping_vertical_offset(new_position_boxes):
    result_groups_overlapp = []
    for a in range(4):
        for b in range(len(new_position_boxes[a + 1]['x'])):
            for c in range(len(new_position_boxes[1]['x'])):
                x1 = new_position_boxes[a + 1]['x'][b]
                y1 = new_position_boxes[a + 1]['y'][b]
                l1 = new_position_boxes[a + 1]['l'][b]
                a1 = new_position_boxes[a + 1]['a'][b]
                x2 = new_position_boxes[1]['x'][c]
                y2 = new_position_boxes[1]['y'][c]
                l2 = new_position_boxes[1]['l'][c]
                a2 = new_position_boxes[1]['a'][c]
                if a == 0 and x1 == x2 and y1 == y2 and l1 == l2 and a1 == a2:
                    continue
                else:
                    result = overlapping_box(x1, y1, l1, a1, x2, y2, l2, a2)
                    result_groups_overlapp.append(result)
            for c in range(len(new_position_boxes[2]['x'])):
                x1 = new_position_boxes[a + 1]['x'][b]
                y1 = new_position_boxes[a + 1]['y'][b]
                l1 = new_position_boxes[a + 1]['l'][b]
                a1 = new_position_boxes[a + 1]['a'][b]
                x2 = new_position_boxes[2]['x'][c]
                y2 = new_position_boxes[2]['y'][c]
                l2 = new_position_boxes[2]['l'][c]
                a2 = new_position_boxes[2]['a'][c]
                if a == 1 and x1 == x2 and y1 == y2 and l1 == l2 and a1 == a2:
                    continue
                else:
                    result = overlapping_box(x1, y1, l1, a1, x2, y2, l2, a2)
                    result_groups_overlapp.append(result)
            for c in range(len(new_position_boxes[3]['x'])):
                x1 = new_position_boxes[a + 1]['x'][b]
                y1 = new_position_boxes[a + 1]['y'][b]
                l1 = new_position_boxes[a + 1]['l'][b]
                a1 = new_position_boxes[a + 1]['a'][b]
                x2 = new_position_boxes[3]['x'][c]
                y2 = new_position_boxes[3]['y'][c]
                l2 = new_position_boxes[3]['l'][c]
                a2 = new_position_boxes[3]['a'][c]
                # print(f'x1:{x1},y1:{y1},l1:{l1},a1:{a1}')
                # print(f'x2:{x2},y2:{y2},l2:{l2},a2:{a2}')
                # print('a',a)
                if a == 2 and x1 == x2 and y1 == y2 and l1 == l2 and a1 == a2:
                    # print('si 1')
                    continue
                else:
                    result = overlapping_box(x1, y1, l1, a1, x2, y2, l2, a2)
                    # print('result',result)
                    result_groups_overlapp.append(result)
            for c in range(len(new_position_boxes[4]['x'])):
                x1 = new_position_boxes[a + 1]['x'][b]
                y1 = new_position_boxes[a + 1]['y'][b]
                l1 = new_position_boxes[a + 1]['l'][b]
                a1 = new_position_boxes[a + 1]['a'][b]
                x2 = new_position_boxes[4]['x'][c]
                y2 = new_position_boxes[4]['y'][c]
                l2 = new_position_boxes[4]['l'][c]
                a2 = new_position_boxes[4]['a'][c]
                # print(f'x1:{x1},y1:{y1},l1:{l1},a1:{a1}')
                # print(f'x2:{x2},y2:{y2},l2:{l2},a2:{a2}')
                # print('a',a)
                if a == 3 and x1 == x2 and y1 == y2 and l1 == l2 and a1 == a2:
                    # print('si 2')
                    continue
                else:
                    result = overlapping_box(x1, y1, l1, a1, x2, y2, l2, a2)
                    # print('result',result)
                    result_groups_overlapp.append(result)
    if len(set(result_groups_overlapp)) == 2:
        output = "Overlapp"
    else:
        output = "Good"
    return output


def overlapping_box(x1, y1, l1, a1, x2, y2, l2, a2):
    # if x2>=(x1+l1):
    # result = False
    # elif x2==x1 and y2>=y1+l1:
    # result = False
    # elif (x2+l2)<=x1:
    # result = False
    # elif x2==x1 and (y2+a2)==y1:
    # result = False
    # elif y2==y1 and (x2+l2)==x1:
    # result = False

    if x2 >= x1 and x2 < (x1 + l1) and y2 >= y1 and y2 < (y1 + a1):
        result = "Overlapp"
    elif x2 > x1 and x2 < (x1 + l1) and (y2 + a2) > y1 and (y2 + a2) < (y1 + a1):
        result = "Overlapp"
    elif (x2 + l2) > x1 and (x2 + l2) <= (x1 + l1) and (y2 + a2) > y1 and (y2 + a2) <= (y1 + a1):
        result = "Overlapp"
    elif (x2 + l2) > x1 and (x2 + l2) < (x1 + l1) and (y2) > y1 and (y2) < (y1 + a1):
        result = "Overlapp"
    else:
        result = "Good"

    return result
