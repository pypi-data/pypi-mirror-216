import math


def Objfun(a, b, c, d, e, f, g, h, show=False):
    total_number_boxes = a * b + c * d + e * f + g * h

    if show == True:
        print("\n", "#" * 8,
              "The Objective function value for this arrange a:{},b:{},c:{},d:{},e:{},f:{},g:{},h:{} solution schedule is: {}".format(
                  a, b, c, d, e, f, g, h, total_number_boxes), "#" * 8)
    return total_number_boxes


def position_boxes(index, result_list, length_val, width_val, pallet_length, pallet_width):
    list_box_pos = []
    box_size = []

    d_m = index  # insert one value of the list above

    boxes = {1: {'x': [], 'y': [], 'l': [], 'a': []},
             2: {'x': [], 'y': [], 'l': [], 'a': []},
             3: {'x': [], 'y': [], 'l': [], 'a': []},
             4: {'x': [], 'y': [], 'l': [], 'a': []}}

    for z in range(4):
        if result_list[d_m][z * 2] == 0 or result_list[d_m][z * 2 + 1] == 0:
            pass
        else:
            if z == 0:
                for i in range(result_list[d_m][z * 2 + 1]):
                    for t in range(result_list[d_m][z * 2]):
                        # anchor_x=0+t*(length_val+4)
                        # anchor_y=0+i*(width_val+4)
                        anchor_x = 0 + t * (length_val)
                        anchor_y = 0 + i * (width_val)
                        list_box_pos.append((anchor_x, anchor_y))
                        box_size.append((length_val, width_val))
                        boxes[1]['x'].append(anchor_x)
                        boxes[1]['y'].append(anchor_y)
                        boxes[1]['l'].append(length_val)
                        boxes[1]['a'].append(width_val)

            elif z == 1:
                for i in range(result_list[d_m][z * 2 + 1]):
                    for t in range(result_list[d_m][z * 2]):
                        # anchor_x=(pallet_length-width_val)-t*(width_val+4)
                        # anchor_y=0+i*(length_val+4)
                        anchor_x = (pallet_length - width_val) - t * (width_val)
                        anchor_y = 0 + i * (length_val)
                        list_box_pos.append((anchor_x, anchor_y))
                        box_size.append((width_val, length_val))
                        boxes[2]['x'].append(anchor_x)
                        boxes[2]['y'].append(anchor_y)
                        boxes[2]['l'].append(width_val)
                        boxes[2]['a'].append(length_val)
            elif z == 2:
                for i in range(result_list[d_m][z * 2]):
                    for t in range(result_list[d_m][z * 2 + 1]):
                        # anchor_x=(pallet_length-length_val)-t*(length_val+4)
                        # anchor_y=(pallet_width-width_val)-i*(width_val+4)
                        anchor_x = (pallet_length - length_val) - t * (length_val)
                        anchor_y = (pallet_width - width_val) - i * (width_val)
                        list_box_pos.append((anchor_x, anchor_y))
                        box_size.append((length_val, width_val))
                        boxes[3]['x'].append(anchor_x)
                        boxes[3]['y'].append(anchor_y)
                        boxes[3]['l'].append(length_val)
                        boxes[3]['a'].append(width_val)
            elif z == 3:
                for i in range(result_list[d_m][z * 2]):
                    for t in range(result_list[d_m][z * 2 + 1]):
                        # anchor_x=0+i*(width_val+4)
                        # anchor_y=(pallet_width-length_val)-t*(length_val+4)
                        anchor_x = 0 + i * (width_val)
                        anchor_y = (pallet_width - length_val) - t * (length_val)
                        list_box_pos.append((anchor_x, anchor_y))
                        box_size.append((width_val, length_val))
                        boxes[4]['x'].append(anchor_x)
                        boxes[4]['y'].append(anchor_y)
                        boxes[4]['l'].append(width_val)
                        boxes[4]['a'].append(length_val)
    return list_box_pos, boxes, box_size


def var_less_equal(a, b):
    val_in = int(math.floor(a / b))
    return val_in
