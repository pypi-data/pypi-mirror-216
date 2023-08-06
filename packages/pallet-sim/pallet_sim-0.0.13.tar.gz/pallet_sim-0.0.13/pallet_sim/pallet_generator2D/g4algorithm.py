import itertools
from .boxprocessing import Objfun, position_boxes
from .lists import list_a, list_b, value_c, list_d, value_f, list_e, value_g, value_h
from .overlapp import eval_overlapp, overlapping_vertical_offset
from .box_offset import vertical_and_horizontal_offset


def algorithm_artikel(length_val: int, width_val: int, height_val: int, pallet_length: int, pallet_width: int,
                      filter_rotation: bool = False) -> dict:
    # ensure that the length of the box is greater than its width and that the length of the pallet is greater than
    # its width
    if length_val < width_val:
        length_val, width_val = width_val, length_val
    if pallet_length < pallet_width:
        pallet_length, pallet_width = pallet_width, pallet_length

    box_size = {
        "length_box": length_val,
        "width_box": width_val,
        "height_box": height_val
    }
    pallet_size = {
        "length_pallet": pallet_length,
        "width_pallet": pallet_width
    }
    b_type_layer = {
        "height": box_size.get('height_box'),
        "length": box_size.get('length_box'),
        "width": box_size.get('width_box')
    }

    m_p = pallet_size.get('length_pallet')
    n_p = pallet_size.get('width_pallet')
    k_b = b_type_layer.get('length')
    i_b = b_type_layer.get('width')

    # print(k_b)
    # print(i_b)
    # print(m_p)
    # print(n_p)

    l_a = list_a(m_p, n_p, k_b, i_b)
    l_b = list_b(m_p, n_p, k_b, i_b)
    a_b = [l_a, l_b]
    list_a_b = list(itertools.product(*a_b))

    list(map(lambda x: value_c(m_p, n_p, k_b, i_b, x[0]), list_a_b))

    list_a_b_c = [e + tuple([value_c(m_p, n_p, k_b, i_b, e[0])]) for e in list_a_b]

    list_a_b_c_d = []
    for x in range(len(list_a_b_c)):
        l_d = list_d(m_p, n_p, k_b, i_b, list_a_b_c[x][1])
        l_d = [(x,) for x in l_d]
        list_inter1 = list(list_a_b_c[x])
        list_inter2 = [tuple(list_inter1) + e for e in l_d]
        list_a_b_c_d = list_a_b_c_d + list_inter2

    list_a_b_c_d_f = [e + tuple([value_f(m_p, n_p, k_b, i_b, e[3])]) for e in list_a_b_c_d]

    list_a_b_c_d_f_e = []
    for x in range(len(list_a_b_c_d_f)):
        l_d = list_e(m_p, n_p, k_b, i_b, list_a_b_c_d_f[x][2])
        l_d = [(x,) for x in l_d]
        list_inter1 = list(list_a_b_c_d_f[x])
        list_inter2 = [tuple(list_inter1) + e for e in l_d]
        list_a_b_c_d_f_e = list_a_b_c_d_f_e + list_inter2

    list_a_b_c_d_f_e_g = [e + tuple([value_g(m_p, n_p, k_b, i_b, e[5])]) for e in list_a_b_c_d_f_e]

    list_a_b_c_d_f_e_g_h = [e + tuple([value_h(m_p, n_p, k_b, i_b, e[1])]) for e in list_a_b_c_d_f_e_g]

    result_list = []

    for x in range(len(list_a_b_c_d_f_e_g_h)):
        # overlapp=True
        a = list_a_b_c_d_f_e_g_h[x][0]
        b = list_a_b_c_d_f_e_g_h[x][1]
        c = list_a_b_c_d_f_e_g_h[x][2]
        d = list_a_b_c_d_f_e_g_h[x][3]
        f = list_a_b_c_d_f_e_g_h[x][4]
        e = list_a_b_c_d_f_e_g_h[x][5]
        g = list_a_b_c_d_f_e_g_h[x][6]
        h = list_a_b_c_d_f_e_g_h[x][7]

        overlapp_val = eval_overlapp(m_p, n_p, k_b, i_b, a, b, c, d, f, e, g, h)

        if not overlapp_val:
            result_list = result_list + [list_a_b_c_d_f_e_g_h[x]]

    n_boxes = []
    for x in range(len(result_list)):
        a = result_list[x][0]
        b = result_list[x][1]
        c = result_list[x][2]
        d = result_list[x][3]
        f = result_list[x][4]
        e = result_list[x][5]
        g = result_list[x][6]
        h = result_list[x][7]
        n_boxes.append(Objfun(a, b, c, d, e, f, g, h, show=False))

    max_value = max(n_boxes)
    max_indexes = [i for i, j in enumerate(n_boxes) if j == max_value]
    # print(max_indexes)

    non_repeating_groups_boxes = []
    return_list = []
    for w in range(0, len(max_indexes)):
        # print(max_indexes[w])
        list_box_pos, boxes, box_size = position_boxes(max_indexes[w], result_list, length_val, width_val,
                                                       pallet_length, pallet_width)

        # print(boxes)
        # reset_global_variables()
        new_position_boxes = vertical_and_horizontal_offset(boxes, m_p, n_p, k_b, i_b)

        result = overlapping_vertical_offset(new_position_boxes)

        if result != 'Overlapp':
            list_box_pos2 = []
            for a in range(4):
                for b in range(len(boxes[a + 1]['x'])):
                    list_box_pos2.append((new_position_boxes[a + 1]['x'][b], new_position_boxes[a + 1]['y'][b]))

            # sort the list and box size to filter out same pallet but different order the sorting is done is parallel
            # so the index of the list_box_pos2 and box_size will be the same for each box
            list_box_pos2, box_size = (list(t) for t in zip(*sorted(zip(list_box_pos2, box_size))))

            if list_box_pos2 in non_repeating_groups_boxes:
                continue
            else:
                non_repeating_groups_boxes.append(list_box_pos2)
                return_list.append((list_box_pos2, box_size))

    if filter_rotation:
        # flip each box per pallet by 180 degree 0,0 becomes length - box length and width - box width and vice versa
        # then order the new configuration and check if it is already in the list if it is then remove it
        # this will remove the same pallet but with different rotation
        filtered_return_list = []
        for boxes_pos, box_size in return_list:
            new_boxes_pos = [(pallet_length - x[0] - box_size[i][0], pallet_width - x[1] - box_size[i][1]) for i, x in
                             enumerate(boxes_pos)]
            new_boxes_pos, new_box_size = (list(t) for t in zip(*sorted(zip(new_boxes_pos, box_size))))
            for boxes_pos2, box_size2 in filtered_return_list:
                if new_boxes_pos == boxes_pos2 and new_box_size == box_size2:
                    break
            else:
                filtered_return_list.append((boxes_pos, box_size))
        return_list = filtered_return_list

    return {
        'pallets': return_list,
        'pallet_size': (pallet_length, pallet_width),
    }
