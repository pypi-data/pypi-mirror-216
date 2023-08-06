def vertical_and_horizontal_offset(boxes, pallet_length, pallet_width, length_val, width_val):
    # print('list of boxes', boxes)

    box_v_moved_g1 = []
    box_v_moved_g2 = []
    box_v_moved_g3 = []
    box_v_moved_g4 = []

    # print(nb_rows_G1)
    if 'nb_rows_G1' in locals(): del nb_rows_G1
    if 'nb_columns_G1' in locals(): del nb_columns_G1
    if 'height_von_level_G1' in locals(): del height_von_level_G1

    if 'nb_rows_G2' in locals(): del nb_rows_G2
    if 'nb_columns_G2' in locals(): del nb_columns_G2
    if 'height_von_level_G2' in locals(): del height_von_level_G2

    if 'nb_rows_G3' in locals(): del nb_rows_G3
    if 'nb_columns_G3' in locals(): del nb_columns_G3
    if 'height_von_level_G3' in locals(): del height_von_level_G3

    if 'nb_rows_G4' in locals(): del nb_rows_G4
    if 'nb_columns_G4' in locals(): del nb_columns_G4
    if 'height_von_level_G4' in locals(): del height_von_level_G4

    if 'val_start_col_4' in locals(): del val_start_col_4
    if 'val_start_col_3' in locals(): del val_start_col_3

    if 'boxes_to_compare_g1' in locals(): del boxes_to_compare_g1

    if 'val1_to_compare' in locals(): del val1_to_compare
    if 'val2_to_compare' in locals(): del val2_to_compare

    for li in range(1):
        if li == 0 and len(boxes[1]['x']) != 0:
            nb_rows_G1 = nb_rows_G1 if 'nb_rows_G1' in locals() else len(set(boxes[1]['y']))
            nb_columns_G1 = nb_columns_G1 if 'nb_columns_G1' in locals() else len(set(boxes[1]['x']))
            height_von_level_G1 = height_von_level_G1 if 'height_von_level_G1' in locals() else max(boxes[1]['y'])

            if len(boxes[4]['x']) != 0:
                nb_rows_G4 = nb_rows_G4 if 'nb_rows_G4' in locals() else len(set(boxes[4]['y']))
                nb_columns_G4 = nb_columns_G4 if 'nb_columns_G4' in locals() else len(set(boxes[4]['x']))
                height_von_level_G4 = height_von_level_G4 if 'height_von_level_G4' in locals() else min(boxes[4]['y'])

                if len(boxes[3]['x']) != 0:
                    nb_rows_G3 = nb_rows_G3 if 'nb_rows_G3' in locals() else len(set(boxes[3]['y']))
                    nb_columns_G3 = nb_columns_G3 if 'nb_columns_G3' in locals() else len(set(boxes[3]['x']))
                    height_von_level_G3 = height_von_level_G3 if 'height_von_level_G3' in locals() else min(
                        boxes[3]['y'])

                    boxes_to_compare_g1 = []
                    for q in range(nb_columns_G4):
                        boxes_to_compare_g1.append((boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * q],
                                                    boxes[4]['y'][nb_rows_G4 - 1 + nb_rows_G4 * q], 4, 0))
                    for c in range(nb_columns_G3):
                        boxes_to_compare_g1.append((boxes[3]['x'][nb_columns_G3 * (nb_rows_G3) - 1 - 1 * c],
                                                    boxes[3]['y'][nb_columns_G3 * (nb_rows_G3) - 1 - 1 * c], 3, 0))
                else:
                    boxes_to_compare_g1 = []
                    for q in range(nb_columns_G4):
                        boxes_to_compare_g1.append((boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * q],
                                                    boxes[4]['y'][nb_rows_G4 - 1 + nb_rows_G4 * q], 4, 0))
            elif len(boxes[3]['x']) != 0:
                nb_rows_G3 = nb_rows_G3 if 'nb_rows_G3' in locals() else len(set(boxes[3]['y']))
                nb_columns_G3 = nb_columns_G3 if 'nb_columns_G3' in locals() else len(set(boxes[3]['x']))
                height_von_level_G3 = height_von_level_G3 if 'height_von_level_G3' in locals() else min(boxes[3]['y'])

                boxes_to_compare_g1 = []
                for c in range(nb_columns_G3):
                    boxes_to_compare_g1.append((boxes[3]['x'][nb_columns_G3 * (nb_rows_G3) - 1 - 1 * c],
                                                boxes[3]['y'][nb_columns_G3 * (nb_rows_G3) - 1 - 1 * c], 3, 0))
            else:
                boxes_to_compare_g1 = []
            if len(boxes_to_compare_g1) != 0:

                columns_moved_G1 = int(len(box_v_moved_g1) / (nb_rows_G1 - 1)) if len(
                    box_v_moved_g1) > nb_columns_G1 else len(box_v_moved_g1)

                if 'nb_columns_G4' in locals():
                    columns_moved_G4 = int(len(box_v_moved_g4) / (nb_rows_G4 - 1)) if len(
                        box_v_moved_g4) > nb_columns_G4 else len(box_v_moved_g4)
                else:
                    columns_moved_G4 = 0
                for b in range(nb_columns_G1 - columns_moved_G1):
                    boxes_above = []
                    start = False
                    for c in range(len(boxes_to_compare_g1)):
                        if boxes_to_compare_g1[c][2] == 4:

                            list1 = [columns_moved_G1 * length_val + b * length_val,
                                     columns_moved_G1 * length_val + b * length_val + length_val]
                            list2 = [boxes_to_compare_g1[c][0], boxes_to_compare_g1[c][0] + width_val]
                            if list1[1] > list2[0] and list2[1] > list1[0]:
                                boxes_above.append(boxes_to_compare_g1[c])

                        if boxes_to_compare_g1[c][2] == 3:
                            list1 = [columns_moved_G1 * length_val + b * length_val,
                                     columns_moved_G1 * length_val + b * length_val + length_val]
                            list2 = [boxes_to_compare_g1[c][0], boxes_to_compare_g1[c][0] + length_val]
                            if list1[1] > list2[0] and list2[1] > list1[0]:
                                boxes_above.append(boxes_to_compare_g1[c])

                    groups = [c[2] for c in boxes_above]
                    if len(set(groups)) == 2:

                        values_y = [a[1] for a in boxes_above]
                        boxes_min_height = [a for a in boxes_above if a[1] == min(values_y)]
                        boxes_not_yet_vm = [t for t in boxes_min_height if t[3] == 0]
                        if len(boxes_not_yet_vm) == 0:
                            hole_distance = boxes_min_height[0][1] - (height_von_level_G1 + width_val)
                            space_in_sections = hole_distance / (nb_rows_G1 - 1 + 1)
                            for n in range(1, nb_rows_G1):
                                boxes[1]['y'][nb_columns_G1 * n + b * 1 + columns_moved_G1] = boxes[1]['y'][
                                                                                                  nb_columns_G1 * n + b * 1 + columns_moved_G1] + space_in_sections * n

                                box_v_moved_g1.append(nb_columns_G1 * n + b * 1 + columns_moved_G1)

                            columns_not_yet_moved = [a for a in boxes_above if
                                                     a[3] == 0 and a[2] == boxes_min_height[0][2]]
                            if len(columns_not_yet_moved) > 0:
                                hole_distance = columns_not_yet_moved[0][1] - (boxes[1]['y'][nb_columns_G1 * (
                                        nb_rows_G1 - 1) + b * 1 + columns_moved_G1] + width_val)
                                if boxes_min_height[0][2] == 4 and b != nb_columns_G1 - columns_moved_G1 - 1:
                                    space_in_sections = hole_distance / (nb_rows_G4 - 1 + 1)
                                    val_start_col_4 = val_start_col_4 if 'val_start_col_4' in locals() and val_start_col_4 > 0 else 0
                                    for q in range(len(columns_not_yet_moved)):
                                        for j in range(nb_rows_G4 - 1):
                                            boxes[4]['y'][nb_rows_G4 - 1 - j + nb_rows_G4 * q + val_start_col_4] = \
                                                boxes[4]['y'][
                                                    nb_rows_G4 - 1 - j + nb_rows_G4 * q + val_start_col_4] - space_in_sections * (
                                                        nb_rows_G4 - 1 - j)
                                            box_v_moved_g4.append(nb_rows_G4 - 1 - j + nb_rows_G4 * q + val_start_col_4)
                                            if j == 0:
                                                result = [idx for idx, tup in enumerate(boxes_to_compare_g1) if
                                                          tup in {columns_not_yet_moved[q]}]
                                                boxes_to_compare_g1[result[0]] = (boxes_to_compare_g1[result[0]][0],
                                                                                  boxes[4]['y'][
                                                                                      nb_rows_G4 - 1 - j + nb_rows_G4 * q + val_start_col_4],
                                                                                  boxes_to_compare_g1[result[0]][2],
                                                                                  boxes_to_compare_g1[result[0]][3])

                                    val_start_col_4 = val_start_col_4 + nb_rows_G4 * len(boxes_above_closest)
                                    set_list = set(columns_not_yet_moved)
                                    result = [idx for idx, tup in enumerate(boxes_to_compare_g1) if tup in set_list]
                                    for t in result:
                                        boxes_to_compare_g1[t] = (
                                            boxes_to_compare_g1[t][0], boxes_to_compare_g1[t][1],
                                            boxes_to_compare_g1[t][2],
                                            1)

                                elif boxes_min_height[0][2] == 3 and b != nb_columns_G1 - columns_moved_G1 - 1:
                                    space_in_sections = hole_distance / (nb_rows_G3 - 1 + 1)
                                    val_start_col_3 = val_start_col_3 if 'val_start_col_3' in locals() and val_start_col_3 > 0 else 0
                                    for p in range(len(columns_not_yet_moved)):
                                        for m in range(nb_rows_G3 - 1):
                                            boxes[3]['y'][
                                                nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - val_start_col_3 - p] = \
                                                boxes[3]['y'][nb_columns_G3 * (
                                                        nb_rows_G3 - 1 * m) - 1 - val_start_col_3 - p] - space_in_sections * (
                                                        n_rows_g - 1 - m)
                                            box_v_moved_g3.append(
                                                nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - val_start_col_3 - p)
                                            if m == 0:
                                                result = [idx for idx, tup in enumerate(boxes_to_compare_g1) if
                                                          tup in {columns_not_yet_moved[p]}]

                                                boxes_to_compare_g1[result[0]] = (boxes_to_compare_g1[result[0]][0],
                                                                                  boxes[3]['y'][nb_columns_G3 * (
                                                                                          nb_rows_G3 - 1 * m) - 1 - val_start_col_3 - p],
                                                                                  boxes_to_compare_g1[result[0]][2],
                                                                                  boxes_to_compare_g1[result[0]][3])

                                    val_start_col_3 = val_start_col_3 + len(boxes_above_closest)
                                    set_list = set(columns_not_yet_moved)
                                    result = [idx for idx, tup in enumerate(boxes_to_compare_g1) if tup in set_list]
                                    for t in result:
                                        boxes_to_compare_g1[t] = (
                                            boxes_to_compare_g1[t][0], boxes_to_compare_g1[t][1],
                                            boxes_to_compare_g1[t][2],
                                            1)

                            continue

                    else:
                        boxes_not_yet_vm = [tup for tup in boxes_above if tup[3] == 0]

                    if len(boxes_not_yet_vm) == 0:

                        if len(boxes_above) == 0:

                            space_in_sections = (pallet_width - (height_von_level_G1 + width_val)) / (
                                    nb_rows_G1 - 1) if nb_rows_G1 > 1 else (
                                    pallet_width - (height_von_level_G1 + width_val))
                            for n in range(1, nb_rows_G1):
                                boxes[1]['y'][nb_columns_G1 * n + b * 1 + columns_moved_G1] = boxes[1]['y'][
                                                                                                  nb_columns_G1 * n + b * 1 + columns_moved_G1] + space_in_sections * n
                                box_v_moved_g1.append(nb_columns_G1 * n + b * 1 + columns_moved_G1)
                            continue
                        else:
                            if nb_rows_G1 > 1:
                                boxes_above_closest = [tup for tup in boxes_above if
                                                       tup[1] == min(boxes_above, key=lambda t: t[1])[1]]
                                hole_distance = boxes_above_closest[0][1] - (height_von_level_G1 + width_val)
                                space_in_sections = hole_distance / (nb_rows_G1 - 1 + 1)
                                for n in range(1, nb_rows_G1):
                                    boxes[1]['y'][nb_columns_G1 * n + b * 1 + columns_moved_G1] = boxes[1]['y'][
                                                                                                      nb_columns_G1 * n + b * 1 + columns_moved_G1] + space_in_sections * n
                                    box_v_moved_g1.append(nb_columns_G1 * n + b * 1 + columns_moved_G1)
                                continue
                            else:
                                continue

                    else:
                        boxes_above_closest = [tup for tup in boxes_above if
                                               tup[1] == min(boxes_not_yet_vm, key=lambda t: t[1])[1] and tup[3] == 0]
                        hole_distance = boxes_above_closest[0][1] - (height_von_level_G1 + width_val) if len(
                            boxes_above_closest) != 0 else "Hole with pallet edge"

                    if hole_distance == "Hole with pallet edge":

                        space_in_sections = (pallet_width - (height_von_level_G1 + width_val)) / (nb_rows_G1 - 1)
                        for t in range(nb_columns_G1 - columns_moved_G1):
                            for n in range(1, nb_rows_G1):
                                boxes[1]['y'][nb_columns_G1 * n + t * 1 + columns_moved_G1] = boxes[1]['y'][
                                                                                                  nb_columns_G1 * n + t * 1 + columns_moved_G1] + space_in_sections * n
                                box_v_moved_g1.append(nb_columns_G1 * n + t * 1 + columns_moved_G1)

                        break
                    else:

                        n_rows_g = locals()['nb_rows_G' + str(boxes_above_closest[0][2])]
                        if n_rows_g > 1:

                            if nb_rows_G1 > 1:

                                space_in_sections = hole_distance / (nb_rows_G1 - 1 + n_rows_g - 1 + 1)
                                for n in range(1, nb_rows_G1):
                                    boxes[1]['y'][nb_columns_G1 * n + b * 1 + columns_moved_G1] = boxes[1]['y'][
                                                                                                      nb_columns_G1 * n + b * 1 + columns_moved_G1] + space_in_sections * n
                                    box_v_moved_g1.append(nb_columns_G1 * n + b * 1 + columns_moved_G1)
                                if boxes_above_closest[0][2] == 3 and b != nb_columns_G1 - columns_moved_G1 - 1:
                                    val_start_col_3 = val_start_col_3 if 'val_start_col_3' in locals() and val_start_col_3 > 0 else 0
                                    for p in range(len(boxes_above_closest)):
                                        for m in range(nb_rows_G3 - 1):
                                            boxes[3]['y'][
                                                nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - val_start_col_3 - p] = \
                                                boxes[3]['y'][nb_columns_G3 * (
                                                        nb_rows_G3 - 1 * m) - 1 - val_start_col_3 - p] - space_in_sections * (
                                                        n_rows_g - 1 - m)
                                            box_v_moved_g3.append(
                                                nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - val_start_col_3 - p)

                                            if m == 0:
                                                result = [idx for idx, tup in enumerate(boxes_to_compare_g1) if
                                                          tup in {boxes_above_closest[p]}]

                                                boxes_to_compare_g1[result[0]] = (boxes_to_compare_g1[result[0]][0],
                                                                                  boxes[3]['y'][nb_columns_G3 * (
                                                                                          nb_rows_G3 - 1 * m) - 1 - val_start_col_3 - p],
                                                                                  boxes_to_compare_g1[result[0]][2],
                                                                                  boxes_to_compare_g1[result[0]][3])

                                                boxes_above_closest[p] = (boxes_above_closest[p][0],
                                                                          boxes[3]['y'][nb_columns_G3 * (
                                                                                  nb_rows_G3 - 1 * m) - 1 - val_start_col_3 - p],
                                                                          boxes_above_closest[p][2],
                                                                          boxes_above_closest[p][3])
                                    val_start_col_3 = val_start_col_3 + len(boxes_above_closest)
                                    set_list = set(boxes_above_closest)
                                    result = [idx for idx, tup in enumerate(boxes_to_compare_g1) if tup in set_list]
                                    for t in result:
                                        boxes_to_compare_g1[t] = (
                                            boxes_to_compare_g1[t][0], boxes_to_compare_g1[t][1],
                                            boxes_to_compare_g1[t][2],
                                            1)

                                elif boxes_above_closest[0][2] == 4 and b != nb_columns_G1 - columns_moved_G1 - 1:

                                    val_start_col_4 = val_start_col_4 if 'val_start_col_4' in locals() and val_start_col_4 > 0 else 0

                                    for q in range(len(boxes_above_closest)):
                                        for j in range(nb_rows_G4 - 1):
                                            boxes[4]['y'][nb_rows_G4 - 1 - j + nb_rows_G4 * q + val_start_col_4] = \
                                                boxes[4]['y'][
                                                    nb_rows_G4 - 1 - j + nb_rows_G4 * q + val_start_col_4] - space_in_sections * (
                                                        nb_rows_G4 - 1 - j)
                                            box_v_moved_g4.append(nb_rows_G4 - 1 - j + nb_rows_G4 * q + val_start_col_4)
                                            if j == 0:
                                                result = [idx for idx, tup in enumerate(boxes_to_compare_g1) if
                                                          tup in {boxes_above_closest[q]}]
                                                boxes_to_compare_g1[result[0]] = (boxes_to_compare_g1[result[0]][0],
                                                                                  boxes[4]['y'][
                                                                                      nb_rows_G4 - 1 - j + nb_rows_G4 * q + val_start_col_4],
                                                                                  boxes_to_compare_g1[result[0]][2],
                                                                                  boxes_to_compare_g1[result[0]][3])
                                                boxes_above_closest[q] = (boxes_above_closest[q][0],
                                                                          boxes[4]['y'][
                                                                              nb_rows_G4 - 1 - j + nb_rows_G4 * q + val_start_col_4],
                                                                          boxes_above_closest[q][2],
                                                                          boxes_above_closest[q][3])

                                    val_start_col_4 = val_start_col_4 + nb_rows_G4 * len(boxes_above_closest)
                                    set_list = set(boxes_above_closest)
                                    result = [idx for idx, tup in enumerate(boxes_to_compare_g1) if tup in set_list]
                                    for t in result:
                                        boxes_to_compare_g1[t] = (
                                            boxes_to_compare_g1[t][0], boxes_to_compare_g1[t][1],
                                            boxes_to_compare_g1[t][2],
                                            1)

                            else:
                                space_in_sections = hole_distance / (n_rows_g - 1 + 1)

                                if boxes_above_closest[0][2] == 3 and b != nb_columns_G1 - columns_moved_G1 - 1:
                                    val_start_col_3 = val_start_col_3 if 'val_start_col_3' in locals() and val_start_col_3 > 0 else 0
                                    for p in range(len(boxes_above_closest)):
                                        for m in range(nb_rows_G3 - 1):

                                            boxes[3]['y'][
                                                nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - val_start_col_3 - p] = \
                                                boxes[3]['y'][nb_columns_G3 * (
                                                        nb_rows_G3 - 1 * m) - 1 - val_start_col_3 - p] - space_in_sections * (
                                                        n_rows_g - 1 - m)
                                            box_v_moved_g3.append(
                                                nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - val_start_col_3)
                                            if m == 0:
                                                result = [idx for idx, tup in enumerate(boxes_to_compare_g1) if
                                                          tup in {boxes_above_closest[p]}]
                                                boxes_to_compare_g1[result[0]] = (boxes_to_compare_g1[result[0]][0],
                                                                                  boxes[3]['y'][nb_columns_G3 * (
                                                                                          nb_rows_G3 - 1 * m) - 1 - val_start_col_3 - p],
                                                                                  boxes_to_compare_g1[result[0]][2],
                                                                                  boxes_to_compare_g1[result[0]][3])
                                                boxes_above_closest[p] = (boxes_above_closest[p][0],
                                                                          boxes[3]['y'][nb_columns_G3 * (
                                                                                  nb_rows_G3 - 1 * m) - 1 - val_start_col_3 - p],
                                                                          boxes_above_closest[p][2],
                                                                          boxes_above_closest[p][3])
                                    val_start_col_3 = val_start_col_3 + len(boxes_above_closest)
                                    set_list = set(boxes_above_closest)
                                    result = [idx for idx, tup in enumerate(boxes_to_compare_g1) if tup in set_list]
                                    for t in result:
                                        boxes_to_compare_g1[t] = (
                                            boxes_to_compare_g1[t][0], boxes_to_compare_g1[t][1],
                                            boxes_to_compare_g1[t][2],
                                            1)
                                elif boxes_above_closest[0][2] == 4 and b != nb_columns_G1 - columns_moved_G1 - 1:
                                    val_start_col_4 = val_start_col_4 if 'val_start_col_4' in locals() and val_start_col_4 > 0 else 0
                                    for q in range(len(boxes_above_closest)):
                                        for j in range(nb_rows_G4 - 1):
                                            boxes[4]['y'][
                                                nb_rows_G4 - 1 - j + nb_rows_G4 * q + nb_rows_G4 * columns_moved_G4 + val_start_col_4] = \
                                                boxes[4]['y'][
                                                    nb_rows_G4 - 1 - j + nb_rows_G4 * q + nb_rows_G4 * columns_moved_G4 + val_start_col_4] - space_in_sections * (
                                                        nb_rows_G4 - 1 - j)
                                            box_v_moved_g4.append(
                                                nb_rows_G4 - 1 - j + nb_rows_G4 * q + nb_rows_G4 * columns_moved_G4 + val_start_col_4)
                                            if j == 0:
                                                result = [idx for idx, tup in enumerate(boxes_to_compare_g1) if
                                                          tup in {boxes_above_closest[q]}]
                                                boxes_to_compare_g1[result[0]] = (boxes_to_compare_g1[result[0]][0],
                                                                                  boxes[4]['y'][
                                                                                      nb_rows_G4 - 1 - j + nb_rows_G4 * q + nb_rows_G4 * columns_moved_G4 + val_start_col_4],
                                                                                  boxes_to_compare_g1[result[0]][2],
                                                                                  boxes_to_compare_g1[result[0]][3])
                                                boxes_above_closest[q] = (boxes_above_closest[q][0],
                                                                          boxes[4]['y'][
                                                                              nb_rows_G4 - 1 - j + nb_rows_G4 * q + nb_rows_G4 * columns_moved_G4 + val_start_col_4],
                                                                          boxes_above_closest[q][2],
                                                                          boxes_above_closest[q][3])

                                    val_start_col_4 = val_start_col_4 + nb_rows_G4 * len(boxes_above_closest)
                                    set_list = set(boxes_above_closest)
                                    result = [idx for idx, tup in enumerate(boxes_to_compare_g1) if tup in set_list]
                                    for t in result:
                                        boxes_to_compare_g1[t] = (
                                            boxes_to_compare_g1[t][0], boxes_to_compare_g1[t][1],
                                            boxes_to_compare_g1[t][2],
                                            1)

                        else:

                            if nb_rows_G1 > 1:

                                space_in_sections = hole_distance / (nb_rows_G1 - 1 + 1)
                                for n in range(1, nb_rows_G1):
                                    boxes[1]['y'][nb_columns_G1 * n + b * 1 + columns_moved_G1] = boxes[1]['y'][
                                                                                                      nb_columns_G1 * n + b * 1 + columns_moved_G1] + space_in_sections * n

                                    box_v_moved_g1.append(nb_columns_G1 * n + b * 1 + columns_moved_G1)

                                set_list = set(boxes_above_closest)
                                result = [idx for idx, tup in enumerate(boxes_to_compare_g1) if tup in set_list]
                                for t in result:
                                    boxes_to_compare_g1[t] = (
                                        boxes_to_compare_g1[t][0], boxes_to_compare_g1[t][1], boxes_to_compare_g1[t][2],
                                        1)
                            else:
                                space_in_sections = 0

            else:

                space_in_sections = (pallet_width - (height_von_level_G1 + width_val)) / (
                        nb_rows_G1 - 1) if nb_rows_G1 > 1 else (pallet_width - (height_von_level_G1 + width_val))
                columns_moved_G1 = int(len(box_v_moved_g1) / (nb_rows_G1 - 1)) if len(
                    box_v_moved_g1) > nb_columns_G1 else len(box_v_moved_g1)
                for b in range(nb_columns_G1 - columns_moved_G1):
                    for n in range(1, nb_rows_G1):
                        boxes[1]['y'][nb_columns_G1 * n + b * 1 + columns_moved_G1] = boxes[1]['y'][
                                                                                          nb_columns_G1 * n + b * 1 + columns_moved_G1] + space_in_sections * n
                        box_v_moved_g1.append(nb_columns_G1 * n + b * 1 + columns_moved_G1)

        if li == 0 and len(boxes[4]['x']) != 0:
            nb_rows_G4 = nb_rows_G4 if 'nb_rows_G4' in locals() else len(set(boxes[4]['y']))
            nb_columns_G4 = nb_columns_G4 if 'nb_columns_G4' in locals() else len(set(boxes[4]['x']))
            height_von_level_G4 = height_von_level_G4 if 'height_von_level_G4' in locals() else min(boxes[4]['y'])
            if nb_rows_G4 > 1:
                if len(boxes[1]['x']) != 0:
                    nb_rows_G1 = nb_rows_G1 if 'nb_rows_G1' in locals() else len(set(boxes[1]['y']))
                    nb_columns_G1 = nb_columns_G1 if 'nb_columns_G1' in locals() else len(set(boxes[1]['x']))
                    height_von_level_G1 = height_von_level_G1 if 'height_von_level_G1' in locals() else max(
                        boxes[1]['y'])

                    if len(boxes[2]['x']) != 0:
                        nb_rows_G2 = nb_rows_G2 if 'nb_rows_G2' in locals() else len(set(boxes[2]['y']))
                        nb_columns_G2 = nb_columns_G2 if 'nb_columns_G2' in locals() else len(set(boxes[2]['x']))
                        height_von_level_G2 = height_von_level_G2 if 'height_von_level_G2' in locals() else max(
                            boxes[2]['y'])

                        boxes_to_compare_g4 = []
                        for q in range(nb_columns_G1):
                            boxes_to_compare_g4.append((boxes[1]['x'][nb_columns_G1 * 0 + q * 1 + (
                                    nb_rows_G1 - 1) * nb_columns_G1], boxes[1]['y'][nb_columns_G1 * 0 + q * 1 + (
                                    nb_rows_G1 - 1) * nb_columns_G1], 1, 0))
                        for c in range(nb_columns_G2):
                            boxes_to_compare_g4.append((boxes[2]['x'][nb_columns_G2 * nb_rows_G2 - 1 - 1 * c],
                                                        boxes[2]['y'][nb_columns_G2 * nb_rows_G2 - 1 - 1 * c], 2, 0))
                    else:
                        boxes_to_compare_g4 = []
                        for q in range(nb_columns_G1):
                            boxes_to_compare_g4.append((boxes[1]['x'][nb_columns_G1 * 0 + q * 1 + (
                                    nb_rows_G1 - 1) * nb_columns_G1], boxes[1]['y'][nb_columns_G1 * 0 + q * 1 + (
                                    nb_rows_G1 - 1) * nb_columns_G1], 1, 0))
                elif len(boxes[2]['x']) != 0:
                    nb_rows_G2 = nb_rows_G2 if 'nb_rows_G2' in locals() else len(set(boxes[2]['y']))
                    nb_columns_G2 = nb_columns_G2 if 'nb_columns_G2' in locals() else len(set(boxes[2]['x']))
                    height_von_level_G2 = height_von_level_G2 if 'height_von_level_G2' in locals() else max(
                        boxes[2]['y'])

                    boxes_to_compare_g4 = []
                    for c in range(nb_columns_G2):
                        boxes_to_compare_g4.append((boxes[2]['x'][nb_columns_G2 * nb_rows_G2 - 1 - 1 * c],
                                                    boxes[2]['y'][nb_columns_G2 * nb_rows_G2 - 1 - 1 * c], 2, 0))
                else:
                    boxes_to_compare_g4 = []
                if len(boxes_to_compare_g4) != 0:
                    columns_moved_G4 = int(len(box_v_moved_g4) / (nb_rows_G4 - 1)) if nb_rows_G4 > 1 else 0
                    if 'nb_rows_G2' in locals():
                        columns_moved_G2 = int(len(box_v_moved_g2) / (nb_rows_G2 - 1)) if nb_rows_G2 > 1 else 0
                    else:
                        columns_moved_G2 = 0
                    if 0 == 1:
                        pass

                    else:

                        if 'boxes_to_compare_g1' in locals():
                            for b in range(nb_columns_G4 - columns_moved_G4):
                                boxes_under = []
                                for c in range(len(boxes_to_compare_g4)):
                                    if boxes_to_compare_g4[c][2] == 1:
                                        list1 = [b * width_val + columns_moved_G4 * width_val,
                                                 b * width_val + width_val + columns_moved_G4 * width_val]
                                        list2 = [boxes_to_compare_g4[c][0], boxes_to_compare_g4[c][0] + length_val]
                                        if list1[1] > list2[0] and list2[1] > list1[0]:
                                            boxes_under.append(boxes_to_compare_g4[c])

                                    if boxes_to_compare_g4[c][2] == 2:
                                        list1 = [b * width_val + columns_moved_G4 * width_val,
                                                 b * width_val + width_val + columns_moved_G4 * width_val]
                                        list2 = [boxes_to_compare_g4[c][0], boxes_to_compare_g4[c][0] + width_val]
                                        if list1[1] > list2[0] and list2[1] > list1[0]:
                                            boxes_under.append(boxes_to_compare_g4[c])

                                if len(boxes_under) > 0:
                                    groups_height = [a[2] for a in boxes_under]
                                    if len(set(groups_height)) == 2:
                                        for tup in boxes_under:
                                            if tup[2] == 1: val1_to_compare = tup[1] + width_val
                                            if tup[2] == 2: val2_to_compare = tup[1] + length_val
                                            if 'val1_to_compare' in locals() and 'val2_to_compare' in locals():
                                                if val1_to_compare > val2_to_compare:
                                                    group_max_value = 1
                                                else:
                                                    group_max_value = 2
                                    else:
                                        group_max_value = list(set(groups_height))[0]

                                    boxes_under_closest = [tup for tup in boxes_under if tup[2] == group_max_value]
                                    if boxes_under_closest[0][2] == 1:
                                        space_hole = height_von_level_G4 - (boxes_under_closest[0][1] + width_val)
                                        space_in_sections = space_hole / (nb_rows_G4 - 1 + 1)
                                        val_start_col_4 = val_start_col_4 if 'val_start_col_4' in locals() and val_start_col_4 > 0 else 0
                                        for m in range(nb_rows_G4 - 1):

                                            if m == 0:
                                                result = [idx for idx, tup in enumerate(boxes_to_compare_g1) if tup in {
                                                    (boxes[4]['x'][
                                                         nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4],
                                                     boxes[4]['y'][
                                                         nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4], 4, 0)}]
                                                boxes[4]['y'][nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4] = \
                                                    boxes[4]['y'][
                                                        nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4] - space_in_sections * (
                                                            nb_rows_G4 - 1 - m)
                                                box_v_moved_g4.append(
                                                    nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4)

                                                boxes_to_compare_g1[result[0]] = (boxes_to_compare_g1[result[0]][0],
                                                                                  boxes[4]['y'][
                                                                                      nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4],
                                                                                  boxes_to_compare_g1[result[0]][2],
                                                                                  1)
                                            else:
                                                boxes[4]['y'][nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4] = \
                                                    boxes[4]['y'][
                                                        nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4] - space_in_sections * (
                                                            nb_rows_G4 - 1 - m)
                                                box_v_moved_g4.append(
                                                    nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4)

                                        val_start_col_4 = val_start_col_4 + nb_rows_G4


                                    elif boxes_under_closest[0][2] == 2:
                                        space_hole = height_von_level_G4 - (boxes_under_closest[0][1] + length_val)
                                        if nb_rows_G2 == 1:
                                            space_in_sections = space_hole / (nb_rows_G4 - 1 + 1)
                                            val_start_col_4 = val_start_col_4 if 'val_start_col_4' in locals() and val_start_col_4 > 0 else 0
                                            for m in range(nb_rows_G4 - 1):

                                                if m == 0:
                                                    result = [idx for idx, tup in enumerate(boxes_to_compare_g1) if
                                                              tup in {(boxes[4]['x'][
                                                                           nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4],
                                                                       boxes[4]['y'][
                                                                           nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4],
                                                                       4, 0)}]
                                                    boxes[4]['y'][
                                                        nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4] = \
                                                        boxes[4]['y'][
                                                            nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4] - space_in_sections * (
                                                                nb_rows_G4 - 1 - m)
                                                    box_v_moved_g4.append(
                                                        nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4)

                                                    boxes_to_compare_g1[result[0]] = (boxes_to_compare_g1[result[0]][0],
                                                                                      boxes[4]['y'][
                                                                                          nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4],
                                                                                      boxes_to_compare_g1[result[0]][2],
                                                                                      1)
                                                else:
                                                    boxes[4]['y'][
                                                        nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4] = \
                                                        boxes[4]['y'][
                                                            nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4] - space_in_sections * (
                                                                nb_rows_G4 - 1 - m)
                                                    box_v_moved_g4.append(
                                                        nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4)

                                            val_start_col_4 = val_start_col_4 + nb_rows_G4

                                        elif nb_rows_G2 > 1:
                                            space_in_sections = space_hole / (nb_rows_G2 - 1 + nb_rows_G4 - 1 + 1)
                                            if len(boxes[3]['x']) > 0:
                                                if height_von_level_G3 > height_von_level_G4:
                                                    for n in range(nb_rows_G2 - 1):
                                                        boxes[2]['y'][
                                                            nb_columns_G2 * nb_rows_G2 - 1 - nb_columns_G2 * n] = \
                                                            boxes[2]['y'][
                                                                nb_columns_G2 * nb_rows_G2 - 1 - nb_columns_G2 * n] + space_in_sections * (
                                                                    nb_rows_G2 - 1 - n)
                                                        box_v_moved_g2.append(
                                                            nb_columns_G2 * nb_rows_G2 - 1 - nb_columns_G2 * n)

                                                    val_start_col_4 = val_start_col_4 if 'val_start_col_4' in locals() and val_start_col_4 > 0 else 0
                                            else:
                                                for n in range(nb_rows_G2 - 1):
                                                    boxes[2]['y'][nb_columns_G2 * nb_rows_G2 - 1 - nb_columns_G2 * n] = \
                                                        boxes[2]['y'][
                                                            nb_columns_G2 * nb_rows_G2 - 1 - nb_columns_G2 * n] + space_in_sections * (
                                                                nb_rows_G2 - 1 - n)
                                                    box_v_moved_g2.append(
                                                        nb_columns_G2 * nb_rows_G2 - 1 - nb_columns_G2 * n)

                                                val_start_col_4 = val_start_col_4 if 'val_start_col_4' in locals() and val_start_col_4 > 0 else 0
                                            for m in range(nb_rows_G4 - 1):

                                                if m == 0:
                                                    result = [idx for idx, tup in enumerate(boxes_to_compare_g1) if
                                                              tup in {(boxes[4]['x'][
                                                                           nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4],
                                                                       boxes[4]['y'][
                                                                           nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4],
                                                                       4, 0)}]
                                                    boxes[4]['y'][
                                                        nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4] = \
                                                        boxes[4]['y'][
                                                            nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4] - space_in_sections * (
                                                                nb_rows_G4 - 1 - m)
                                                    box_v_moved_g4.append(
                                                        nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4)

                                                    boxes_to_compare_g1[result[0]] = (boxes_to_compare_g1[result[0]][0],
                                                                                      boxes[4]['y'][
                                                                                          nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4],
                                                                                      boxes_to_compare_g1[result[0]][2],
                                                                                      1)
                                                else:
                                                    boxes[4]['y'][
                                                        nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4] = \
                                                        boxes[4]['y'][
                                                            nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4] - space_in_sections * (
                                                                nb_rows_G4 - 1 - m)
                                                    box_v_moved_g4.append(
                                                        nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4)

                                            val_start_col_4 = val_start_col_4 + nb_rows_G4

                                else:
                                    space_in_sections = height_von_level_G4 / (
                                            nb_rows_G4 - 1) if nb_rows_G4 > 1 else height_von_level_G4
                                    columns_moved_G4 = int(
                                        len(box_v_moved_g4) / (nb_rows_G4 - 1)) if nb_rows_G4 > 1 else len(
                                        box_v_moved_g4)
                                    val_start_col_4 = val_start_col_4 if 'val_start_col_4' in locals() and val_start_col_4 > 0 else 0
                                    for b in range(nb_columns_G4 - columns_moved_G4):
                                        for n in range(nb_rows_G4 - 1):
                                            boxes[4]['y'][nb_rows_G4 - 1 - n + val_start_col_4] = boxes[4]['y'][
                                                                                                      nb_rows_G4 - 1 - n + val_start_col_4] - space_in_sections * (
                                                                                                          nb_rows_G4 - 1 - n)
                                            box_v_moved_g4.append(nb_rows_G4 - 1 - n + val_start_col_4)
                                        val_start_col_4 = val_start_col_4 + nb_rows_G4



                        else:
                            no_g1_box_moved_g4 = []
                            for b in range(nb_columns_G4 - columns_moved_G4):
                                boxes_under = []
                                for c in range(len(boxes_to_compare_g4)):
                                    if boxes_to_compare_g4[c][2] == 2:
                                        list1 = [b * width_val + columns_moved_G4 * width_val,
                                                 b * width_val + width_val + columns_moved_G4 * width_val]
                                        list2 = [boxes_to_compare_g4[c][0], boxes_to_compare_g4[c][0] + width_val]
                                        if list1[1] > list2[0] and list2[1] > list1[0]:
                                            boxes_under.append(boxes_to_compare_g4[c])

                                if len(boxes_under) > 0:
                                    boxes_under_closest = boxes_under

                                    if boxes_under_closest[0][2] == 2:
                                        space_hole = height_von_level_G4 - (boxes_under_closest[0][1] + length_val)
                                        if nb_rows_G2 == 1:
                                            space_in_sections = space_hole / (nb_rows_G4 - 1 + 1)
                                            val_start_col_4 = val_start_col_4 if 'val_start_col_4' in locals() and val_start_col_4 > 0 else 0
                                            for m in range(nb_rows_G4 - 1):
                                                boxes[4]['y'][nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4] = \
                                                    boxes[4]['y'][
                                                        nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4] - space_in_sections * (
                                                            nb_rows_G4 - 1 - m)
                                                box_v_moved_g4.append(
                                                    nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4)
                                                if m == 0:
                                                    no_g1_box_moved_g4.append((boxes[4]['x'][
                                                                                   nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4],
                                                                               boxes[4]['y'][
                                                                                   nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4],
                                                                               4, 1))

                                            val_start_col_4 = val_start_col_4 + nb_rows_G4

                                        elif nb_rows_G2 > 1:
                                            space_in_sections = space_hole / (nb_rows_G2 - 1 + nb_rows_G4 - 1 + 1)
                                            val_start_col_2 = val_start_col_2 if 'val_start_col_2' in locals() and val_start_col_2 > 0 else 0
                                            for n in range(nb_rows_G2 - 1):
                                                boxes[2]['y'][
                                                    nb_columns_G2 * nb_rows_G2 - 1 - n * nb_columns_G2 - 1 * val_start_col_2] = \
                                                    boxes[2]['y'][
                                                        nb_columns_G2 * nb_rows_G2 - 1 - n * nb_columns_G2 - 1 * val_start_col_2] + space_in_sections * (
                                                            nb_rows_G2 - 1 - n)
                                                box_v_moved_g2.append(
                                                    nb_columns_G2 * nb_rows_G2 - 1 - n * nb_columns_G2 - 1 * val_start_col_2)
                                            val_start_col_2 = val_start_col_2 + 1

                                            val_start_col_4 = val_start_col_4 if 'val_start_col_4' in locals() and val_start_col_4 > 0 else 0
                                            for m in range(nb_rows_G4 - 1):
                                                boxes[4]['y'][nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4] = \
                                                    boxes[4]['y'][
                                                        nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4] - space_in_sections * (
                                                            nb_rows_G4 - 1 - m)
                                                box_v_moved_g4.append(
                                                    nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4)
                                                if m == 0:
                                                    no_g1_box_moved_g4.append((boxes[4]['x'][
                                                                                   nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4],
                                                                               boxes[4]['y'][
                                                                                   nb_rows_G4 - 1 - m + nb_rows_G4 * 0 + val_start_col_4],
                                                                               4, 1))

                                            val_start_col_4 = val_start_col_4 + nb_rows_G4



                                else:
                                    space_in_sections = height_von_level_G4 / (
                                            nb_rows_G4 - 1) if nb_rows_G4 > 1 else height_von_level_G4
                                    columns_moved_G4 = int(
                                        len(box_v_moved_g4) / (nb_rows_G4 - 1)) if nb_rows_G4 > 1 else len(
                                        box_v_moved_g4)

                                    for b in range(nb_columns_G4 - columns_moved_G4):
                                        for n in range(nb_rows_G4 - 1):
                                            boxes[4]['y'][
                                                nb_rows_G4 - 1 - n + nb_rows_G4 * b + nb_rows_G4 * columns_moved_G4] = \
                                                boxes[4]['y'][
                                                    nb_rows_G4 - 1 - n + nb_rows_G4 * b + nb_rows_G4 * columns_moved_G4] - space_in_sections * (
                                                        nb_rows_G4 - 1 - n)
                                            box_v_moved_g4.append(
                                                nb_rows_G4 - 1 - n + nb_rows_G4 * b + nb_rows_G4 * columns_moved_G4)
                                            if n == 0:
                                                no_g1_box_moved_g4.append((boxes[4]['x'][
                                                                               nb_rows_G4 - 1 - n + nb_rows_G4 * b + nb_rows_G4 * columns_moved_G4],
                                                                           boxes[4]['y'][
                                                                               nb_rows_G4 - 1 - n + nb_rows_G4 * b + nb_rows_G4 * columns_moved_G4],
                                                                           4, 1))
                                    break


                else:
                    space_in_sections = height_von_level_G4 / (
                            nb_rows_G4 - 1) if nb_rows_G4 > 1 else height_von_level_G4
                    columns_moved_G4 = int(len(box_v_moved_g4) / (nb_rows_G4 - 1)) if nb_rows_G4 > 1 else len(
                        box_v_moved_g4)
                    for b in range(nb_columns_G4 - columns_moved_G4):
                        for n in range(nb_rows_G4 - 1):
                            boxes[4]['y'][nb_rows_G4 - 1 - n + nb_rows_G4 * b + nb_rows_G4 * columns_moved_G4] = \
                                boxes[4]['y'][
                                    nb_rows_G4 - 1 - n + nb_rows_G4 * b + nb_rows_G4 * columns_moved_G4] - space_in_sections * (
                                        nb_rows_G4 - 1 - n)
                            box_v_moved_g4.append(nb_rows_G4 - 1 - n + nb_rows_G4 * b + nb_rows_G4 * columns_moved_G4)

        if li == 0 and len(boxes[3]['x']) != 0:
            nb_rows_G3 = nb_rows_G3 if 'nb_rows_G3' in locals() else len(set(boxes[3]['y']))
            nb_columns_G3 = nb_columns_G3 if 'nb_columns_G3' in locals() else len(set(boxes[3]['x']))
            height_von_level_G3 = height_von_level_G3 if 'height_von_level_G3' in locals() else min(boxes[3]['y'])
            if nb_rows_G3 > 1:
                if len(boxes[1]['x']) != 0:
                    nb_rows_G1 = nb_rows_G1 if 'nb_rows_G1' in locals() else len(set(boxes[1]['y']))
                    nb_columns_G1 = nb_columns_G1 if 'nb_columns_G1' in locals() else len(set(boxes[1]['x']))
                    height_von_level_G1 = height_von_level_G1 if 'height_von_level_G1' in locals() else max(
                        boxes[1]['y'])

                    if len(boxes[2]['x']) != 0:
                        nb_rows_G2 = nb_rows_G2 if 'nb_rows_G2' in locals() else len(set(boxes[2]['y']))
                        nb_columns_G2 = nb_columns_G2 if 'nb_columns_G2' in locals() else len(set(boxes[2]['x']))
                        height_von_level_G2 = height_von_level_G2 if 'height_von_level_G2' in locals() else max(
                            boxes[2]['y'])

                        boxes_to_compare_g3 = []
                        for q in range(nb_columns_G1):
                            boxes_to_compare_g3.append((boxes[1]['x'][nb_columns_G1 * 0 + q * 1 + (
                                    nb_rows_G1 - 1) * nb_columns_G1], boxes[1]['y'][nb_columns_G1 * 0 + q * 1 + (
                                    nb_rows_G1 - 1) * nb_columns_G1], 1, 0))
                        for c in range(nb_columns_G2):
                            boxes_to_compare_g3.append((boxes[2]['x'][nb_columns_G2 * nb_rows_G2 - 1 - 1 * c],
                                                        boxes[2]['y'][nb_columns_G2 * nb_rows_G2 - 1 - 1 * c], 2, 0))
                    else:
                        boxes_to_compare_g3 = []
                        for q in range(nb_columns_G1):
                            boxes_to_compare_g3.append((boxes[1]['x'][nb_columns_G1 * 0 + q * 1 + (
                                    nb_rows_G1 - 1) * nb_columns_G1], boxes[1]['y'][nb_columns_G1 * 0 + q * 1 + (
                                    nb_rows_G1 - 1) * nb_columns_G1], 1, 0))
                elif len(boxes[2]['x']) != 0:
                    nb_rows_G2 = nb_rows_G2 if 'nb_rows_G2' in locals() else len(set(boxes[2]['y']))
                    nb_columns_G2 = nb_columns_G2 if 'nb_columns_G2' in locals() else len(set(boxes[2]['x']))
                    height_von_level_G2 = height_von_level_G2 if 'height_von_level_G2' in locals() else max(
                        boxes[2]['y'])

                    boxes_to_compare_g3 = []
                    for c in range(nb_columns_G2):
                        boxes_to_compare_g3.append((boxes[2]['x'][nb_columns_G2 * nb_rows_G2 - 1 - 1 * c],
                                                    boxes[2]['y'][nb_columns_G2 * nb_rows_G2 - 1 - 1 * c], 2, 0))
                else:
                    boxes_to_compare_g3 = []

                if len(boxes_to_compare_g3) != 0:
                    columns_moved_G3 = int(len(box_v_moved_g3) / (nb_rows_G3 - 1)) if nb_rows_G3 > 1 else 0
                    if 'nb_rows_G2' in locals():
                        columns_moved_G2 = int(len(box_v_moved_g2) / (nb_rows_G2 - 1)) if nb_rows_G2 > 1 else 0
                    if 0 == 1:
                        pass
                    else:
                        if 'boxes_to_compare_g1' in locals():
                            for b in range(nb_columns_G3 - columns_moved_G3):
                                boxes_under = []
                                for c in range(len(boxes_to_compare_g3)):
                                    if boxes_to_compare_g3[c][2] == 1:
                                        list1 = [
                                            pallet_length - length_val * nb_columns_G3 + b * length_val + columns_moved_G3 * length_val,
                                            pallet_length - length_val * nb_columns_G3 + b * length_val + length_val + columns_moved_G3 * length_val]
                                        list2 = [boxes_to_compare_g3[c][0], boxes_to_compare_g3[c][0] + length_val]
                                        if list1[1] > list2[0] and list2[1] > list1[0]:
                                            boxes_under.append(boxes_to_compare_g3[c])

                                    if boxes_to_compare_g3[c][2] == 2:

                                        list1 = [
                                            pallet_length - length_val * nb_columns_G3 + b * length_val + columns_moved_G3 * length_val,
                                            pallet_length - length_val * nb_columns_G3 + b * length_val + length_val + columns_moved_G3 * length_val]
                                        list2 = [boxes_to_compare_g3[c][0], boxes_to_compare_g3[c][0] + width_val]
                                        if list1[1] > list2[0] and list2[1] > list1[0]:
                                            boxes_under.append(boxes_to_compare_g3[c])
                                if len(boxes_under) > 0:
                                    groups_height = [a[2] for a in boxes_under]
                                    if len(set(groups_height)) == 2:
                                        for tup in boxes_under:
                                            if tup[2] == 1: val1_to_compare = tup[1] + width_val
                                            if tup[2] == 2: val2_to_compare = tup[1] + length_val
                                            if 'val1_to_compare' in locals() and 'val2_to_compare' in locals():
                                                if val1_to_compare > val2_to_compare:
                                                    group_max_value = 1
                                                else:
                                                    group_max_value = 2
                                    else:
                                        group_max_value = list(set(groups_height))[0]

                                    boxes_under_closest = [tup for tup in boxes_under if tup[2] == group_max_value]
                                    if boxes_under_closest[0][2] == 1:
                                        space_hole = height_von_level_G3 - (boxes_under_closest[0][1] + width_val)
                                        space_in_sections = space_hole / (nb_rows_G3 - 1 + 1)
                                        val_start_col_3 = val_start_col_3 if 'val_start_col_3' in locals() and val_start_col_3 > 0 else 0
                                        for m in range(nb_rows_G3 - 1):
                                            if m == 0:
                                                result = [idx for idx, tup in enumerate(boxes_to_compare_g1) if tup in {
                                                    (boxes[3]['x'][
                                                         nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - val_start_col_3],
                                                     boxes[3]['y'][
                                                         nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - val_start_col_3], 3,
                                                     0)}]

                                                boxes[3]['y'][
                                                    nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - val_start_col_3] = \
                                                    boxes[3]['y'][nb_columns_G3 * (
                                                            nb_rows_G3 - 1 * m) - 1 - val_start_col_3] - space_in_sections * (
                                                            nb_rows_G3 - 1 - m)
                                                box_v_moved_g3.append(
                                                    nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - val_start_col_3)

                                                boxes_to_compare_g1[result[0]] = (boxes_to_compare_g1[result[0]][0],
                                                                                  boxes[3]['y'][nb_columns_G3 * (
                                                                                          nb_rows_G3 - 1 * m) - 1 - val_start_col_3],
                                                                                  boxes_to_compare_g1[result[0]][2],
                                                                                  1)
                                            else:
                                                boxes[3]['y'][
                                                    nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - val_start_col_3] = \
                                                    boxes[3]['y'][nb_columns_G3 * (
                                                            nb_rows_G3 - 1 * m) - 1 - val_start_col_3] - space_in_sections * (
                                                            nb_rows_G3 - 1 - m)
                                                box_v_moved_g3.append(
                                                    nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - val_start_col_3)

                                        val_start_col_3 = val_start_col_3 + 1

                                    elif boxes_under_closest[0][2] == 2:
                                        space_hole = height_von_level_G3 - (boxes_under_closest[0][1] + length_val)
                                        if nb_rows_G2 == 1:
                                            space_in_sections = space_hole / (nb_rows_G3 - 1 + 1)
                                            val_start_col_3 = val_start_col_3 if 'val_start_col_3' in locals() and val_start_col_3 > 0 else 0
                                            for m in range(nb_rows_G3 - 1):
                                                if m == 0:
                                                    result = [idx for idx, tup in enumerate(boxes_to_compare_g1) if
                                                              tup in {(boxes[3]['x'][nb_columns_G3 * (
                                                                      nb_rows_G3 - 1 * m) - 1 - val_start_col_3],
                                                                       boxes[3]['y'][nb_columns_G3 * (
                                                                               nb_rows_G3 - 1 * m) - 1 - val_start_col_3],
                                                                       3, 0)}]

                                                    boxes[3]['y'][
                                                        nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - val_start_col_3] = \
                                                        boxes[3]['y'][nb_columns_G3 * (
                                                                nb_rows_G3 - 1 * m) - 1 - val_start_col_3] - space_in_sections * (
                                                                nb_rows_G3 - 1 - m)
                                                    box_v_moved_g3.append(
                                                        nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - val_start_col_3)

                                                    boxes_to_compare_g1[result[0]] = (boxes_to_compare_g1[result[0]][0],
                                                                                      boxes[3]['y'][nb_columns_G3 * (
                                                                                              nb_rows_G3 - 1 * m) - 1 - val_start_col_3],
                                                                                      boxes_to_compare_g1[result[0]][2],
                                                                                      1)
                                                else:
                                                    boxes[3]['y'][
                                                        nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - val_start_col_3] = \
                                                        boxes[3]['y'][nb_columns_G3 * (
                                                                nb_rows_G3 - 1 * m) - 1 - val_start_col_3] - space_in_sections * (
                                                                nb_rows_G3 - 1 - m)
                                                    box_v_moved_g3.append(
                                                        nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - val_start_col_3)

                                            val_start_col_3 = val_start_col_3 + 1
                                        elif nb_rows_G2 > 1:
                                            space_in_sections = space_hole / (nb_rows_G2 - 1 + nb_rows_G3 - 1 + 1)
                                            val_start_col_2 = val_start_col_2 if 'val_start_col_2' in locals() and val_start_col_2 > 0 else 0
                                            for n in range(nb_rows_G2 - 1):
                                                boxes[2]['y'][
                                                    nb_columns_G2 * nb_rows_G2 - 1 - nb_columns_G2 * n - 1 * val_start_col_2 - columns_moved_G2] = \
                                                    boxes[2]['y'][
                                                        nb_columns_G2 * nb_rows_G2 - 1 - nb_columns_G2 * n - 1 * val_start_col_2 - columns_moved_G2] + space_in_sections * (
                                                            nb_rows_G2 - 1 - n)
                                                box_v_moved_g2.append(
                                                    nb_columns_G2 * nb_rows_G2 - 1 - nb_columns_G2 * n - 1 * val_start_col_2 - columns_moved_G2)
                                            val_start_col_2 = val_start_col_2 + 1

                                            val_start_col_3 = val_start_col_3 if 'val_start_col_3' in locals() and val_start_col_3 > 0 else 0
                                            for m in range(nb_rows_G3 - 1):
                                                if m == 0:
                                                    result = [idx for idx, tup in enumerate(boxes_to_compare_g1) if
                                                              tup in {(boxes[3]['x'][nb_columns_G3 * (
                                                                      nb_rows_G3 - 1 * m) - 1 - val_start_col_3],
                                                                       boxes[3]['y'][nb_columns_G3 * (
                                                                               nb_rows_G3 - 1 * m) - 1 - val_start_col_3],
                                                                       3, 0)}]

                                                    boxes[3]['y'][
                                                        nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - val_start_col_3] = \
                                                        boxes[3]['y'][nb_columns_G3 * (
                                                                nb_rows_G3 - 1 * m) - 1 - val_start_col_3] - space_in_sections * (
                                                                nb_rows_G3 - 1 - m)
                                                    box_v_moved_g3.append(
                                                        nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - val_start_col_3)

                                                    boxes_to_compare_g1[result[0]] = (boxes_to_compare_g1[result[0]][0],
                                                                                      boxes[3]['y'][nb_columns_G3 * (
                                                                                              nb_rows_G3 - 1 * m) - 1 - val_start_col_3],
                                                                                      boxes_to_compare_g1[result[0]][2],
                                                                                      1)
                                                else:
                                                    boxes[3]['y'][
                                                        nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - val_start_col_3] = \
                                                        boxes[3]['y'][nb_columns_G3 * (
                                                                nb_rows_G3 - 1 * m) - 1 - val_start_col_3] - space_in_sections * (
                                                                nb_rows_G3 - 1 - m)
                                                    box_v_moved_g3.append(
                                                        nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - val_start_col_3)

                                            val_start_col_3 = val_start_col_3 + 1


                                elif len(boxes_under) == 0 and len(boxes[2]['x']) == 0:
                                    space_in_sections = height_von_level_G3 / (
                                            nb_rows_G3 - 1) if nb_rows_G3 > 1 else height_von_level_G3

                                    columns_moved_G3 = int(
                                        len(box_v_moved_g3) / (nb_rows_G3 - 1)) if nb_rows_G3 > 1 else 0
                                    val_start_col_3 = val_start_col_3 if 'val_start_col_3' in locals() and val_start_col_3 > 0 else 0
                                    for p in range(nb_columns_G3 - columns_moved_G3):
                                        for m in range(nb_rows_G3 - 1):
                                            boxes[3]['y'][nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - val_start_col_3] = \
                                                boxes[3]['y'][nb_columns_G3 * (
                                                        nb_rows_G3 - 1 * m) - 1 - val_start_col_3] - space_in_sections * (
                                                        nb_rows_G3 - 1 - m)
                                            box_v_moved_g3.append(
                                                nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - val_start_col_3)
                                        val_start_col_3 = val_start_col_3 + 1
                        else:
                            no_g1_box_moved_g3 = []
                            for b in range(nb_columns_G3 - columns_moved_G3):
                                boxes_under = []
                                for c in range(len(boxes_to_compare_g3)):
                                    if boxes_to_compare_g3[c][2] == 2:
                                        list1 = [
                                            pallet_length - length_val * nb_columns_G3 + b * length_val + columns_moved_G3 * length_val,
                                            pallet_length - length_val * nb_columns_G3 + b * length_val + length_val + columns_moved_G3 * length_val]
                                        list2 = [boxes_to_compare_g3[c][0], boxes_to_compare_g3[c][0] + width_val]
                                        if list1[1] > list2[0] and list2[1] > list1[0]:
                                            boxes_under.append(boxes_to_compare_g3[c])
                                if len(boxes_under) > 0:
                                    boxes_under_closest = boxes_under
                                    if boxes_under_closest[0][2] == 2:
                                        space_hole = height_von_level_G3 - (boxes_under_closest[0][1] + length_val)
                                        if nb_rows_G2 == 1:
                                            space_in_sections = space_hole / (nb_rows_G3 - 1 + 1)
                                            val_start_col_3 = val_start_col_3 if 'val_start_col_3' in locals() and val_start_col_3 > 0 else 0
                                            for m in range(nb_rows_G3 - 1):
                                                boxes[3]['y'][
                                                    nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - val_start_col_3] = \
                                                    boxes[3]['y'][nb_columns_G3 * (
                                                            nb_rows_G3 - 1 * m) - 1 - val_start_col_3] - space_in_sections * (
                                                            nb_rows_G3 - 1 - m)
                                                box_v_moved_g3.append(
                                                    nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - val_start_col_3)
                                                if m == 0:
                                                    no_g1_box_moved_g3.append((boxes[3]['x'][nb_columns_G3 * (
                                                            nb_rows_G3 - 1 * m) - 1 - val_start_col_3],
                                                                               boxes[3]['y'][nb_columns_G3 * (
                                                                                       nb_rows_G3 - 1 * m) - 1 - val_start_col_3],
                                                                               3, 1))
                                            val_start_col_3 = val_start_col_3 + 1
                                        elif nb_rows_G2 > 1:
                                            space_in_sections = space_hole / (nb_rows_G2 - 1 + nb_rows_G3 - 1 + 1)
                                            val_start_col_2 = val_start_col_2 if 'val_start_col_2' in locals() and val_start_col_2 > 0 else 0
                                            for n in range(nb_rows_G2 - 1):
                                                boxes[2]['y'][
                                                    nb_columns_G2 * nb_rows_G2 - 1 - n * nb_columns_G2 - 1 * val_start_col_2] = \
                                                    boxes[2]['y'][
                                                        nb_columns_G2 * nb_rows_G2 - 1 - n * nb_columns_G2 - 1 * val_start_col_2] + space_in_sections * (
                                                            nb_rows_G2 - 1 - n)
                                                box_v_moved_g2.append(
                                                    nb_columns_G2 * nb_rows_G2 - 1 - n * nb_columns_G2 - 1 * val_start_col_2)
                                            val_start_col_2 = val_start_col_2 + 1

                                            val_start_col_3 = val_start_col_3 if 'val_start_col_3' in locals() and val_start_col_3 > 0 else 0
                                            for m in range(nb_rows_G3 - 1):
                                                boxes[3]['y'][
                                                    nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - val_start_col_3] = \
                                                    boxes[3]['y'][nb_columns_G3 * (
                                                            nb_rows_G3 - 1 * m) - 1 - val_start_col_3] - space_in_sections * (
                                                            nb_rows_G3 - 1 - m)
                                                box_v_moved_g3.append(
                                                    nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - val_start_col_3)
                                                if m == 0:
                                                    no_g1_box_moved_g3.append((boxes[3]['x'][nb_columns_G3 * (
                                                            nb_rows_G3 - 1 * m) - 1 - val_start_col_3],
                                                                               boxes[3]['y'][nb_columns_G3 * (
                                                                                       nb_rows_G3 - 1 * m) - 1 - val_start_col_3],
                                                                               3, 1))

                                            val_start_col_3 = val_start_col_3 + 1




                                else:
                                    space_in_sections = height_von_level_G3 / (
                                            nb_rows_G3 - 1) if nb_rows_G3 > 1 else height_von_level_G3
                                    columns_moved_G3 = int(
                                        len(box_v_moved_g3) / (nb_rows_G3 - 1)) if nb_rows_G3 > 1 else 0
                                    for p in range(nb_columns_G3 - columns_moved_G3):
                                        for m in range(nb_rows_G3 - 1):
                                            boxes[3]['y'][
                                                nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - 1 * p - columns_moved_G3] = \
                                                boxes[3]['y'][nb_columns_G3 * (
                                                        nb_rows_G3 - 1 * m) - 1 - 1 * p - columns_moved_G3] - space_in_sections * (
                                                        nb_rows_G3 - 1 - m)
                                            box_v_moved_g3.append(
                                                nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - 1 * p - columns_moved_G3)
                                            if m == 0:
                                                no_g1_box_moved_g3.append((boxes[3]['x'][nb_columns_G3 * (
                                                        nb_rows_G3 - 1 * m) - 1 - 1 * p - columns_moved_G3],
                                                                           boxes[3]['y'][nb_columns_G3 * (
                                                                                   nb_rows_G3 - 1 * m) - 1 - 1 * p - columns_moved_G3],
                                                                           3, 1))
                                    break

                else:
                    space_in_sections = height_von_level_G3 / (
                            nb_rows_G3 - 1) if nb_rows_G3 > 1 else height_von_level_G3
                    columns_moved_G3 = int(len(box_v_moved_g3) / (nb_rows_G3 - 1)) if nb_rows_G3 > 1 else 0
                    for p in range(nb_columns_G3 - columns_moved_G3):
                        for m in range(nb_rows_G3 - 1):
                            boxes[3]['y'][nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - 1 * p - columns_moved_G3] = \
                                boxes[3]['y'][nb_columns_G3 * (
                                        nb_rows_G3 - 1 * m) - 1 - 1 * p - columns_moved_G3] - space_in_sections * (
                                        nb_rows_G3 - 1 - m)
                            box_v_moved_g3.append(nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - 1 * p - columns_moved_G3)

        if li == 0 and len(boxes[2]['x']) != 0:

            nb_rows_G2 = nb_rows_G2 if 'nb_rows_G2' in locals() else len(set(boxes[2]['y']))
            nb_columns_G2 = nb_columns_G2 if 'nb_columns_G2' in locals() else len(set(boxes[2]['x']))
            height_von_level_G2 = height_von_level_G2 if 'height_von_level_G2' in locals() else max(boxes[2]['y'])

            if len(boxes[3]['x']) != 0:
                nb_rows_G3 = nb_rows_G3 if 'nb_rows_G3' in locals() else len(set(boxes[3]['y']))
                nb_columns_G3 = nb_columns_G3 if 'nb_columns_G3' in locals() else len(set(boxes[3]['x']))
                height_von_level_G3 = height_von_level_G3 if 'height_von_level_G3' in locals() else min(boxes[3]['y'])

                if len(boxes[4]['x']) != 0:
                    nb_rows_G4 = nb_rows_G4 if 'nb_rows_G4' in locals() else len(set(boxes[4]['y']))
                    nb_columns_G4 = nb_columns_G4 if 'nb_columns_G4' in locals() else len(set(boxes[4]['x']))
                    height_von_level_G4 = height_von_level_G4 if 'height_von_level_G4' in locals() else min(
                        boxes[4]['y'])

                    boxes_to_compare_g2 = []
                    for q in range(nb_columns_G4):
                        boxes_to_compare_g2.append((boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * q],
                                                    boxes[4]['y'][nb_rows_G4 - 1 + nb_rows_G4 * q], 4, 0))
                    for c in range(nb_columns_G3):
                        boxes_to_compare_g2.append((boxes[3]['x'][nb_columns_G3 * (nb_rows_G3) - 1 - 1 * c],
                                                    boxes[3]['y'][nb_columns_G3 * (nb_rows_G3) - 1 - 1 * c], 3, 0))

                else:
                    boxes_to_compare_g2 = []
                    for c in range(nb_columns_G3):
                        boxes_to_compare_g2.append((boxes[3]['x'][nb_columns_G3 * (nb_rows_G3) - 1 - 1 * c],
                                                    boxes[3]['y'][nb_columns_G3 * (nb_rows_G3) - 1 - 1 * c], 3, 0))
            elif len(boxes[4]['x']) != 0:
                nb_rows_G4 = nb_rows_G4 if 'nb_rows_G4' in locals() else len(set(boxes[4]['y']))
                nb_columns_G4 = nb_columns_G4 if 'nb_columns_G4' in locals() else len(set(boxes[4]['x']))
                height_von_level_G4 = height_von_level_G4 if 'height_von_level_G4' in locals() else min(boxes[4]['y'])

                boxes_to_compare_g2 = []
                for q in range(nb_columns_G4):
                    boxes_to_compare_g2.append((boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * q],
                                                boxes[4]['y'][nb_rows_G4 - 1 + nb_rows_G4 * q], 4, 0))
            else:
                boxes_to_compare_g2 = []

            if 'boxes_to_compare_g1' in locals():
                if len(boxes_to_compare_g1) != 0:
                    if len(boxes_to_compare_g2) != 0:
                        for r in range(len(boxes_to_compare_g2)):
                            for e in range(len(boxes_to_compare_g1)):
                                if boxes_to_compare_g1[e][0] == boxes_to_compare_g2[r][0] and \
                                        boxes_to_compare_g1[e][1] == boxes_to_compare_g2[r][1] and \
                                        boxes_to_compare_g1[e][2] == boxes_to_compare_g2[r][2]:
                                    list_update = list(boxes_to_compare_g2[r])
                                    list_update[3] = boxes_to_compare_g1[e][3]
                                    tuple_update = tuple(list_update)
                                    boxes_to_compare_g2[r] = tuple_update
            else:
                if 'no_g1_box_moved_g4' in locals():
                    if len(no_g1_box_moved_g4) != 0:
                        if len(boxes_to_compare_g2) != 0:
                            for r in range(len(boxes_to_compare_g2)):
                                for e in range(len(no_g1_box_moved_g4)):
                                    if no_g1_box_moved_g4[e][0] == boxes_to_compare_g2[r][0] and \
                                            no_g1_box_moved_g4[e][1] == boxes_to_compare_g2[r][1] and \
                                            no_g1_box_moved_g4[e][2] == boxes_to_compare_g2[r][2]:
                                        list_update = list(boxes_to_compare_g2[r])
                                        list_update[3] = no_g1_box_moved_g4[e][3]
                                        tuple_update = tuple(list_update)
                                        boxes_to_compare_g2[r] = tuple_update
                if 'no_g1_box_moved_g3' in locals():
                    if len(no_g1_box_moved_g3) != 0:
                        if len(boxes_to_compare_g2) != 0:
                            for r in range(len(boxes_to_compare_g2)):
                                for e in range(len(no_g1_box_moved_g3)):
                                    if no_g1_box_moved_g3[e][0] == boxes_to_compare_g2[r][0] and \
                                            no_g1_box_moved_g3[e][1] == boxes_to_compare_g2[r][1] and \
                                            no_g1_box_moved_g3[e][2] == boxes_to_compare_g2[r][2]:
                                        list_update = list(boxes_to_compare_g2[r])
                                        list_update[3] = no_g1_box_moved_g3[e][3]
                                        tuple_update = tuple(list_update)
                                        boxes_to_compare_g2[r] = tuple_update

            # print('boxes to compare g2:',boxes_to_compare_g2 )
            if len(boxes_to_compare_g2) != 0:

                columns_moved_G2 = int(len(box_v_moved_g2) / (nb_rows_G2 - 1)) if nb_rows_G2 > 1 else len(
                    box_v_moved_g2)

                if 'nb_columns_G4' in locals():
                    columns_moved_G4 = int(len(box_v_moved_g4) / (nb_rows_G4 - 1)) if nb_rows_G4 > 1 else len(
                        box_v_moved_g4)

                for b in range(nb_columns_G2 - columns_moved_G2):
                    boxes_above = []
                    for c in range(len(boxes_to_compare_g2)):
                        if boxes_to_compare_g2[c][2] == 3:
                            list1 = [
                                pallet_length - width_val * nb_columns_G2 + columns_moved_G2 * width_val + b * width_val,
                                pallet_length - width_val * nb_columns_G2 + columns_moved_G2 * width_val + b * width_val + width_val]
                            list2 = [boxes_to_compare_g2[c][0], boxes_to_compare_g2[c][0] + length_val]
                            if list1[1] > list2[0] and list2[1] > list1[0]:
                                boxes_above.append(boxes_to_compare_g2[c])
                        if boxes_to_compare_g2[c][2] == 4:
                            list1 = [
                                pallet_length - width_val * nb_columns_G2 + columns_moved_G2 * width_val + b * width_val,
                                pallet_length - width_val * nb_columns_G2 + columns_moved_G2 * width_val + b * width_val + width_val]
                            list2 = [boxes_to_compare_g2[c][0], boxes_to_compare_g2[c][0] + width_val]
                            if list1[1] > list2[0] and list2[1] > list1[0]:
                                boxes_above.append(boxes_to_compare_g2[c])

                    # print(boxes_above)
                    groups = [c[2] for c in boxes_above]
                    if len(set(groups)) == 2:
                        values_y = [a[1] for a in boxes_above]
                        boxes_min_height = [a for a in boxes_above if a[1] == min(values_y)]
                        boxes_not_yet_vm = [b for b in boxes_min_height if b[3] == 0]
                        if len(boxes_not_yet_vm) == 0:

                            hole_distance = boxes_min_height[0][1] - (height_von_level_G2 + length_val)
                            space_in_sections = hole_distance / (nb_rows_G2 - 1 + 1)
                            for n in range(nb_rows_G2 - 1):
                                boxes[2]['y'][
                                    nb_columns_G2 * nb_rows_G2 - 1 - nb_columns_G2 * n - 1 * b - columns_moved_G2] = \
                                    boxes[2]['y'][
                                        nb_columns_G2 * nb_rows_G2 - 1 - nb_columns_G2 * n - 1 * b - columns_moved_G2] + space_in_sections * (
                                            nb_rows_G2 - 1 - n)
                                box_v_moved_g2.append(
                                    nb_columns_G2 * nb_rows_G2 - 1 - nb_columns_G2 * n - 1 * b - columns_moved_G2)
                            continue

                    else:
                        boxes_not_yet_vm = [tup for tup in boxes_above if tup[3] == 0]

                    if len(boxes_not_yet_vm) == 0:

                        if len(boxes_above) == 0:

                            space_in_sections = (pallet_width - (height_von_level_G2 + length_val)) / (
                                    nb_rows_G2 - 1) if nb_rows_G2 > 1 else (
                                    pallet_width - (height_von_level_G2 + length_val))

                            for m in range(nb_rows_G2 - 1):
                                boxes[2]['y'][
                                    nb_columns_G2 * nb_rows_G2 - 1 - nb_columns_G2 * m - columns_moved_G2 - 1 * b] = \
                                    boxes[2]['y'][
                                        nb_columns_G2 * nb_rows_G2 - 1 - nb_columns_G2 * m - columns_moved_G2 - 1 * b] + space_in_sections * (
                                            nb_rows_G2 - 1 - m)
                                box_v_moved_g2.append(
                                    nb_columns_G2 * nb_rows_G2 - 1 - nb_columns_G2 * m - columns_moved_G2 - 1 * b)

                            continue
                        # continue
                        else:
                            if nb_rows_G2 > 1:

                                boxes_above_closest = [tup for tup in boxes_above if
                                                       tup[1] == min(boxes_above, key=lambda t: t[1])[1]]
                                hole_distance = boxes_above_closest[0][1] - (height_von_level_G2 + length_val)
                                space_in_sections = hole_distance / (nb_rows_G2 - 1 + 1)
                                for n in range(nb_rows_G2 - 1):
                                    boxes[2]['y'][
                                        nb_columns_G2 * nb_rows_G2 - 1 - nb_columns_G2 * n - 1 * b - columns_moved_G2] = \
                                        boxes[2]['y'][
                                            nb_columns_G2 * nb_rows_G2 - 1 - nb_columns_G2 * n - 1 * b - columns_moved_G2] + space_in_sections * (
                                                nb_rows_G2 - 1 - n)
                                    box_v_moved_g2.append(
                                        nb_columns_G2 * nb_rows_G2 - 1 - nb_columns_G2 * n - 1 * b - columns_moved_G2)

                                set_list = set(boxes_above_closest)
                                result = [idx for idx, tup in enumerate(boxes_to_compare_g2) if tup in set_list]
                                for t in result:
                                    boxes_to_compare_g2[t] = (
                                        boxes_to_compare_g2[t][0], boxes_to_compare_g2[t][1], boxes_to_compare_g2[t][2],
                                        1)
                                continue
                            else:
                                continue
                    else:

                        boxes_above_closest = [tup for tup in boxes_above if
                                               tup[1] == min(boxes_not_yet_vm, key=lambda t: t[1])[1] and tup[3] == 0]
                        hole_distance = boxes_above_closest[0][1] - (height_von_level_G2 + length_val) if len(
                            boxes_above_closest) != 0 else "Hole with pallet edge"

                    if hole_distance == "Hole with pallet edge":
                        space_in_sections = (pallet_width - (height_von_level_G2 + length_val)) / (nb_rows_G2 - 1)
                        for p in range(nb_columns_G2 - columns_moved_G2):
                            for m in range(nb_rows_G2 - 1):
                                boxes[2]['y'][
                                    nb_columns_G2 * nb_rows_G2 - 1 - nb_columns_G2 * m - 1 * p - columns_moved_G2] = \
                                    boxes[2]['y'][
                                        nb_columns_G2 * nb_rows_G2 - 1 - nb_columns_G2 * m - 1 * p - columns_moved_G2] + space_in_sections * (
                                            nb_rows_G2 - 1 - m)
                                box_v_moved_g2.append(
                                    nb_columns_G2 * nb_rows_G2 - 1 - nb_columns_G2 * m - 1 * p - columns_moved_G2)
                        break
                    else:

                        n_rows_g = locals()['nb_rows_G' + str(boxes_above_closest[0][2])]

                        if n_rows_g > 1:
                            if nb_rows_G2 > 1:

                                space_in_sections = hole_distance / (nb_rows_G2 - 1 + n_rows_g - 1 + 1)
                                for n in range(nb_rows_G2 - 1):
                                    boxes[2]['y'][
                                        nb_columns_G2 * nb_rows_G2 - 1 - nb_columns_G2 * n - 1 * b - columns_moved_G2] = \
                                        boxes[2]['y'][
                                            nb_columns_G2 * nb_rows_G2 - 1 - nb_columns_G2 * n - 1 * b - columns_moved_G2] + space_in_sections * (
                                                nb_rows_G2 - 1 - n)
                                    box_v_moved_g2.append(
                                        nb_columns_G2 * nb_rows_G2 - 1 - nb_columns_G2 * n - 1 * b - columns_moved_G2)

                                if boxes_above_closest[0][2] == 3:
                                    val_start_col_3 = val_start_col_3 if 'val_start_col_3' in locals() and val_start_col_3 > 0 else 0
                                    for p in range(len(boxes_above_closest)):
                                        for m in range(nb_rows_G3 - 1):
                                            boxes[3]['y'][
                                                nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - 1 * p - val_start_col_3] = \
                                                boxes[3]['y'][nb_columns_G3 * (
                                                        nb_rows_G3 - 1 * m) - 1 - 1 * p - val_start_col_3] - space_in_sections * (
                                                        n_rows_g - 1 - m)
                                            box_v_moved_g3.append(
                                                nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - 1 * p - val_start_col_3)
                                            if m == 0:
                                                result = [idx for idx, tup in enumerate(boxes_to_compare_g2) if
                                                          tup in {boxes_above_closest[p]}]
                                                boxes_to_compare_g2[result[0]] = (boxes_to_compare_g2[result[0]][0],
                                                                                  boxes[3]['y'][nb_columns_G3 * (
                                                                                          nb_rows_G3 - 1 * m) - 1 - 1 * p - val_start_col_3],
                                                                                  boxes_to_compare_g2[result[0]][2],
                                                                                  boxes_to_compare_g2[result[0]][3])
                                                boxes_above_closest[p] = (boxes_above_closest[p][0],
                                                                          boxes[3]['y'][nb_columns_G3 * (
                                                                                  nb_rows_G3 - 1 * m) - 1 - 1 * p - val_start_col_3],
                                                                          boxes_above_closest[p][2],
                                                                          boxes_above_closest[p][3])

                                    val_start_col_3 = val_start_col_3 + len(boxes_above_closest)
                                elif boxes_above_closest[0][2] == 4:
                                    val_start_col_4 = val_start_col_4 if 'val_start_col_4' in locals() and val_start_col_4 > 0 else 0
                                    for q in range(len(boxes_above_closest)):
                                        for j in range(nb_rows_G4 - 1):

                                            boxes[4]['y'][nb_rows_G4 - 1 - j + nb_rows_G4 * q + val_start_col_4] = \
                                                boxes[4]['y'][
                                                    nb_rows_G4 - 1 - j + nb_rows_G4 * q + val_start_col_4] - space_in_sections * (
                                                        nb_rows_G4 - 1 - n)
                                            box_v_moved_g4.append(nb_rows_G4 - 1 - j + nb_rows_G4 * q + val_start_col_4)
                                            if j == 0:
                                                result = [idx for idx, tup in enumerate(boxes_to_compare_g2) if
                                                          tup in {boxes_above_closest[q]}]

                                                boxes_to_compare_g2[result[0]] = (boxes_to_compare_g2[result[0]][0],
                                                                                  boxes[4]['y'][
                                                                                      nb_rows_G4 - 1 + nb_rows_G4 * q + val_start_col_4],
                                                                                  boxes_to_compare_g2[result[0]][2],
                                                                                  boxes_to_compare_g2[result[0]][3])
                                                boxes_above_closest[q] = (boxes_above_closest[q][0],
                                                                          boxes[4]['y'][
                                                                              nb_rows_G4 - 1 + nb_rows_G4 * q + val_start_col_4],
                                                                          boxes_above_closest[q][2],
                                                                          boxes_above_closest[q][3])

                                    val_start_col_4 = val_start_col_4 + nb_rows_G4 * len(boxes_above_closest)

                                set_list = set(boxes_above_closest)
                                result = [idx for idx, tup in enumerate(boxes_to_compare_g2) if tup in set_list]
                                for t in result:
                                    boxes_to_compare_g2[t] = (
                                        boxes_to_compare_g2[t][0], boxes_to_compare_g2[t][1], boxes_to_compare_g2[t][2],
                                        1)

                            else:
                                space_in_sections = hole_distance / (n_rows_g - 1 + 1)
                                if boxes_above_closest[0][2] == 3:
                                    val_start_col_3 = val_start_col_3 if 'val_start_col_3' in locals() and val_start_col_3 > 0 else 0

                                    for p in range(len(boxes_above_closest)):
                                        for m in range(nb_rows_G3 - 1):

                                            boxes[3]['y'][
                                                nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - 1 * p - val_start_col_3] = \
                                                boxes[3]['y'][nb_columns_G3 * (
                                                        nb_rows_G3 - 1 * m) - 1 - 1 * p - val_start_col_3] - space_in_sections * (
                                                        n_rows_g - 1 - m)
                                            box_v_moved_g3.append(
                                                nb_columns_G3 * (nb_rows_G3 - 1 * m) - 1 - 1 * p - val_start_col_3)
                                            if m == 0:
                                                result = [idx for idx, tup in enumerate(boxes_to_compare_g2) if
                                                          tup in {boxes_above_closest[p]}]
                                                boxes_to_compare_g2[result[0]] = (boxes_to_compare_g2[result[0]][0],
                                                                                  boxes[3]['y'][nb_columns_G3 * (
                                                                                          nb_rows_G3 - 1 * m) - 1 - 1 * p - val_start_col_3],
                                                                                  boxes_to_compare_g2[result[0]][2],
                                                                                  boxes_to_compare_g2[result[0]][3])
                                                boxes_above_closest[p] = (boxes_above_closest[p][0],
                                                                          boxes[3]['y'][nb_columns_G3 * (
                                                                                  nb_rows_G3 - 1 * m) - 1 - 1 * p - val_start_col_3],
                                                                          boxes_above_closest[p][2],
                                                                          boxes_above_closest[p][3])

                                    val_start_col_3 = val_start_col_3 + len(boxes_above_closest)
                                elif boxes_above_closest[0][2] == 4:
                                    val_start_col_4 = val_start_col_4 if 'val_start_col_4' in locals() and val_start_col_4 > 0 else 0
                                    for q in range(len(boxes_above_closest)):
                                        for j in range(nb_rows_G4 - 1):

                                            boxes[4]['y'][nb_rows_G4 - 1 - j + nb_rows_G4 * q + val_start_col_4] = \
                                                boxes[4]['y'][
                                                    nb_rows_G4 - 1 - j + nb_rows_G4 * q + val_start_col_4] - space_in_sections * (
                                                        nb_rows_G4 - 1 - j)
                                            box_v_moved_g4.append(nb_rows_G4 - 1 - j + nb_rows_G4 * q + val_start_col_4)
                                            if j == 0:
                                                result = [idx for idx, tup in enumerate(boxes_to_compare_g2) if
                                                          tup in {boxes_above_closest[q]}]

                                                boxes_to_compare_g2[result[0]] = (boxes_to_compare_g2[result[0]][0],
                                                                                  boxes[4]['y'][
                                                                                      nb_rows_G4 - 1 + nb_rows_G4 * q + val_start_col_4],
                                                                                  boxes_to_compare_g2[result[0]][2],
                                                                                  boxes_to_compare_g2[result[0]][3])
                                                boxes_above_closest[q] = (boxes_above_closest[q][0],
                                                                          boxes[4]['y'][
                                                                              nb_rows_G4 - 1 + nb_rows_G4 * q + val_start_col_4],
                                                                          boxes_above_closest[q][2],
                                                                          boxes_above_closest[q][3])

                                    val_start_col_4 = val_start_col_4 + nb_rows_G4 * len(boxes_above_closest)

                                set_list = set(boxes_above_closest)
                                result = [idx for idx, tup in enumerate(boxes_to_compare_g2) if tup in set_list]
                                for t in result:
                                    boxes_to_compare_g2[t] = (
                                        boxes_to_compare_g2[t][0], boxes_to_compare_g2[t][1], boxes_to_compare_g2[t][2],
                                        1)

                        else:
                            if nb_rows_G2 > 1:
                                space_in_sections = hole_distance / (nb_rows_G2 - 1 + 1)
                                for n in range(nb_rows_G2 - 1):
                                    boxes[2]['y'][
                                        nb_columns_G2 * nb_rows_G2 - 1 - nb_columns_G2 * n - 1 * b - columns_moved_G2] = \
                                        boxes[2]['y'][
                                            nb_columns_G2 * nb_rows_G2 - 1 - nb_columns_G2 * n - 1 * b - columns_moved_G2] + space_in_sections * (
                                                nb_rows_G2 - 1 - n)
                                    box_v_moved_g2.append(
                                        nb_columns_G2 * nb_rows_G2 - 1 - nb_columns_G2 * n - 1 * b - columns_moved_G2)

                                set_list = set(boxes_above_closest)
                                result = [idx for idx, tup in enumerate(boxes_to_compare_g2) if tup in set_list]
                                for t in result:
                                    boxes_to_compare_g2[t] = (
                                        boxes_to_compare_g2[t][0], boxes_to_compare_g2[t][1], boxes_to_compare_g2[t][2],
                                        1)
                                # break
                            else:
                                space_in_sections = 0

            else:
                space_in_sections = (pallet_width - (height_von_level_G2 + length_val)) / (
                        nb_rows_G2 - 1) if nb_rows_G2 > 1 else (pallet_width - (height_von_level_G2 + length_val))
                columns_moved_G2 = int(len(box_v_moved_g2) / ((nb_rows_G2 - 1))) if len(
                    box_v_moved_g2) > nb_columns_G2 else len(box_v_moved_g2)
                for p in range(nb_columns_G2 - columns_moved_G2):
                    for m in range(nb_rows_G2 - 1):
                        boxes[2]['y'][nb_columns_G2 * nb_rows_G2 - 1 - nb_columns_G2 * m - 1 * p - columns_moved_G2] = \
                            boxes[2]['y'][
                                nb_columns_G2 * nb_rows_G2 - 1 - nb_columns_G2 * m - 1 * p - columns_moved_G2] + space_in_sections * (
                                    nb_rows_G2 - 1 - m)
                        box_v_moved_g2.append(
                            nb_columns_G2 * nb_rows_G2 - 1 - nb_columns_G2 * m - 1 * p - columns_moved_G2)

    #####################################################################################################################################################################################################################################################

    box_h_moved_g1 = []
    box_h_moved_g2 = []
    box_h_moved_g3 = []
    box_h_moved_g4 = []

    # if 'nb_rows_G1' in locals(): del nb_rows_G1
    # if 'nb_columns_G1' in locals(): del nb_columns_G1
    if 'length_von_level_G1' in locals(): del length_von_level_G1

    # if 'nb_rows_G2' in locals(): del nb_rows_G2
    # if 'nb_columns_G2' in locals(): del nb_columns_G2
    if 'length_von_level_G2' in locals(): del length_von_level_G2

    # if 'nb_rows_G3' in locals(): del nb_rows_G3
    # if 'nb_columns_G3' in locals(): del nb_columns_G3
    if 'length_von_level_G3' in locals(): del length_von_level_G3

    # if 'nb_rows_G4' in locals(): del nb_rows_G4
    # if 'nb_columns_G4' in locals(): del nb_columns_G4
    if 'length_von_level_G4' in locals(): del length_von_level_G4

    if 'val_start_row_4' in locals(): del val_start_row_4
    if 'val_start_row_3' in locals(): del val_start_row_3
    if 'val_start_row_2' in locals(): del val_start_row_2
    if 'val_start_row_1' in locals(): del val_start_row_1

    if 'boxes_to_compare_g1' in locals(): del boxes_to_compare_g1
    if 'boxes_to_compare_g2' in locals(): del boxes_to_compare_g2

    if 'val1_to_compare' in locals(): del val1_to_compare
    if 'val2_to_compare' in locals(): del val2_to_compare
    if 'val3_to_compare' in locals(): del val3_to_compare

    for li in range(1):
        if li == 0 and len(boxes[2]['x']) != 0:
            nb_rows_G2 = nb_rows_G2 if 'nb_rows_G2' in locals() else len(set(boxes[2]['y']))
            nb_columns_G2 = nb_columns_G2 if 'nb_columns_G2' in locals() else len(set(boxes[2]['x']))
            length_von_level_G2 = length_von_level_G2 if 'length_von_level_G2' in locals() else min(boxes[2]['x'])

            if len(boxes[1]['x']) != 0:
                nb_rows_G1 = nb_rows_G1 if 'nb_rows_G1' in locals() else len(set(boxes[1]['y']))
                nb_columns_G1 = nb_columns_G1 if 'nb_columns_G1' in locals() else len(set(boxes[1]['x']))
                length_von_level_G1 = length_von_level_G1 if 'length_von_level_G1' in locals() else max(boxes[1]['x'])

                if len(boxes[4]['x']) != 0:
                    nb_rows_G4 = nb_rows_G4 if 'nb_rows_G4' in locals() else len(set(boxes[4]['y']))
                    nb_columns_G4 = nb_columns_G4 if 'nb_columns_G4' in locals() else len(set(boxes[4]['x']))
                    length_von_level_G4 = length_von_level_G4 if 'length_von_level_G4' in locals() else max(
                        boxes[4]['x'])

                    boxes_to_compare_g2 = []
                    for q in range(nb_rows_G1):
                        boxes_to_compare_g2.append((boxes[1]['x'][nb_columns_G1 * q + (nb_columns_G1 - 1)],
                                                    boxes[1]['y'][nb_columns_G1 * q + (nb_columns_G1 - 1)], 1, 0))
                    for c in range(nb_rows_G4):
                        boxes_to_compare_g2.append((
                            boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (nb_columns_G4 - 1) - c],
                            boxes[4]['y'][nb_rows_G4 - 1 + nb_rows_G4 * (nb_columns_G4 - 1) - c],
                            4, 0))
                else:
                    boxes_to_compare_g2 = []
                    for q in range(nb_rows_G1):
                        boxes_to_compare_g2.append((boxes[1]['x'][nb_columns_G1 * q + (nb_columns_G1 - 1)],
                                                    boxes[1]['y'][nb_columns_G1 * q + (nb_columns_G1 - 1)], 1, 0))
            elif len(boxes[4]['x']) != 0:
                nb_rows_G4 = nb_rows_G4 if 'nb_rows_G4' in locals() else len(set(boxes[4]['y']))
                nb_columns_G4 = nb_columns_G4 if 'nb_columns_G4' in locals() else len(set(boxes[4]['x']))
                length_von_level_G4 = length_von_level_G4 if 'length_von_level_G4' in locals() else max(boxes[4]['x'])

                boxes_to_compare_g2 = []
                for c in range(nb_rows_G4):
                    boxes_to_compare_g2.append((boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (nb_columns_G4 - 1) - c],
                                                boxes[4]['y'][nb_rows_G4 - 1 + nb_rows_G4 * (nb_columns_G4 - 1) - c], 4,
                                                0))
            else:
                boxes_to_compare_g2 = []

            ################
            if len(boxes[3]['y']) != 0:
                boxes_from_g3_to_compare = []
                for u in range(nb_rows_G2):
                    for p in range(nb_columns_G3):
                        if boxes[3]['y'][nb_columns_G3 * (nb_rows_G3) - 1 - 1 * p] < boxes[2]['y'][(
                                                                                                           nb_columns_G2 * nb_rows_G2 - 1 - (
                                                                                                           nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * u] + length_val and \
                                boxes[3]['x'][nb_columns_G3 * (nb_rows_G3) - 1 - 1 * p] < boxes[2]['x'][
                            (nb_columns_G2 * nb_rows_G2 - 1 - (nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * u]:
                            boxes_from_g3_to_compare.append((boxes[3]['x'][nb_columns_G3 * (nb_rows_G3) - 1 - 1 * p],
                                                             boxes[3]['y'][nb_columns_G3 * (nb_rows_G3) - 1 - 1 * p], 3,
                                                             0))

                if len(boxes_from_g3_to_compare) != 0:
                    boxes_from_g3_to_compare = list(set(boxes_from_g3_to_compare))
                    boxes_to_compare_g2 = boxes_to_compare_g2 + boxes_from_g3_to_compare
            ################################################

            if len(boxes_to_compare_g2) != 0:
                for b in range(nb_rows_G2):
                    boxes_on_the_side = []
                    start = False
                    for c in range(len(boxes_to_compare_g2)):
                        if boxes_to_compare_g2[c][2] == 1:
                            list1 = [boxes[2]['y'][(nb_columns_G2 * nb_rows_G2 - 1 - (
                                    nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * b],
                                     boxes[2]['y'][(nb_columns_G2 * nb_rows_G2 - 1 - (
                                             nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * b] + length_val]
                            list2 = [boxes_to_compare_g2[c][1], boxes_to_compare_g2[c][1] + width_val]
                            if list1[1] > list2[0] and list2[1] > list1[0]:
                                boxes_on_the_side.append(boxes_to_compare_g2[c])

                        if boxes_to_compare_g2[c][2] == 4:
                            list1 = [boxes[2]['y'][(nb_columns_G2 * nb_rows_G2 - 1 - (
                                    nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * b],
                                     boxes[2]['y'][(nb_columns_G2 * nb_rows_G2 - 1 - (
                                             nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * b] + length_val]
                            list2 = [boxes_to_compare_g2[c][1], boxes_to_compare_g2[c][1] + length_val]
                            if list1[1] > list2[0] and list2[1] > list1[0]:
                                boxes_on_the_side.append(boxes_to_compare_g2[c])

                        if boxes_to_compare_g2[c][2] == 3:
                            list1 = [boxes[2]['y'][(nb_columns_G2 * nb_rows_G2 - 1 - (
                                    nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * b],
                                     boxes[2]['y'][(nb_columns_G2 * nb_rows_G2 - 1 - (
                                             nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * b] + length_val]
                            list2 = [boxes_to_compare_g2[c][1], boxes_to_compare_g2[c][1] + width_val]
                            if list1[1] > list2[0] and list2[1] > list1[0]:
                                boxes_on_the_side.append(boxes_to_compare_g2[c])
                    groups = [c[2] for c in boxes_on_the_side]
                    if len(set(groups)) >= 2:
                        val1_to_compare = None
                        val2_to_compare = None
                        val3_to_compare = None
                        for tup in boxes_on_the_side:
                            if tup[2] == 1:
                                if val1_to_compare is None or tup[0] + length_val > val1_to_compare: val1_to_compare = \
                                    tup[0] + length_val
                            if tup[2] == 4:
                                if val2_to_compare is None or tup[0] + width_val > val2_to_compare: val2_to_compare = \
                                    tup[0] + width_val
                            if tup[2] == 3:
                                if val3_to_compare is None or tup[0] + length_val > val3_to_compare: val3_to_compare = \
                                    tup[0] + length_val
                        LIST = [val1_to_compare, val2_to_compare, val3_to_compare]
                        index = LIST.index(max([i for i in LIST if i is not None]))
                        if index == 0:
                            group_max_value = 1
                        elif index == 1:
                            group_max_value = 4
                        elif index == 2:
                            group_max_value = 3
                        boxes_max_x_pos = [a for a in boxes_on_the_side if a[2] == group_max_value]
                        boxes_not_yet_hm = [t for t in boxes_max_x_pos if t[3] == 0]
                        if len(boxes_not_yet_hm) == 0:
                            if boxes_max_x_pos[0][2] == 1:
                                hole_distance = length_von_level_G2 - (boxes_max_x_pos[0][0] + length_val)
                            elif boxes_max_x_pos[0][2] == 4:
                                hole_distance = length_von_level_G2 - (boxes_max_x_pos[0][0] + width_val)
                            elif boxes_max_x_pos[0][2] == 3:
                                hole_distance = length_von_level_G2 - (
                                        boxes_max_x_pos[0][0] + len(boxes_max_x_pos) * length_val)

                            space_in_sections = hole_distance / (nb_columns_G2 - 1 + 1)
                            for n in range(1, nb_columns_G2):
                                boxes[2]['x'][(nb_columns_G2 * nb_rows_G2 - 1 - (
                                        nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * b - (n - 1)] = \
                                    boxes[2]['x'][(nb_columns_G2 * nb_rows_G2 - 1 - (
                                            nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * b - (
                                                          n - 1)] - space_in_sections * (nb_columns_G2 - n)
                                box_h_moved_g1.append((nb_columns_G2 * nb_rows_G2 - 1 - (
                                        nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * b - (n - 1))

                            boxes_of_group_4_not_yet_moved = [a for a in boxes_on_the_side if a[3] == 0 and a[2] == 4]

                            rows_not_yet_moved = [a for a in boxes_on_the_side if
                                                  a[3] == 0 and a[2] == boxes_max_x_pos[0][2]]

                            if len(rows_not_yet_moved) > 0:
                                hole_distance = boxes[2]['x'][(nb_columns_G2 * nb_rows_G2 - 1 - (
                                        nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * b] - \
                                                rows_not_yet_moved[0][0]
                                if boxes_on_the_side_closest[0][2] == 1 and b != nb_rows_G2 - 1:
                                    val_start_row_1 = val_start_row_1 if 'val_start_row_1' in locals() and val_start_row_1 > 0 else 0
                                    for p in range(len(boxes_on_the_side_closest)):
                                        for m in range(nb_columns_G1 - 1):
                                            boxes[1]['x'][
                                                nb_columns_G1 * p + (nb_columns_G1 - 1) - m + val_start_row_1] = \
                                                boxes[1]['x'][nb_columns_G1 * p + (
                                                        nb_columns_G1 - 1) - m + val_start_row_1] + space_in_sections * (
                                                        n_columns_g - 1 - m)
                                            box_h_moved_g1.append(
                                                nb_columns_G1 * p + (nb_columns_G1 - 1) - m + val_start_row_1)

                                            if m == 0:
                                                result = [idx for idx, tup in enumerate(boxes_to_compare_g2) if
                                                          tup in {boxes_on_the_side_closest[p]}]

                                                boxes_to_compare_g2[result[0]] = (boxes[1]['x'][nb_columns_G1 * p + (
                                                        nb_columns_G1 - 1) - m + val_start_row_1],
                                                                                  boxes_to_compare_g2[result[0]][1],
                                                                                  boxes_to_compare_g2[result[0]][2],
                                                                                  boxes_to_compare_g2[result[0]][3])

                                                boxes_on_the_side_closest[p] = (boxes[1]['x'][nb_columns_G1 * p + (
                                                        nb_columns_G1 - 1) - m + val_start_row_1],
                                                                                boxes_on_the_side_closest[p][1],
                                                                                boxes_on_the_side_closest[p][2],
                                                                                boxes_on_the_side_closest[p][3])
                                    val_start_row_1 = val_start_row_1 + nb_columns_G1 * len(boxes_on_the_side_closest)
                                    set_list = set(boxes_on_the_side_closest)
                                    result = [idx for idx, tup in enumerate(boxes_to_compare_g2) if tup in set_list]
                                    for t in result:
                                        boxes_to_compare_g2[t] = (
                                            boxes_to_compare_g2[t][0], boxes_to_compare_g2[t][1],
                                            boxes_to_compare_g2[t][2],
                                            1)

                                elif boxes_on_the_side_closest[0][2] == 4 and b != nb_rows_G2 - 1:
                                    val_start_row_4 = val_start_row_4 if 'val_start_row_4' in locals() and val_start_row_4 > 0 else 0
                                    for q in range(len(boxes_on_the_side_closest)):
                                        for j in range(nb_columns_G4 - 1):
                                            boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                    nb_columns_G4 - 1) - q - nb_rows_G4 * j - val_start_row_4] = \
                                                boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                        nb_columns_G4 - 1) - q - nb_rows_G4 * j - val_start_row_4] + space_in_sections * (
                                                        nb_columns_G4 - 1 - j)
                                            box_h_moved_g4.append(nb_rows_G4 - 1 + nb_rows_G4 * (
                                                    nb_columns_G4 - 1) - q - nb_rows_G4 * j - val_start_row_4)
                                            if j == 0:
                                                result = [idx for idx, tup in enumerate(boxes_to_compare_g2) if
                                                          tup in {boxes_on_the_side_closest[q]}]
                                                boxes_to_compare_g2[result[0]] = (boxes[4]['x'][
                                                                                      nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                                              nb_columns_G4 - 1) - q - nb_rows_G4 * j - val_start_row_4],
                                                                                  boxes_to_compare_g2[result[0]][1],
                                                                                  boxes_to_compare_g2[result[0]][2],
                                                                                  boxes_to_compare_g2[result[0]][3])
                                                boxes_on_the_side_closest[q] = (boxes[4]['x'][
                                                                                    nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                                            nb_columns_G4 - 1) - q - nb_rows_G4 * j - val_start_row_4],
                                                                                boxes_on_the_side_closest[q][1],
                                                                                boxes_on_the_side_closest[q][2],
                                                                                boxes_on_the_side_closest[q][3])

                                    val_start_row_4 = val_start_row_4 + len(boxes_on_the_side_closest)
                                    set_list = set(boxes_on_the_side_closest)
                                    result = [idx for idx, tup in enumerate(boxes_to_compare_g2) if tup in set_list]
                                    for t in result:
                                        boxes_to_compare_g2[t] = (
                                            boxes_to_compare_g2[t][0], boxes_to_compare_g2[t][1],
                                            boxes_to_compare_g2[t][2],
                                            1)
                            elif len(rows_not_yet_moved) == 0 and len(
                                    boxes_of_group_4_not_yet_moved) != 0 and b != nb_rows_G2 - 1:
                                hole_distance = boxes[2]['x'][(nb_columns_G2 * nb_rows_G2 - 1 - (
                                        nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * b] - (
                                                        boxes_of_group_4_not_yet_moved[0][0] + width_val)
                                space_in_sections = hole_distance / (nb_columns_G4 - 1 + 1)
                                val_start_row_4 = val_start_row_4 if 'val_start_row_4' in locals() and val_start_row_4 > 0 else 0
                                for q in range(len(boxes_of_group_4_not_yet_moved)):
                                    for j in range(nb_columns_G4 - 1):
                                        boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                nb_columns_G4 - 1) - q - nb_rows_G4 * j - val_start_row_4] = \
                                            boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                    nb_columns_G4 - 1) - q - nb_rows_G4 * j - val_start_row_4] + space_in_sections * (
                                                    nb_columns_G4 - 1 - j)
                                        box_h_moved_g4.append(nb_rows_G4 - 1 + nb_rows_G4 * (
                                                nb_columns_G4 - 1) - q - nb_rows_G4 * j - val_start_row_4)
                                        if j == 0:
                                            result = [idx for idx, tup in enumerate(boxes_to_compare_g2) if
                                                      tup in {boxes_of_group_4_not_yet_moved[q]}]
                                            boxes_to_compare_g2[result[0]] = (boxes[4]['x'][
                                                                                  nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                                          nb_columns_G4 - 1) - q - nb_rows_G4 * j - val_start_row_4],
                                                                              boxes_to_compare_g2[result[0]][1],
                                                                              boxes_to_compare_g2[result[0]][2],
                                                                              boxes_to_compare_g2[result[0]][3])
                                            boxes_of_group_4_not_yet_moved[q] = (boxes[4]['x'][
                                                                                     nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                                             nb_columns_G4 - 1) - q - nb_rows_G4 * j - val_start_row_4],
                                                                                 boxes_on_the_side_closest[q][1],
                                                                                 boxes_on_the_side_closest[q][2],
                                                                                 boxes_on_the_side_closest[q][3])

                                val_start_row_4 = val_start_row_4 + len(boxes_of_group_4_not_yet_moved)
                                set_list = set(boxes_of_group_4_not_yet_moved)
                                result = [idx for idx, tup in enumerate(boxes_to_compare_g2) if tup in set_list]
                                for t in result:
                                    boxes_to_compare_g2[t] = (
                                        boxes_to_compare_g2[t][0], boxes_to_compare_g2[t][1], boxes_to_compare_g2[t][2],
                                        1)

                            continue

                    else:
                        boxes_not_yet_hm = [tup for tup in boxes_on_the_side if tup[3] == 0]

                    if len(boxes_not_yet_hm) == 0:
                        if len(boxes_on_the_side) == 0:

                            space_in_sections = length_von_level_G2 / (
                                    nb_columns_G2 - 1) if nb_columns_G2 > 1 else length_von_level_G2
                            for n in range(1, nb_columns_G2):
                                boxes[2]['x'][(nb_columns_G2 * nb_rows_G2 - 1 - (
                                        nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * b - (n - 1)] = \
                                    boxes[2]['x'][(nb_columns_G2 * nb_rows_G2 - 1 - (
                                            nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * b - (
                                                          n - 1)] - space_in_sections * (nb_columns_G2 - n)
                                box_h_moved_g2.append((nb_columns_G2 * nb_rows_G2 - 1 - (
                                        nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * b - (n - 1))
                            continue
                        else:
                            if nb_columns_G2 > 1:
                                boxes_on_the_side_closest = [tup for tup in boxes_on_the_side if
                                                             tup[0] == min(boxes_on_the_side, key=lambda t: t[0])[0]]

                                hole_distance = length_von_level_G2 - (boxes_on_the_side_closest[0][0] + width_val)
                                space_in_sections = hole_distance / (nb_columns_G2 - 1 + 1)
                                for n in range(1, nb_columns_G2):
                                    boxes[2]['x'][(nb_columns_G2 * nb_rows_G2 - 1 - (
                                            nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * b - (n - 1)] = \
                                        boxes[2]['x'][(nb_columns_G2 * nb_rows_G2 - 1 - (
                                                nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * b - (
                                                              n - 1)] - space_in_sections * (nb_columns_G2 - n)
                                    box_h_moved_g2.append((nb_columns_G2 * nb_rows_G2 - 1 - (
                                            nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * b - (n - 1))
                                continue
                            else:
                                continue

                    else:
                        boxes_on_the_side_closest = [tup for tup in boxes_on_the_side if
                                                     tup[0] == max(boxes_not_yet_hm, key=lambda t: t[0])[0] and tup[
                                                         3] == 0]

                        if len(boxes_on_the_side_closest) != 0:
                            if boxes_on_the_side_closest[0][2] == 1:
                                hole_distance = length_von_level_G2 - (boxes_on_the_side_closest[0][0] + length_val)
                            elif boxes_on_the_side_closest[0][2] == 4:
                                hole_distance = length_von_level_G2 - (boxes_on_the_side_closest[0][0] + width_val)
                            elif 'boxes_max_x_pos' in locals():
                                if boxes_on_the_side_closest[0][2] == 3:
                                    hole_distance = length_von_level_G2 - (
                                            boxes_max_x_pos[0][0] + len(boxes_max_x_pos) * length_val)

                        else:
                            hole_distance = "Hole with pallet edge"

                    if hole_distance == "Hole with pallet edge":
                        space_in_sections = length_von_level_G2 / (nb_columns_G2 - 1)
                        for t in range(nb_rows_G2):
                            for n in range(1, nb_columns_G2):
                                boxes[2]['x'][(nb_columns_G2 * nb_rows_G2 - 1 - (
                                        nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * t - (n - 1)] = \
                                    boxes[2]['x'][(nb_columns_G2 * nb_rows_G2 - 1 - (
                                            nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * t - (
                                                          n - 1)] - space_in_sections * (nb_columns_G2 - n)
                                box_h_moved_g2.append((nb_columns_G2 * nb_rows_G2 - 1 - (
                                        nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * t - (n - 1))

                        break
                    else:
                        if 'group_max_value' in locals():
                            if group_max_value == 3:
                                if nb_columns_G2 > 1:
                                    space_in_sections = hole_distance / (nb_columns_G2 - 1 + 1)
                                    for n in range(1, nb_columns_G2):
                                        # print('aqui talvez')
                                        boxes[2]['x'][(nb_columns_G2 * nb_rows_G2 - 1 - (
                                                nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * b - (n - 1)] = \
                                            boxes[2]['x'][(nb_columns_G2 * nb_rows_G2 - 1 - (
                                                    nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * b - (
                                                                  n - 1)] - space_in_sections * (nb_columns_G2 - n)
                                        box_h_moved_g2.append((nb_columns_G2 * nb_rows_G2 - 1 - (
                                                nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * b - (n - 1))
                                continue

                        n_columns_g = locals()['nb_columns_G' + str(boxes_on_the_side_closest[0][2])]
                        if n_columns_g > 1:

                            if nb_columns_G2 > 1:

                                space_in_sections = hole_distance / (nb_columns_G2 - 1 + n_columns_g - 1 + 1)
                                for n in range(1, nb_columns_G2):
                                    boxes[2]['x'][(nb_columns_G2 * nb_rows_G2 - 1 - (
                                            nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * b - (n - 1)] = \
                                        boxes[2]['x'][(nb_columns_G2 * nb_rows_G2 - 1 - (
                                                nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * b - (
                                                              n - 1)] - space_in_sections * (nb_columns_G2 - n)
                                    box_h_moved_g2.append((nb_columns_G2 * nb_rows_G2 - 1 - (
                                            nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * b - (n - 1))

                                if boxes_on_the_side_closest[0][2] == 1 and b != nb_rows_G2 - 1:

                                    val_start_row_1 = val_start_row_1 if 'val_start_row_1' in locals() and val_start_row_1 > 0 else 0
                                    for p in range(len(boxes_on_the_side_closest)):
                                        for m in range(nb_columns_G1 - 1):
                                            boxes[1]['x'][
                                                nb_columns_G1 * p + (nb_columns_G1 - 1) - m + val_start_row_1] = \
                                                boxes[1]['x'][nb_columns_G1 * p + (
                                                        nb_columns_G1 - 1) - m + val_start_row_1] + space_in_sections * (
                                                        n_columns_g - 1 - m)
                                            box_h_moved_g1.append(
                                                nb_columns_G1 * p + (nb_columns_G1 - 1) - m + val_start_row_1)

                                            if m == 0:
                                                result = [idx for idx, tup in enumerate(boxes_to_compare_g2) if
                                                          tup in {boxes_on_the_side_closest[p]}]

                                                boxes_to_compare_g2[result[0]] = (boxes[1]['x'][nb_columns_G1 * p + (
                                                        nb_columns_G1 - 1) - m + val_start_row_1],
                                                                                  boxes_to_compare_g2[result[0]][1],
                                                                                  boxes_to_compare_g2[result[0]][2],
                                                                                  boxes_to_compare_g2[result[0]][3])

                                                boxes_on_the_side_closest[p] = (boxes[1]['x'][nb_columns_G1 * p + (
                                                        nb_columns_G1 - 1) - m + val_start_row_1],
                                                                                boxes_on_the_side_closest[p][1],
                                                                                boxes_on_the_side_closest[p][2],
                                                                                boxes_on_the_side_closest[p][3])

                                    val_start_row_1 = val_start_row_1 + nb_columns_G1 * len(boxes_on_the_side_closest)
                                    set_list = set(boxes_on_the_side_closest)
                                    result = [idx for idx, tup in enumerate(boxes_to_compare_g2) if tup in set_list]

                                    for t in result:
                                        boxes_to_compare_g2[t] = (
                                            boxes_to_compare_g2[t][0], boxes_to_compare_g2[t][1],
                                            boxes_to_compare_g2[t][2],
                                            1)

                                elif boxes_on_the_side_closest[0][2] == 4 and b != nb_rows_G2 - 1:
                                    val_start_row_4 = val_start_row_4 if 'val_start_row_4' in locals() and val_start_row_4 > 0 else 0
                                    for q in range(len(boxes_on_the_side_closest)):
                                        for j in range(nb_columns_G4 - 1):
                                            boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                    nb_columns_G4 - 1) - q - nb_rows_G4 * j - val_start_row_4] = \
                                                boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                        nb_columns_G4 - 1) - q - nb_rows_G4 * j - val_start_row_4] + space_in_sections * (
                                                        nb_columns_G4 - 1 - j)
                                            box_h_moved_g4.append(nb_rows_G4 - 1 + nb_rows_G4 * (
                                                    nb_columns_G4 - 1) - q - nb_rows_G4 * j - val_start_row_4)
                                            if j == 0:
                                                result = [idx for idx, tup in enumerate(boxes_to_compare_g2) if
                                                          tup in {boxes_on_the_side_closest[q]}]
                                                boxes_to_compare_g2[result[0]] = (boxes[4]['x'][
                                                                                      nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                                              nb_columns_G4 - 1) - q - nb_rows_G4 * j - val_start_row_4],
                                                                                  boxes_to_compare_g2[result[0]][1],
                                                                                  boxes_to_compare_g2[result[0]][2],
                                                                                  boxes_to_compare_g2[result[0]][3])
                                                boxes_on_the_side_closest[q] = (boxes[4]['x'][
                                                                                    nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                                            nb_columns_G4 - 1) - q - nb_rows_G4 * j - val_start_row_4],
                                                                                boxes_on_the_side_closest[q][1],
                                                                                boxes_on_the_side_closest[q][2],
                                                                                boxes_on_the_side_closest[q][3])

                                    val_start_row_4 = val_start_row_4 + len(boxes_on_the_side_closest)
                                    set_list = set(boxes_on_the_side_closest)
                                    result = [idx for idx, tup in enumerate(boxes_to_compare_g2) if tup in set_list]
                                    for t in result:
                                        boxes_to_compare_g2[t] = (
                                            boxes_to_compare_g2[t][0], boxes_to_compare_g2[t][1],
                                            boxes_to_compare_g2[t][2],
                                            1)


                            else:
                                space_in_sections = hole_distance / (n_columns_g - 1 + 1)

                                if boxes_on_the_side_closest[0][2] == 1 and b != nb_rows_G2 - 1:

                                    val_start_row_1 = val_start_row_1 if 'val_start_row_1' in locals() and val_start_row_1 > 0 else 0
                                    for p in range(len(boxes_on_the_side_closest)):
                                        for m in range(nb_columns_G1 - 1):
                                            boxes[1]['x'][
                                                nb_columns_G1 * p + (nb_columns_G1 - 1) - m + val_start_row_1] = \
                                                boxes[1]['x'][nb_columns_G1 * p + (
                                                        nb_columns_G1 - 1) - m + val_start_row_1] + space_in_sections * (
                                                        n_columns_g - 1 - m)
                                            box_h_moved_g1.append(
                                                nb_columns_G1 * p + (nb_columns_G1 - 1) - m + val_start_row_1)

                                            if m == 0:
                                                result = [idx for idx, tup in enumerate(boxes_to_compare_g2) if
                                                          tup in {boxes_on_the_side_closest[p]}]

                                                boxes_to_compare_g2[result[0]] = (boxes[1]['x'][nb_columns_G1 * p + (
                                                        nb_columns_G1 - 1) - m + val_start_row_1],
                                                                                  boxes_to_compare_g2[result[0]][1],
                                                                                  boxes_to_compare_g2[result[0]][2],
                                                                                  boxes_to_compare_g2[result[0]][3])

                                                boxes_on_the_side_closest[p] = (boxes[1]['x'][nb_columns_G1 * p + (
                                                        nb_columns_G1 - 1) - m + val_start_row_1],
                                                                                boxes_on_the_side_closest[p][1],
                                                                                boxes_on_the_side_closest[p][2],
                                                                                boxes_on_the_side_closest[p][3])

                                    val_start_row_1 = val_start_row_1 + nb_columns_G1 * len(boxes_on_the_side_closest)
                                    set_list = set(boxes_on_the_side_closest)
                                    result = [idx for idx, tup in enumerate(boxes_to_compare_g2) if tup in set_list]
                                    for t in result:
                                        boxes_to_compare_g2[t] = (
                                            boxes_to_compare_g2[t][0], boxes_to_compare_g2[t][1],
                                            boxes_to_compare_g2[t][2],
                                            1)

                                elif boxes_on_the_side_closest[0][2] == 4 and b != nb_rows_G2 - 1:
                                    val_start_row_4 = val_start_row_4 if 'val_start_row_4' in locals() and val_start_row_4 > 0 else 0
                                    for q in range(len(boxes_on_the_side_closest)):
                                        for j in range(nb_columns_G4 - 1):
                                            boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                    nb_columns_G4 - 1) - q - nb_rows_G4 * j - val_start_row_4] = \
                                                boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                        nb_columns_G4 - 1) - q - nb_rows_G4 * j - val_start_row_4] + space_in_sections * (
                                                        nb_columns_G4 - 1 - j)
                                            box_h_moved_g4.append(nb_rows_G4 - 1 + nb_rows_G4 * (
                                                    nb_columns_G4 - 1) - q - nb_rows_G4 * j - val_start_row_4)
                                            if j == 0:
                                                result = [idx for idx, tup in enumerate(boxes_to_compare_g2) if
                                                          tup in {boxes_on_the_side_closest[q]}]
                                                boxes_to_compare_g2[result[0]] = (boxes[4]['x'][
                                                                                      nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                                              nb_columns_G4 - 1) - q - nb_rows_G4 * j - val_start_row_4],
                                                                                  boxes_to_compare_g2[result[0]][1],
                                                                                  boxes_to_compare_g2[result[0]][2],
                                                                                  boxes_to_compare_g2[result[0]][3])
                                                boxes_on_the_side_closest[q] = (boxes[4]['x'][
                                                                                    nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                                            nb_columns_G4 - 1) - q - nb_rows_G4 * j - val_start_row_4],
                                                                                boxes_on_the_side_closest[q][1],
                                                                                boxes_on_the_side_closest[q][2],
                                                                                boxes_on_the_side_closest[q][3])

                                    val_start_row_4 = val_start_row_4 + len(boxes_on_the_side_closest)
                                    set_list = set(boxes_on_the_side_closest)
                                    result = [idx for idx, tup in enumerate(boxes_to_compare_g2) if tup in set_list]
                                    for t in result:
                                        boxes_to_compare_g2[t] = (
                                            boxes_to_compare_g2[t][0], boxes_to_compare_g2[t][1],
                                            boxes_to_compare_g2[t][2],
                                            1)


                        else:

                            if nb_columns_G2 > 1:
                                space_in_sections = hole_distance / (nb_columns_G2 - 1 + 1)
                                for n in range(1, nb_columns_G2):
                                    boxes[2]['x'][(nb_columns_G2 * nb_rows_G2 - 1 - (
                                            nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * b - (n - 1)] = \
                                        boxes[2]['x'][(nb_columns_G2 * nb_rows_G2 - 1 - (
                                                nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * b - (
                                                              n - 1)] - space_in_sections * (nb_columns_G2 - n)
                                    box_h_moved_g2.append((nb_columns_G2 * nb_rows_G2 - 1 - (
                                            nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * b - (n - 1))

                                set_list = set(boxes_on_the_side_closest)
                                result = [idx for idx, tup in enumerate(boxes_to_compare_g2) if tup in set_list]
                                for t in result:
                                    boxes_to_compare_g2[t] = (
                                        boxes_to_compare_g2[t][0], boxes_to_compare_g2[t][1], boxes_to_compare_g2[t][2],
                                        1)
                            else:
                                space_in_sections = 0

            else:
                space_in_sections = length_von_level_G2 / (
                        nb_columns_G2 - 1) if nb_columns_G2 > 1 else length_von_level_G2
                for t in range(nb_rows_G2):
                    for n in range(1, nb_columns_G2):
                        boxes[2]['x'][
                            (nb_columns_G2 * nb_rows_G2 - 1 - (nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * t - (
                                    n - 1)] = boxes[2]['x'][(nb_columns_G2 * nb_rows_G2 - 1 - (
                                nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * t - (
                                                                    n - 1)] - space_in_sections * (
                                                      nb_columns_G2 - n)
                        box_h_moved_g2.append(
                            (nb_columns_G2 * nb_rows_G2 - 1 - (nb_rows_G2 - 1) * nb_columns_G2) + nb_columns_G2 * t - (
                                    n - 1))

        ############################################################################################################################################################################################################################################################################

        if li == 0 and len(boxes[1]['x']) != 0:
            nb_rows_G1 = nb_rows_G1 if 'nb_rows_G1' in locals() else len(set(boxes[1]['y']))
            nb_columns_G1 = nb_columns_G1 if 'nb_columns_G1' in locals() else len(set(boxes[1]['x']))
            length_von_level_G1 = length_von_level_G1 if 'length_von_level_G1' in locals() else max(boxes[1]['x'])
            if nb_columns_G1 > 1:
                if len(boxes[2]['x']) != 0:
                    nb_rows_G2 = nb_rows_G2 if 'nb_rows_G2' in locals() else len(set(boxes[2]['y']))
                    nb_columns_G2 = nb_columns_G2 if 'nb_columns_G2' in locals() else len(set(boxes[2]['x']))
                    length_von_level_G2 = length_von_level_G2 if 'length_von_level_G2' in locals() else min(
                        boxes[2]['x'])

                    if len(boxes[3]['x']) != 0:
                        nb_rows_G3 = nb_rows_G3 if 'nb_rows_G3' in locals() else len(set(boxes[3]['y']))
                        nb_columns_G3 = nb_columns_G3 if 'nb_columns_G3' in locals() else len(set(boxes[3]['x']))
                        length_von_level_G3 = length_von_level_G3 if 'length_von_level_G3' in locals() else min(
                            boxes[3]['x'])

                        boxes_to_compare_g1 = []
                        for q in range(nb_rows_G2):
                            boxes_to_compare_g1.append((boxes[2]['x'][
                                                            nb_columns_G2 * nb_rows_G2 - 1 - q * nb_columns_G2],
                                                        boxes[2]['y'][
                                                            nb_columns_G2 * nb_rows_G2 - 1 - q * nb_columns_G2], 2, 0))
                        for c in range(nb_rows_G3):
                            boxes_to_compare_g1.append((boxes[3]['x'][
                                                            nb_columns_G3 * (nb_rows_G3) - 1 - c * nb_columns_G3],
                                                        boxes[3]['y'][
                                                            nb_columns_G3 * (nb_rows_G3) - 1 - c * nb_columns_G3], 3,
                                                        0))
                    else:
                        boxes_to_compare_g1 = []
                        for q in range(nb_rows_G2):
                            boxes_to_compare_g1.append((boxes[2]['x'][
                                                            nb_columns_G2 * nb_rows_G2 - 1 - q * nb_columns_G2],
                                                        boxes[2]['y'][
                                                            nb_columns_G2 * nb_rows_G2 - 1 - q * nb_columns_G2], 2, 0))
                elif len(boxes[3]['x']) != 0:
                    nb_rows_G3 = nb_rows_G3 if 'nb_rows_G3' in locals() else len(set(boxes[3]['y']))
                    nb_columns_G3 = nb_columns_G3 if 'nb_columns_G3' in locals() else len(set(boxes[3]['x']))
                    length_von_level_G3 = length_von_level_G3 if 'length_von_level_G3' in locals() else min(
                        boxes[3]['x'])

                    boxes_to_compare_g1 = []
                    for c in range(nb_rows_G3):
                        boxes_to_compare_g1.append((boxes[3]['x'][nb_columns_G3 * (nb_rows_G3) - 1 - c * nb_columns_G3],
                                                    boxes[3]['y'][nb_columns_G3 * (nb_rows_G3) - 1 - c * nb_columns_G3],
                                                    3, 0))
                else:
                    boxes_to_compare_g1 = []

                ################
                if len(boxes[4]['y']) != 0:
                    boxes_from_g4_to_compare = []
                    for u in range(nb_rows_G1):
                        for p in range(nb_columns_G4):

                            if boxes[4]['y'][nb_rows_G4 - 1 + nb_rows_G4 * (nb_columns_G4 - 1) - p] < boxes[1]['y'][
                                nb_columns_G1 * u + (nb_columns_G1 - 1)] + width_val and boxes[4]['x'][
                                nb_rows_G4 - 1 + nb_rows_G4 * (nb_columns_G4 - 1) - p] > boxes[1]['x'][
                                nb_columns_G1 * u + (nb_columns_G1 - 1)] + length_val:
                                boxes_from_g4_to_compare.append((boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                        nb_columns_G4 - 1) - p], boxes[4]['y'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                        nb_columns_G4 - 1) - p], 4, 0))

                    if len(boxes_from_g4_to_compare) != 0:
                        boxes_from_g4_to_compare = list(set(boxes_from_g4_to_compare))
                        boxes_to_compare_g1 = boxes_to_compare_g1 + boxes_from_g4_to_compare
                ################################################

                if len(boxes_to_compare_g1) != 0:
                    rows_moved_G1 = int(len(box_h_moved_g1) / (nb_columns_G1 - 1)) if nb_columns_G1 > 1 else 0
                    if 'nb_columns_G2' in locals():
                        rows_moved_G2 = int(len(box_h_moved_g2) / (nb_columns_G2 - 1)) if nb_columns_G2 > 1 else 0
                    else:
                        rows_moved_G2 = 0
                    if 0 == 1:
                        pass

                    else:

                        if 'boxes_to_compare_g2' in locals():
                            for b in range(nb_rows_G1 - rows_moved_G1):
                                boxes_on_the_side_right = []
                                for c in range(len(boxes_to_compare_g1)):
                                    if boxes_to_compare_g1[c][2] == 2:
                                        list1 = [boxes[1]['y'][nb_columns_G1 * b + (
                                                nb_columns_G1 - 1) + rows_moved_G1 * nb_columns_G1],
                                                 boxes[1]['y'][nb_columns_G1 * b + (
                                                         nb_columns_G1 - 1) + rows_moved_G1 * nb_columns_G1] + width_val]
                                        list2 = [boxes_to_compare_g1[c][1], boxes_to_compare_g1[c][1] + length_val]
                                        if list1[1] > list2[0] and list2[1] > list1[0]:
                                            boxes_on_the_side_right.append(boxes_to_compare_g1[c])

                                    if boxes_to_compare_g1[c][2] == 3:
                                        list1 = [boxes[1]['y'][nb_columns_G1 * b + (
                                                nb_columns_G1 - 1) + rows_moved_G1 * nb_columns_G1],
                                                 boxes[1]['y'][nb_columns_G1 * b + (
                                                         nb_columns_G1 - 1) + rows_moved_G1 * nb_columns_G1] + width_val]
                                        list2 = [boxes_to_compare_g1[c][1], boxes_to_compare_g1[c][1] + width_val]
                                        if list1[1] > list2[0] and list2[1] > list1[0]:
                                            boxes_on_the_side_right.append(boxes_to_compare_g1[c])

                                    if boxes_to_compare_g1[c][2] == 4:
                                        list1 = [boxes[1]['y'][nb_columns_G1 * b + (
                                                nb_columns_G1 - 1) + rows_moved_G1 * nb_columns_G1],
                                                 boxes[1]['y'][nb_columns_G1 * b + (
                                                         nb_columns_G1 - 1) + rows_moved_G1 * nb_columns_G1] + width_val]
                                        list2 = [boxes_to_compare_g1[c][1], boxes_to_compare_g1[c][1] + length_val]
                                        if list1[1] > list2[0] and list2[1] > list1[0]:
                                            boxes_on_the_side_right.append(boxes_to_compare_g1[c])

                                if len(boxes_on_the_side_right) > 0:
                                    groups_length = [a[2] for a in boxes_on_the_side_right]
                                    if len(set(groups_length)) >= 2:
                                        val1_to_compare = None
                                        val2_to_compare = None
                                        val3_to_compare = None
                                        for tup in boxes_on_the_side_right:
                                            if tup[2] == 2:
                                                if val1_to_compare is None or tup[
                                                    0] > val1_to_compare: val1_to_compare = tup[0]
                                            if tup[2] == 4:
                                                if val2_to_compare is None or tup[
                                                    0] > val2_to_compare: val2_to_compare = tup[0]
                                            if tup[2] == 3:
                                                if val3_to_compare is None or tup[
                                                    0] > val3_to_compare: val3_to_compare = tup[0]
                                        LIST = [val1_to_compare, val2_to_compare, val3_to_compare]
                                        index = LIST.index(min([i for i in LIST if i is not None]))
                                        if index == 0:
                                            group_max_value = 2
                                        elif index == 1:
                                            group_max_value = 4
                                        elif index == 2:
                                            group_max_value = 3

                                    else:
                                        group_max_value = list(set(groups_length))[0]

                                    boxes_on_the_side_right_closest = [tup for tup in boxes_on_the_side_right if
                                                                       tup[2] == group_max_value]

                                    if boxes_on_the_side_right_closest[0][2] == 2:
                                        space_hole = boxes_on_the_side_right_closest[0][0] - (
                                                length_von_level_G1 + length_val)
                                        space_in_sections = space_hole / (nb_columns_G1 - 1 + 1)

                                        val_start_row_1 = val_start_row_1 if 'val_start_row_1' in locals() and val_start_row_1 > 0 else 0

                                        for j in range(nb_columns_G1 - 1):
                                            if j == 0:
                                                result = [idx for idx, tup in enumerate(boxes_to_compare_g2) if tup in {
                                                    (boxes[1]['x'][
                                                         nb_columns_G1 * 0 + (nb_columns_G1 - 1) - j + val_start_row_1],
                                                     boxes[1]['y'][
                                                         nb_columns_G1 * 0 + (nb_columns_G1 - 1) - j + val_start_row_1],
                                                     1, 0)}]

                                                boxes[1]['x'][
                                                    nb_columns_G1 * 0 + (nb_columns_G1 - 1) - j + val_start_row_1] = \
                                                    boxes[1]['x'][nb_columns_G1 * 0 + (
                                                            nb_columns_G1 - 1) - j + val_start_row_1] + space_in_sections * (
                                                            nb_columns_G1 - (j + 1))
                                                box_h_moved_g1.append(
                                                    nb_columns_G1 * 0 + (nb_columns_G1 - 1) - j + val_start_row_1)

                                                boxes_to_compare_g2[result[0]] = (boxes[1]['x'][nb_columns_G1 * 0 + (
                                                        nb_columns_G1 - 1) - j + val_start_row_1],
                                                                                  boxes_to_compare_g2[result[0]][1],
                                                                                  boxes_to_compare_g2[result[0]][2],
                                                                                  1)

                                            else:
                                                boxes[1]['x'][
                                                    nb_columns_G1 * 0 + (nb_columns_G1 - 1) - j + val_start_row_1] = \
                                                    boxes[1]['x'][nb_columns_G1 * 0 + (
                                                            nb_columns_G1 - 1) - j + val_start_row_1] + space_in_sections * (
                                                            nb_columns_G1 - (j + 1))
                                                box_h_moved_g1.append(
                                                    nb_columns_G1 * 0 + (nb_columns_G1 - 1) - j + val_start_row_1)

                                        val_start_row_1 = val_start_row_1 + nb_columns_G1


                                    elif boxes_on_the_side_right_closest[0][2] == 3:
                                        space_hole = boxes_on_the_side_right_closest[0][0] - (
                                                length_von_level_G1 + length_val)
                                        if nb_columns_G3 == 1:
                                            space_in_sections = space_hole / (nb_columns_G1 - 1 + 1)
                                            val_start_row_1 = val_start_row_1 if 'val_start_row_1' in locals() and val_start_row_1 > 0 else 0

                                            for m in range(nb_columns_G1 - 1):
                                                if m == 0:
                                                    result = [idx for idx, tup in enumerate(boxes_to_compare_g2) if
                                                              tup in {(boxes[1]['x'][nb_columns_G1 * 0 + (
                                                                      nb_columns_G1 - 1) - m + val_start_row_1],
                                                                       boxes[1]['y'][nb_columns_G1 * 0 + (
                                                                               nb_columns_G1 - 1) - m + val_start_row_1],
                                                                       1, 0)}]
                                                    boxes[1]['x'][
                                                        nb_columns_G1 * 0 + (nb_columns_G1 - 1) - m + val_start_row_1] = \
                                                        boxes[1]['x'][nb_columns_G1 * 0 + (
                                                                nb_columns_G1 - 1) - m + val_start_row_1] + space_in_sections * (
                                                                nb_columns_G1 - (m + 1))
                                                    box_h_moved_g1.append(
                                                        nb_columns_G1 * 0 + (nb_columns_G1 - 1) - m + val_start_row_1)

                                                    boxes_to_compare_g2[result[0]] = (boxes[1]['x'][
                                                                                          nb_columns_G1 * 0 + (
                                                                                                  nb_columns_G1 - 1) - m + val_start_row_1],
                                                                                      boxes_to_compare_g2[result[0]][1],
                                                                                      boxes_to_compare_g2[result[0]][2],
                                                                                      1)

                                                else:
                                                    boxes[1]['x'][
                                                        nb_columns_G1 * 0 + (nb_columns_G1 - 1) - m + val_start_row_1] = \
                                                        boxes[1]['x'][nb_columns_G1 * 0 + (
                                                                nb_columns_G1 - 1) - m + val_start_row_1] + space_in_sections * (
                                                                nb_columns_G1 - (m + 1))
                                                    box_h_moved_g1.append(
                                                        nb_columns_G1 * 0 + (nb_columns_G1 - 1) - m + val_start_row_1)

                                            val_start_row_1 = val_start_row_1 + nb_columns_G1

                                        elif nb_columns_G3 > 1:
                                            space_in_sections = space_hole / (nb_columns_G3 - 1 + nb_columns_G1 - 1 + 1)
                                            if b != nb_rows_G1 - rows_moved_G1 - 1:
                                                val_start_row_3 = val_start_row_3 if 'val_start_row_3' in locals() and val_start_row_3 > 0 else 0
                                                for n in range(nb_columns_G3 - 1):
                                                    boxes[3]['x'][
                                                        nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - val_start_row_3] = \
                                                        boxes[3]['x'][
                                                            nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - val_start_row_3] - space_in_sections * (
                                                                nb_columns_G3 - 1 - n)
                                                    box_h_moved_g3.append(
                                                        nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - val_start_row_3)
                                                val_start_row_3 = val_start_row_3 + nb_columns_G3
                                            else:
                                                if len(boxes[4]['x']) != 0:
                                                    for item in boxes_on_the_side_right_closest:

                                                        if item[1] + width_val <= boxes[4]['y'][
                                                            nb_rows_G4 - 1 + nb_rows_G4 * (nb_columns_G4 - 1) - 0] or \
                                                                boxes[1]['x'][nb_columns_G1 * 0 + (
                                                                        nb_columns_G1 - 1) + nb_columns_G1 * (
                                                                                      nb_rows_G1 - 1)] + length_val > \
                                                                boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                        nb_columns_G4 - 1) - 0] + width_val:

                                                            val_start_row_3 = val_start_row_3 if 'val_start_row_3' in locals() and val_start_row_3 > 0 else 0
                                                            for n in range(nb_columns_G3 - 1):
                                                                boxes[3]['x'][
                                                                    nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - val_start_row_3] = \
                                                                    boxes[3]['x'][
                                                                        nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - val_start_row_3] - space_in_sections * (
                                                                            nb_columns_G3 - 1 - n)
                                                                box_h_moved_g3.append(
                                                                    nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - val_start_row_3)
                                                            val_start_row_3 = val_start_row_3 + nb_columns_G3

                                            val_start_row_1 = val_start_row_1 if 'val_start_row_1' in locals() and val_start_row_1 > 0 else 0
                                            for m in range(nb_columns_G1 - 1):
                                                if m == 0:
                                                    result = [idx for idx, tup in enumerate(boxes_to_compare_g2) if
                                                              tup in {(boxes[1]['x'][nb_columns_G1 * 0 + (
                                                                      nb_columns_G1 - 1) - m + val_start_row_1],
                                                                       boxes[1]['y'][nb_columns_G1 * 0 + (
                                                                               nb_columns_G1 - 1) - m + val_start_row_1],
                                                                       1, 0)}]
                                                    boxes[1]['x'][
                                                        nb_columns_G1 * 0 + (nb_columns_G1 - 1) - m + val_start_row_1] = \
                                                        boxes[1]['x'][nb_columns_G1 * 0 + (
                                                                nb_columns_G1 - 1) - m + val_start_row_1] + space_in_sections * (
                                                                nb_columns_G1 - (m + 1))
                                                    box_h_moved_g1.append(
                                                        nb_columns_G1 * 0 + (nb_columns_G1 - 1) - m + val_start_row_1)

                                                    boxes_to_compare_g2[result[0]] = (boxes[1]['x'][
                                                                                          nb_columns_G1 * 0 + (
                                                                                                  nb_columns_G1 - 1) - m + val_start_row_1],
                                                                                      boxes_to_compare_g2[result[0]][1],
                                                                                      boxes_to_compare_g2[result[0]][2],
                                                                                      1)

                                                else:
                                                    boxes[1]['x'][
                                                        nb_columns_G1 * 0 + (nb_columns_G1 - 1) - m + val_start_row_1] = \
                                                        boxes[1]['x'][nb_columns_G1 * 0 + (
                                                                nb_columns_G1 - 1) - m + val_start_row_1] + space_in_sections * (
                                                                nb_columns_G1 - (m + 1))
                                                    box_h_moved_g1.append(
                                                        nb_columns_G1 * 0 + (nb_columns_G1 - 1) - m + val_start_row_1)

                                            val_start_row_1 = val_start_row_1 + nb_columns_G1

                                    elif boxes_on_the_side_right_closest[0][2] == 4:
                                        space_hole = boxes_on_the_side_right_closest[0][0] - (
                                                length_von_level_G1 + length_val)
                                        space_in_sections = space_hole / (nb_columns_G1 - 1 + 1)
                                        val_start_row_1 = val_start_row_1 if 'val_start_row_1' in locals() and val_start_row_1 > 0 else 0

                                        for m in range(nb_columns_G1 - 1):
                                            if m == 0:
                                                result = [idx for idx, tup in enumerate(boxes_to_compare_g2) if tup in {
                                                    (boxes[1]['x'][
                                                         nb_columns_G1 * 0 + (nb_columns_G1 - 1) - m + val_start_row_1],
                                                     boxes[1]['y'][
                                                         nb_columns_G1 * 0 + (nb_columns_G1 - 1) - m + val_start_row_1],
                                                     1, 0)}]
                                                boxes[1]['x'][
                                                    nb_columns_G1 * 0 + (nb_columns_G1 - 1) - m + val_start_row_1] = \
                                                    boxes[1]['x'][nb_columns_G1 * 0 + (
                                                            nb_columns_G1 - 1) - m + val_start_row_1] + space_in_sections * (
                                                            nb_columns_G1 - (m + 1))
                                                box_h_moved_g1.append(
                                                    nb_columns_G1 * 0 + (nb_columns_G1 - 1) - m + val_start_row_1)

                                                boxes_to_compare_g2[result[0]] = (boxes[1]['x'][nb_columns_G1 * 0 + (
                                                        nb_columns_G1 - 1) - m + val_start_row_1],
                                                                                  boxes_to_compare_g2[result[0]][1],
                                                                                  boxes_to_compare_g2[result[0]][2],
                                                                                  1)

                                            else:
                                                boxes[1]['x'][
                                                    nb_columns_G1 * 0 + (nb_columns_G1 - 1) - m + val_start_row_1] = \
                                                    boxes[1]['x'][nb_columns_G1 * 0 + (
                                                            nb_columns_G1 - 1) - m + val_start_row_1] + space_in_sections * (
                                                            nb_columns_G1 - (m + 1))
                                                box_h_moved_g1.append(
                                                    nb_columns_G1 * 0 + (nb_columns_G1 - 1) - m + val_start_row_1)

                                        val_start_row_1 = val_start_row_1 + nb_columns_G1


                                elif len(boxes_on_the_side_right) == 0 and len(boxes[2]['x']) == 0:
                                    space_in_sections = (pallet_length - (length_von_level_G1 + length_val)) / (
                                            nb_columns_G1 - 1) if nb_columns_G1 > 1 else length_von_level_G1
                                    rows_moved_G1 = int(
                                        len(box_h_moved_g1) / (nb_columns_G1 - 1)) if nb_rows_G1 > 1 else len(
                                        box_h_moved_g1)
                                    val_start_row_1 = val_start_row_1 if 'val_start_row_1' in locals() and val_start_row_1 > 0 else 0
                                    for b in range(nb_rows_G1 - rows_moved_G1):
                                        for n in range(1, nb_columns_G1):
                                            boxes[1]['x'][(nb_columns_G1 - 1) - (n - 1) + val_start_row_1] = \
                                                boxes[1]['x'][
                                                    (nb_columns_G1 - 1) - (
                                                                n - 1) + val_start_row_1] + space_in_sections * (
                                                        nb_columns_G1 - n)
                                            box_h_moved_g1.append((nb_columns_G1 - 1) - (n - 1) + val_start_row_1)
                                        val_start_row_1 = val_start_row_1 + nb_columns_G1
                                else:
                                    if b == nb_rows_G1 - rows_moved_G1 - 1:
                                        space_in_sections = (pallet_length - (length_von_level_G1 + length_val)) / (
                                                nb_columns_G1 - 1) if nb_columns_G1 > 1 else length_von_level_G1
                                        rows_moved_G1 = int(
                                            len(box_h_moved_g1) / (nb_columns_G1 - 1)) if nb_columns_G1 > 1 else len(
                                            box_h_moved_g1)
                                        for b in range(nb_rows_G1 - rows_moved_G1):
                                            for n in range(1, nb_columns_G1):
                                                boxes[1]['x'][nb_columns_G1 * b + (nb_columns_G1 - 1) - (
                                                        n - 1) + rows_moved_G1 * nb_columns_G1] = boxes[1]['x'][
                                                                                                      nb_columns_G1 * b + (
                                                                                                              nb_columns_G1 - 1) - (
                                                                                                              n - 1) + rows_moved_G1 * nb_columns_G1] + space_in_sections * (
                                                                                                          nb_columns_G1 - n)
                                                box_h_moved_g1.append(nb_columns_G1 * b + (nb_columns_G1 - 1) - (
                                                        n - 1) + rows_moved_G1 * nb_columns_G1)



                        else:
                            no_g2_box_moved_g1 = []
                            for b in range(nb_rows_G1 - rows_moved_G1):
                                boxes_on_the_side_right = []
                                for c in range(len(boxes_to_compare_g1)):
                                    if boxes_to_compare_g1[c][2] == 3:
                                        list1 = [boxes[1]['y'][nb_columns_G1 * b + (
                                                nb_columns_G1 - 1) + rows_moved_G1 * nb_columns_G1],
                                                 boxes[1]['y'][nb_columns_G1 * b + (
                                                         nb_columns_G1 - 1) + rows_moved_G1 * nb_columns_G1] + width_val]
                                        list2 = [boxes_to_compare_g1[c][1], boxes_to_compare_g1[c][1] + width_val]
                                        if list1[1] > list2[0] and list2[1] > list1[0]:
                                            boxes_on_the_side_right.append(boxes_to_compare_g1[c])

                                    if boxes_to_compare_g1[c][2] == 4:
                                        list1 = [boxes[1]['y'][nb_columns_G1 * b + (
                                                nb_columns_G1 - 1) + rows_moved_G1 * nb_columns_G1],
                                                 boxes[1]['y'][nb_columns_G1 * b + (
                                                         nb_columns_G1 - 1) + rows_moved_G1 * nb_columns_G1] + width_val]
                                        list2 = [boxes_to_compare_g1[c][1], boxes_to_compare_g1[c][1] + length_val]
                                        if list1[1] > list2[0] and list2[1] > list1[0]:
                                            boxes_on_the_side_right.append(boxes_to_compare_g1[c])

                                if len(boxes_on_the_side_right) > 0:
                                    groups_length = [a[2] for a in boxes_on_the_side_right]
                                    if len(set(groups_length)) >= 2:
                                        val1_to_compare = None
                                        val2_to_compare = None
                                        val3_to_compare = None
                                        for tup in boxes_on_the_side_right:
                                            if tup[2] == 2:
                                                if val1_to_compare is None or tup[
                                                    0] > val1_to_compare: val1_to_compare = tup[0]
                                            if tup[2] == 4:
                                                if val2_to_compare is None or tup[
                                                    0] > val2_to_compare: val2_to_compare = tup[0]
                                            if tup[2] == 3:
                                                if val3_to_compare is None or tup[
                                                    0] > val3_to_compare: val3_to_compare = tup[0]
                                        LIST = [val1_to_compare, val2_to_compare, val3_to_compare]
                                        index = LIST.index(min([i for i in LIST if i is not None]))
                                        if index == 0:
                                            group_max_value = 2
                                        elif index == 1:
                                            group_max_value = 4
                                        elif index == 2:
                                            group_max_value = 3

                                    else:
                                        group_max_value = list(set(groups_length))[0]

                                    boxes_on_the_side_right_closest = [tup for tup in boxes_on_the_side_right if
                                                                       tup[2] == group_max_value]

                                    if boxes_on_the_side_right_closest[0][2] == 3:
                                        space_hole = boxes_on_the_side_right_closest[0][0] - (
                                                length_von_level_G1 + length_val)
                                        if nb_columns_G3 == 1:
                                            space_in_sections = space_hole / (nb_columns_G1 - 1 + 1)
                                            val_start_row_1 = val_start_row_1 if 'val_start_row_1' in locals() and val_start_row_1 > 0 else 0
                                            for m in range(nb_columns_G1 - 1):
                                                boxes[1]['x'][
                                                    nb_columns_G1 * 0 + (nb_columns_G1 - 1) - m + val_start_row_1] = \
                                                    boxes[1]['x'][nb_columns_G1 * 0 + (
                                                            nb_columns_G1 - 1) - m + val_start_row_1] + space_in_sections * (
                                                            nb_columns_G1 - (m + 1))
                                                box_h_moved_g1.append(
                                                    nb_columns_G1 * 0 + (nb_columns_G1 - 1) - m + val_start_row_1)
                                                if m == 0:
                                                    no_g2_box_moved_g1.append((boxes[1]['x'][nb_columns_G1 * 0 + (
                                                            nb_columns_G1 - 1) - m + val_start_row_1],
                                                                               boxes[1]['y'][nb_columns_G1 * 0 + (
                                                                                       nb_columns_G1 - 1) - m + val_start_row_1],
                                                                               1, 1))
                                            val_start_row_1 = val_start_row_1 + nb_columns_G1

                                        elif nb_columns_G3 > 1:
                                            space_in_sections = space_hole / (nb_columns_G3 - 1 + nb_columns_G1 - 1 + 1)
                                            if b != nb_rows_G1 - rows_moved_G1 - 1:
                                                val_start_row_3 = val_start_row_3 if 'val_start_row_3' in locals() and val_start_row_3 > 0 else 0
                                                for n in range(nb_columns_G3 - 1):
                                                    boxes[3]['x'][
                                                        nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - val_start_row_3] = \
                                                        boxes[3]['x'][
                                                            nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - val_start_row_3] - space_in_sections * (
                                                                nb_columns_G3 - 1 - n)
                                                    box_h_moved_g3.append(
                                                        nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - val_start_row_3)
                                                val_start_row_3 = val_start_row_3 + nb_columns_G3
                                            else:
                                                if len(boxes[4]['x']) != 0:
                                                    for item in boxes_on_the_side_right_closest:
                                                        if item[1] + width_val <= boxes[4]['y'][
                                                            nb_rows_G4 - 1 + nb_rows_G4 * (nb_columns_G4 - 1) - 0] or \
                                                                boxes[1]['x'][nb_columns_G1 * 0 + (
                                                                        nb_columns_G1 - 1) + nb_columns_G1 * (
                                                                                      nb_rows_G1 - 1)] + length_val > \
                                                                boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                        nb_columns_G4 - 1) - 0] + width_val:

                                                            val_start_row_3 = val_start_row_3 if 'val_start_row_3' in locals() and val_start_row_3 > 0 else 0
                                                            for n in range(nb_columns_G3 - 1):
                                                                boxes[3]['x'][
                                                                    nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - val_start_row_3] = \
                                                                    boxes[3]['x'][
                                                                        nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - val_start_row_3] - space_in_sections * (
                                                                            nb_columns_G3 - 1 - n)
                                                                box_h_moved_g3.append(
                                                                    nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - val_start_row_3)
                                                            val_start_row_3 = val_start_row_3 + nb_columns_G3

                                            val_start_row_1 = val_start_row_1 if 'val_start_row_1' in locals() and val_start_row_1 > 0 else 0
                                            for m in range(nb_columns_G1 - 1):
                                                boxes[1]['x'][
                                                    nb_columns_G1 * 0 + (nb_columns_G1 - 1) - m + val_start_row_1] = \
                                                    boxes[1]['x'][nb_columns_G1 * 0 + (
                                                            nb_columns_G1 - 1) - m + val_start_row_1] + space_in_sections * (
                                                            nb_columns_G1 - (m + 1))
                                                box_h_moved_g1.append(
                                                    nb_columns_G1 * 0 + (nb_columns_G1 - 1) - m + val_start_row_1)
                                                if m == 0:
                                                    no_g2_box_moved_g1.append((boxes[1]['x'][nb_columns_G1 * 0 + (
                                                            nb_columns_G1 - 1) - m + val_start_row_1],
                                                                               boxes[1]['y'][nb_columns_G1 * 0 + (
                                                                                       nb_columns_G1 - 1) - m + val_start_row_1],
                                                                               1, 1))

                                            val_start_row_1 = val_start_row_1 + nb_columns_G1

                                    elif boxes_on_the_side_right_closest[0][2] == 4:
                                        space_hole = boxes_on_the_side_right_closest[0][0] - (
                                                length_von_level_G1 + length_val)
                                        space_in_sections = space_hole / (nb_columns_G1 - 1 + 1)
                                        val_start_row_1 = val_start_row_1 if 'val_start_row_1' in locals() and val_start_row_1 > 0 else 0

                                        for m in range(nb_columns_G1 - 1):
                                            boxes[1]['x'][
                                                nb_columns_G1 * 0 + (nb_columns_G1 - 1) - m + val_start_row_1] = \
                                                boxes[1]['x'][nb_columns_G1 * 0 + (
                                                        nb_columns_G1 - 1) - m + val_start_row_1] + space_in_sections * (
                                                        nb_columns_G1 - (m + 1))
                                            box_h_moved_g1.append(
                                                nb_columns_G1 * 0 + (nb_columns_G1 - 1) - m + val_start_row_1)

                                        val_start_row_1 = val_start_row_1 + nb_columns_G1

                                else:
                                    space_in_sections = (pallet_length - (length_von_level_G1 + length_val)) / (
                                            nb_columns_G1 - 1) if nb_columns_G1 > 1 else length_von_level_G1
                                    rows_moved_G1 = int(
                                        len(box_h_moved_g1) / (nb_columns_G1 - 1)) if nb_columns_G1 > 1 else len(
                                        box_h_moved_g1)

                                    for b in range(nb_rows_G1 - rows_moved_G1):
                                        for n in range(1, nb_columns_G1):
                                            boxes[1]['x'][nb_columns_G1 * b + (nb_columns_G1 - 1) - (
                                                    n - 1) + rows_moved_G1 * nb_columns_G1] = boxes[1]['x'][
                                                                                                  nb_columns_G1 * b + (
                                                                                                          nb_columns_G1 - 1) - (
                                                                                                          n - 1) + rows_moved_G1 * nb_columns_G1] + space_in_sections * (
                                                                                                      nb_columns_G1 - n)
                                            box_h_moved_g1.append(nb_columns_G1 * b + (nb_columns_G1 - 1) - (
                                                    n - 1) + rows_moved_G1 * nb_columns_G1)
                                            if n == 0:
                                                no_g2_box_moved_g1.append((boxes[1]['x'][nb_columns_G1 * b + (
                                                        nb_columns_G1 - 1) - (
                                                                                                 n - 1) + rows_moved_G1 * nb_columns_G1],
                                                                           boxes[1]['y'][nb_columns_G1 * b + (
                                                                                   nb_columns_G1 - 1) - (
                                                                                                 n - 1) + rows_moved_G1 * nb_columns_G1],
                                                                           1, 1))
                                    break


                else:
                    space_in_sections = (pallet_length - (length_von_level_G1 + length_val)) / (
                            nb_columns_G1 - 1) if nb_columns_G1 > 1 else length_von_level_G1
                    rows_moved_G1 = int(len(box_h_moved_g1) / (nb_columns_G1 - 1)) if nb_columns_G1 > 1 else len(
                        box_h_moved_g1)
                    for b in range(nb_rows_G1 - rows_moved_G1):
                        for n in range(1, nb_columns_G1):
                            boxes[1]['x'][
                                nb_columns_G1 * b + (nb_columns_G1 - 1) - (n - 1) + rows_moved_G1 * nb_columns_G1] = \
                                boxes[1]['x'][nb_columns_G1 * b + (nb_columns_G1 - 1) - (
                                        n - 1) + rows_moved_G1 * nb_columns_G1] + space_in_sections * (
                                        nb_columns_G1 - n)
                            box_h_moved_g1.append(
                                nb_columns_G1 * b + (nb_columns_G1 - 1) - (n - 1) + rows_moved_G1 * nb_columns_G1)

        ########################################################################################################################

        if li == 0 and len(boxes[4]['x']) != 0:
            nb_rows_G4 = nb_rows_G4 if 'nb_rows_G4' in locals() else len(set(boxes[4]['y']))
            nb_columns_G4 = nb_columns_G4 if 'nb_columns_G4' in locals() else len(set(boxes[4]['x']))
            length_von_level_G4 = length_von_level_G4 if 'length_von_level_G4' in locals() else max(boxes[4]['x'])
            if nb_columns_G4 > 1:
                if len(boxes[2]['x']) != 0:
                    nb_rows_G2 = nb_rows_G2 if 'nb_rows_G2' in locals() else len(set(boxes[2]['y']))
                    nb_columns_G2 = nb_columns_G2 if 'nb_columns_G2' in locals() else len(set(boxes[2]['x']))
                    length_von_level_G2 = length_von_level_G2 if 'length_von_level_G2' in locals() else min(
                        boxes[2]['x'])

                    if len(boxes[3]['x']) != 0:
                        nb_rows_G3 = nb_rows_G3 if 'nb_rows_G3' in locals() else len(set(boxes[3]['y']))
                        nb_columns_G3 = nb_columns_G3 if 'nb_columns_G3' in locals() else len(set(boxes[3]['x']))
                        length_von_level_G3 = length_von_level_G3 if 'length_von_level_G3' in locals() else min(
                            boxes[3]['x'])

                        boxes_to_compare_g4 = []
                        for q in range(nb_rows_G2):
                            boxes_to_compare_g4.append((boxes[2]['x'][
                                                            nb_columns_G2 * nb_rows_G2 - 1 - q * nb_columns_G2],
                                                        boxes[2]['y'][
                                                            nb_columns_G2 * nb_rows_G2 - 1 - q * nb_columns_G2], 2, 0))
                        for c in range(nb_rows_G3):
                            boxes_to_compare_g4.append((boxes[3]['x'][
                                                            nb_columns_G3 * (nb_rows_G3) - 1 - c * nb_columns_G3],
                                                        boxes[3]['y'][
                                                            nb_columns_G3 * (nb_rows_G3) - 1 - c * nb_columns_G3], 3,
                                                        0))
                    else:
                        boxes_to_compare_g4 = []
                        for q in range(nb_rows_G2):
                            boxes_to_compare_g4.append((boxes[2]['x'][
                                                            nb_columns_G2 * nb_rows_G2 - 1 - q * nb_columns_G2],
                                                        boxes[2]['y'][
                                                            nb_columns_G2 * nb_rows_G2 - 1 - q * nb_columns_G2], 2, 0))
                elif len(boxes[3]['x']) != 0:
                    nb_rows_G3 = nb_rows_G3 if 'nb_rows_G3' in locals() else len(set(boxes[3]['y']))
                    nb_columns_G3 = nb_columns_G3 if 'nb_columns_G3' in locals() else len(set(boxes[3]['x']))
                    length_von_level_G3 = length_von_level_G3 if 'length_von_level_G3' in locals() else min(
                        boxes[3]['x'])

                    boxes_to_compare_g4 = []
                    for c in range(nb_rows_G3):
                        boxes_to_compare_g4.append((boxes[3]['x'][nb_columns_G3 * (nb_rows_G3) - 1 - c * nb_columns_G3],
                                                    boxes[3]['y'][nb_columns_G3 * (nb_rows_G3) - 1 - c * nb_columns_G3],
                                                    3, 0))
                else:
                    boxes_to_compare_g4 = []

                ################
                if len(boxes[1]['y']) != 0:
                    boxes_from_g1_to_compare = []
                    for u in range(nb_rows_G4):
                        for p in range(nb_columns_G1):
                            if boxes[1]['y'][nb_columns_G1 * (nb_rows_G1 - 1) + (nb_columns_G1 - 1) - p] + width_val > \
                                    boxes[4]['y'][nb_rows_G4 - 1 + nb_rows_G4 * (nb_columns_G4 - 1) - u] and \
                                    boxes[1]['x'][nb_columns_G1 * (nb_rows_G1 - 1) + (nb_columns_G1 - 1) - p] > \
                                    boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (nb_columns_G4 - 1) - u] + width_val:
                                boxes_from_g1_to_compare.append((boxes[1]['x'][nb_columns_G1 * (nb_rows_G1 - 1) + (
                                        nb_columns_G1 - 1) - p], boxes[1]['y'][nb_columns_G1 * (nb_rows_G1 - 1) + (
                                        nb_columns_G1 - 1) - p], 1, 0))

                    if len(boxes_from_g1_to_compare) != 0:
                        boxes_from_g1_to_compare = list(set(boxes_from_g1_to_compare))
                        boxes_to_compare_g4 = boxes_to_compare_g4 + boxes_from_g1_to_compare
                ################################################

                if len(boxes_to_compare_g4) != 0:
                    rows_moved_G4 = int(len(box_h_moved_g4) / (nb_columns_G4 - 1)) if nb_columns_G4 > 1 else 0
                    if 'nb_columns_G3' in locals():
                        rows_moved_G3 = int(len(box_h_moved_g3) / (nb_columns_G3 - 1)) if nb_columns_G3 > 1 else 0
                    else:
                        rows_moved_G3 = 0
                    if 0 == 1:
                        pass

                    else:
                        if 'boxes_to_compare_g2' in locals():
                            for b in range(nb_rows_G4 - rows_moved_G4):
                                boxes_on_the_side_right = []
                                for c in range(len(boxes_to_compare_g4)):
                                    if boxes_to_compare_g4[c][2] == 2:
                                        list1 = [boxes[4]['y'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                nb_columns_G4 - 1) - b - rows_moved_G4],
                                                 boxes[4]['y'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                         nb_columns_G4 - 1) - b - rows_moved_G4] + length_val]
                                        list2 = [boxes_to_compare_g4[c][1], boxes_to_compare_g4[c][1] + length_val]
                                        if list1[1] > list2[0] and list2[1] > list1[0]:
                                            boxes_on_the_side_right.append(boxes_to_compare_g4[c])

                                    if boxes_to_compare_g4[c][2] == 3:
                                        list1 = [boxes[4]['y'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                nb_columns_G4 - 1) - b - rows_moved_G4],
                                                 boxes[4]['y'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                         nb_columns_G4 - 1) - b - rows_moved_G4] + length_val]
                                        list2 = [boxes_to_compare_g4[c][1], boxes_to_compare_g4[c][1] + width_val]
                                        if list1[1] > list2[0] and list2[1] > list1[0]:
                                            boxes_on_the_side_right.append(boxes_to_compare_g4[c])

                                    if boxes_to_compare_g4[c][2] == 1:
                                        list1 = [boxes[4]['y'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                nb_columns_G4 - 1) - b - rows_moved_G4],
                                                 boxes[4]['y'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                         nb_columns_G4 - 1) - b - rows_moved_G4] + length_val]
                                        list2 = [boxes_to_compare_g4[c][1], boxes_to_compare_g4[c][1] + width_val]
                                        if list1[1] > list2[0] and list2[1] > list1[0]:
                                            boxes_on_the_side_right.append(boxes_to_compare_g4[c])

                                if len(boxes_on_the_side_right) > 0:
                                    groups_length = [a[2] for a in boxes_on_the_side_right]
                                    if len(set(groups_length)) >= 2:
                                        val1_to_compare = None
                                        val2_to_compare = None
                                        val3_to_compare = None
                                        for tup in boxes_on_the_side_right:
                                            if tup[2] == 2:
                                                if val1_to_compare is None or tup[
                                                    0] > val1_to_compare: val1_to_compare = tup[0]
                                            if tup[2] == 3:
                                                if val2_to_compare is None or tup[
                                                    0] > val2_to_compare: val2_to_compare = tup[0]
                                            if tup[2] == 1:
                                                if val3_to_compare is None or tup[
                                                    0] > val3_to_compare: val3_to_compare = tup[0]
                                        LIST = [val1_to_compare, val2_to_compare, val3_to_compare]
                                        index = LIST.index(min([i for i in LIST if i is not None]))
                                        if index == 0:
                                            group_max_value = 2
                                        elif index == 1:
                                            group_max_value = 3
                                        elif index == 2:
                                            group_max_value = 1
                                    else:
                                        group_max_value = list(set(groups_length))[0]

                                    boxes_on_the_side_right_closest = [tup for tup in boxes_on_the_side_right if
                                                                       tup[2] == group_max_value]

                                    if boxes_on_the_side_right_closest[0][2] == 2:
                                        space_hole = boxes_on_the_side_right_closest[0][0] - (
                                                length_von_level_G4 + width_val)
                                        space_in_sections = space_hole / (nb_columns_G4 - 1 + 1)
                                        val_start_row_4 = val_start_row_4 if 'val_start_row_4' in locals() and val_start_row_4 > 0 else 0
                                        for j in range(nb_columns_G4 - 1):
                                            if j == 0:
                                                result = [idx for idx, tup in enumerate(boxes_to_compare_g2) if tup in {
                                                    (boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                            nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4],
                                                     boxes[4]['y'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                             nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4],
                                                     4, 0)}]
                                                boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                        nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4] = \
                                                    boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                            nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4] + space_in_sections * (
                                                            nb_columns_G4 - (j + 1))
                                                box_h_moved_g4.append(nb_rows_G4 - 1 + nb_rows_G4 * (
                                                        nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4)

                                                boxes_to_compare_g2[result[0]] = (boxes[4]['x'][
                                                                                      nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                                              nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4],
                                                                                  boxes_to_compare_g2[result[0]][1],
                                                                                  boxes_to_compare_g2[result[0]][2],
                                                                                  1)

                                            else:
                                                boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                        nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4] = \
                                                    boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                            nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4] + space_in_sections * (
                                                            nb_columns_G4 - (j + 1))
                                                box_h_moved_g4.append(nb_rows_G4 - 1 + nb_rows_G4 * (
                                                        nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4)

                                        val_start_row_4 = val_start_row_4 + 1


                                    elif boxes_on_the_side_right_closest[0][2] == 3:
                                        space_hole = boxes_on_the_side_right_closest[0][0] - (
                                                length_von_level_G4 + width_val)
                                        if nb_columns_G3 == 1:
                                            space_in_sections = space_hole / (nb_columns_G4 - 1 + 1)
                                            val_start_row_4 = val_start_row_4 if 'val_start_row_4' in locals() and val_start_row_4 > 0 else 0
                                            for j in range(nb_columns_G4 - 1):
                                                if j == 0:
                                                    result = [idx for idx, tup in enumerate(boxes_to_compare_g2) if
                                                              tup in {(boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                      nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4],
                                                                       boxes[4]['y'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                               nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4],
                                                                       4, 0)}]
                                                    boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                            nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4] = \
                                                        boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4] + space_in_sections * (
                                                                nb_columns_G4 - (j + 1))
                                                    box_h_moved_g4.append(nb_rows_G4 - 1 + nb_rows_G4 * (
                                                            nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4)

                                                    boxes_to_compare_g2[result[0]] = (boxes[4]['x'][
                                                                                          nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                                                  nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4],
                                                                                      boxes_to_compare_g2[result[0]][1],
                                                                                      boxes_to_compare_g2[result[0]][2],
                                                                                      1)

                                                else:
                                                    boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                            nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4] = \
                                                        boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4] + space_in_sections * (
                                                                nb_columns_G4 - (j + 1))
                                                    box_h_moved_g4.append(nb_rows_G4 - 1 + nb_rows_G4 * (
                                                            nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4)

                                            val_start_row_4 = val_start_row_4 + 1

                                        elif nb_columns_G3 > 1:
                                            space_in_sections = space_hole / (nb_columns_G3 - 1 + nb_columns_G4 - 1 + 1)
                                            if b != nb_rows_G4 - rows_moved_G4 - 1:
                                                val_start_row_3 = val_start_row_3 if 'val_start_row_3' in locals() and val_start_row_3 > 0 else 0
                                                for n in range(nb_columns_G3 - 1):
                                                    boxes[3]['x'][
                                                        nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - val_start_row_3] = \
                                                        boxes[3]['x'][
                                                            nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - val_start_row_3] - space_in_sections * (
                                                                nb_columns_G3 - 1 - n)
                                                    box_h_moved_g3.append(
                                                        nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - val_start_row_3)
                                                val_start_row_3 = val_start_row_3 + nb_columns_G3

                                            val_start_row_4 = val_start_row_4 if 'val_start_row_4' in locals() and val_start_row_4 > 0 else 0
                                            for j in range(nb_columns_G4 - 1):
                                                if j == 0:

                                                    result = [idx for idx, tup in enumerate(boxes_to_compare_g2) if
                                                              tup in {(boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                      nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4],
                                                                       boxes[4]['y'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                               nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4],
                                                                       4, 0)}]
                                                    boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                            nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4] = \
                                                        boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4] + space_in_sections * (
                                                                nb_columns_G4 - (j + 1))
                                                    box_h_moved_g4.append(nb_rows_G4 - 1 + nb_rows_G4 * (
                                                            nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4)

                                                    boxes_to_compare_g2[result[0]] = (boxes[4]['x'][
                                                                                          nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                                                  nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4],
                                                                                      boxes_to_compare_g2[result[0]][1],
                                                                                      boxes_to_compare_g2[result[0]][2],
                                                                                      1)

                                                else:

                                                    boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                            nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4] = \
                                                        boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4] + space_in_sections * (
                                                                nb_columns_G4 - (j + 1))
                                                    box_h_moved_g4.append(nb_rows_G4 - 1 + nb_rows_G4 * (
                                                            nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4)

                                            val_start_row_4 = val_start_row_4 + 1


                                    elif boxes_on_the_side_right_closest[0][2] == 1:
                                        space_hole = boxes_on_the_side_right_closest[0][0] - (
                                                length_von_level_G4 + width_val)
                                        space_in_sections = space_hole / (nb_columns_G4 - 1 + 1)
                                        val_start_row_4 = val_start_row_4 if 'val_start_row_4' in locals() and val_start_row_4 > 0 else 0

                                        for j in range(nb_columns_G4 - 1):
                                            if j == 0:
                                                result = [idx for idx, tup in enumerate(boxes_to_compare_g2) if tup in {
                                                    (boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                            nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4],
                                                     boxes[4]['y'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                             nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4],
                                                     4, 0)}]
                                                boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                        nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4] = \
                                                    boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                            nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4] + space_in_sections * (
                                                            nb_columns_G4 - (j + 1))
                                                box_h_moved_g4.append(nb_rows_G4 - 1 + nb_rows_G4 * (
                                                        nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4)

                                                boxes_to_compare_g2[result[0]] = (boxes[4]['x'][
                                                                                      nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                                              nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4],
                                                                                  boxes_to_compare_g2[result[0]][1],
                                                                                  boxes_to_compare_g2[result[0]][2],
                                                                                  1)

                                            else:
                                                boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                        nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4] = \
                                                    boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                            nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4] + space_in_sections * (
                                                            nb_columns_G4 - (j + 1))
                                                box_h_moved_g4.append(nb_rows_G4 - 1 + nb_rows_G4 * (
                                                        nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4)

                                        val_start_row_4 = val_start_row_4 + 1

                                elif len(boxes_on_the_side_right) == 0 and len(boxes[3]['x']) == 0:
                                    space_in_sections = (pallet_length - (length_von_level_G4 + width_val)) / (
                                            nb_columns_G4 - 1) if nb_columns_G4 > 1 else (
                                            pallet_length - (length_von_level_G4 + width_val))
                                    rows_moved_G4 = int(
                                        len(box_h_moved_g4) / (nb_columns_G4 - 1)) if nb_rows_G4 > 1 else len(
                                        box_h_moved_g4)
                                    val_start_row_4 = val_start_row_4 if 'val_start_row_4' in locals() and val_start_row_4 > 0 else 0
                                    for b in range(nb_rows_G4 - rows_moved_G4):
                                        for n in range(1, nb_columns_G4):
                                            boxes[4]['x'][
                                                nb_rows_G4 - 1 + nb_rows_G4 * (nb_columns_G4 - 1) - b - nb_rows_G4 * (
                                                        n - 1) - rows_moved_G4] = boxes[4]['x'][
                                                                                      nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                                              nb_columns_G4 - 1) - b - nb_rows_G4 * (
                                                                                              n - 1) - rows_moved_G4] + space_in_sections * (
                                                                                          nb_columns_G4 - n)
                                            box_h_moved_g4.append(
                                                nb_rows_G4 - 1 + nb_rows_G4 * (nb_columns_G4 - 1) - b - nb_rows_G4 * (
                                                        n - 1) - rows_moved_G4)
                                        val_start_row_4 = val_start_row_4 + 1

                        else:
                            no_g2_box_moved_g4 = []
                            for b in range(nb_rows_G4 - rows_moved_G4):
                                boxes_on_the_side_right = []
                                for c in range(len(boxes_to_compare_g4)):
                                    if boxes_to_compare_g4[c][2] == 3:
                                        list1 = [boxes[4]['y'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                nb_columns_G4 - 1) - b - rows_moved_G4],
                                                 boxes[4]['y'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                         nb_columns_G4 - 1) - b - rows_moved_G4] + length_val]
                                        list2 = [boxes_to_compare_g4[c][1], boxes_to_compare_g4[c][1] + width_val]
                                        if list1[1] > list2[0] and list2[1] > list1[0]:
                                            boxes_on_the_side_right.append(boxes_to_compare_g4[c])

                                    if boxes_to_compare_g4[c][2] == 1:
                                        list1 = [boxes[4]['y'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                nb_columns_G4 - 1) - b - rows_moved_G4],
                                                 boxes[4]['y'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                         nb_columns_G4 - 1) - b - rows_moved_G4] + length_val]
                                        list2 = [boxes_to_compare_g4[c][1], boxes_to_compare_g4[c][1] + width_val]
                                        if list1[1] > list2[0] and list2[1] > list1[0]:
                                            boxes_on_the_side_right.append(boxes_to_compare_g4[c])
                                if len(boxes_on_the_side_right) > 0:
                                    groups_length = [a[2] for a in boxes_on_the_side_right]
                                    if len(set(groups_length)) >= 2:
                                        val1_to_compare = None
                                        val2_to_compare = None
                                        val3_to_compare = None
                                        for tup in boxes_on_the_side_right:
                                            if tup[2] == 2:
                                                if val1_to_compare is None or tup[
                                                    0] > val1_to_compare: val1_to_compare = tup[0]
                                            if tup[2] == 3:
                                                if val2_to_compare is None or tup[
                                                    0] > val2_to_compare: val2_to_compare = tup[0]
                                            if tup[2] == 1:
                                                if val3_to_compare is None or tup[
                                                    0] > val3_to_compare: val3_to_compare = tup[0]
                                        LIST = [val1_to_compare, val2_to_compare, val3_to_compare]
                                        index = LIST.index(min([i for i in LIST if i is not None]))
                                        if index == 0:
                                            group_max_value = 2
                                        elif index == 1:
                                            group_max_value = 3
                                        elif index == 2:
                                            group_max_value = 1
                                    else:
                                        group_max_value = list(set(groups_length))[0]

                                    boxes_on_the_side_right_closest = [tup for tup in boxes_on_the_side_right if
                                                                       tup[2] == group_max_value]

                                    if boxes_on_the_side_right_closest[0][2] == 3:
                                        space_hole = boxes_on_the_side_right_closest[0][0] - (
                                                length_von_level_G4 + width_val)
                                        if nb_columns_G3 == 1:
                                            space_in_sections = space_hole / (nb_columns_G4 - 1 + 1)
                                            val_start_row_4 = val_start_row_4 if 'val_start_row_4' in locals() and val_start_row_4 > 0 else 0

                                            for j in range(nb_columns_G4 - 1):
                                                boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                        nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4] = \
                                                    boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                            nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4] + space_in_sections * (
                                                            nb_columns_G4 - (j + 1))
                                                box_h_moved_g4.append(nb_rows_G4 - 1 + nb_rows_G4 * (
                                                        nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4)
                                                if j == 0:
                                                    no_g2_box_moved_g4.append((boxes[4]['x'][
                                                                                   nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                                           nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4],
                                                                               boxes[4]['y'][
                                                                                   nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                                           nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4],
                                                                               4, 1))
                                            val_start_row_4 = val_start_row_4 + 1

                                        elif nb_columns_G3 > 1:
                                            space_in_sections = space_hole / (nb_columns_G3 - 1 + nb_columns_G4 - 1 + 1)
                                            val_start_row_3 = val_start_row_3 if 'val_start_row_3' in locals() and val_start_row_3 > 0 else 0
                                            for n in range(nb_columns_G3 - 1):
                                                boxes[3]['x'][
                                                    nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - val_start_row_3] = \
                                                    boxes[3]['x'][
                                                        nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - val_start_row_3] - space_in_sections * (
                                                            nb_columns_G3 - 1 - n)
                                                box_h_moved_g3.append(
                                                    nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - val_start_row_3)
                                            val_start_row_3 = val_start_row_3 + nb_columns_G3

                                            val_start_row_4 = val_start_row_4 if 'val_start_row_4' in locals() and val_start_row_4 > 0 else 0
                                            for j in range(nb_columns_G4 - 1):
                                                boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                        nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4] = \
                                                    boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                            nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4] + space_in_sections * (
                                                            nb_columns_G4 - (j + 1))
                                                box_h_moved_g4.append(nb_rows_G4 - 1 + nb_rows_G4 * (
                                                        nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4)
                                                if j == 0:
                                                    no_g2_box_moved_g4.append((boxes[4]['x'][
                                                                                   nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                                           nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4],
                                                                               boxes[4]['y'][
                                                                                   nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                                           nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4],
                                                                               4, 1))
                                            val_start_row_4 = val_start_row_4 + 1

                                    elif boxes_on_the_side_right_closest[0][2] == 1:
                                        space_hole = boxes_on_the_side_right_closest[0][0] - (
                                                length_von_level_G4 + width_val)
                                        space_in_sections = space_hole / (nb_columns_G4 - 1 + 1)

                                        val_start_row_4 = val_start_row_4 if 'val_start_row_4' in locals() and val_start_row_4 > 0 else 0
                                        for j in range(nb_columns_G4 - 1):
                                            boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                    nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4] = \
                                                boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                        nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4] + space_in_sections * (
                                                        nb_columns_G4 - (j + 1))
                                            box_h_moved_g4.append(nb_rows_G4 - 1 + nb_rows_G4 * (
                                                    nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4)
                                            if j == 0:
                                                no_g2_box_moved_g4.append((boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                        nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4],
                                                                           boxes[4]['y'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                                   nb_columns_G4 - 1) - nb_rows_G4 * j - val_start_row_4],
                                                                           4, 1))
                                        val_start_row_4 = val_start_row_4 + 1




                                else:
                                    space_in_sections = (pallet_length - (length_von_level_G4 + width_val)) / (
                                            nb_columns_G4 - 1) if nb_columns_G4 > 1 else (
                                            pallet_length - (length_von_level_G4 + width_val))
                                    rows_moved_G4 = int(
                                        len(box_h_moved_g4) / (nb_columns_G4 - 1)) if nb_rows_G4 > 1 else len(
                                        box_h_moved_g4)
                                    for b in range(nb_rows_G4 - rows_moved_G4):
                                        for n in range(1, nb_columns_G4):
                                            boxes[4]['x'][
                                                nb_rows_G4 - 1 + nb_rows_G4 * (nb_columns_G4 - 1) - b - nb_rows_G4 * (
                                                        n - 1) - rows_moved_G4] = boxes[4]['x'][
                                                                                      nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                                              nb_columns_G4 - 1) - b - nb_rows_G4 * (
                                                                                              n - 1) - rows_moved_G4] + space_in_sections * (
                                                                                          nb_columns_G4 - n)
                                            box_h_moved_g4.append(
                                                nb_rows_G4 - 1 + nb_rows_G4 * (nb_columns_G4 - 1) - b - nb_rows_G4 * (
                                                        n - 1) - rows_moved_G4)
                                            if n == 0:
                                                no_g2_box_moved_g4.append((boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                        nb_columns_G4 - 1) - b - nb_rows_G4 * (
                                                                                                 n - 1) - rows_moved_G4],
                                                                           boxes[4]['y'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                                   nb_columns_G4 - 1) - b - nb_rows_G4 * (
                                                                                                 n - 1) - rows_moved_G4],
                                                                           4, 1))
                                    break

                else:
                    space_in_sections = (pallet_length - (length_von_level_G4 + width_val)) / (
                            nb_columns_G4 - 1) if nb_columns_G4 > 1 else (
                            pallet_length - (length_von_level_G4 + width_val))

                    rows_moved_G4 = int(len(box_h_moved_g4) / (nb_columns_G4 - 1)) if nb_rows_G4 > 1 else len(
                        box_h_moved_g4)
                    for b in range(nb_rows_G4 - rows_moved_G4):
                        for n in range(1, nb_columns_G4):
                            boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (nb_columns_G4 - 1) - b - nb_rows_G4 * (
                                    n - 1) - rows_moved_G4] = boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                    nb_columns_G4 - 1) - b - nb_rows_G4 * (
                                                                                    n - 1) - rows_moved_G4] + space_in_sections * (
                                                                      nb_columns_G4 - n)
                            box_h_moved_g4.append(nb_rows_G4 - 1 + nb_rows_G4 * (nb_columns_G4 - 1) - b - nb_rows_G4 * (
                                    n - 1) - rows_moved_G4)

        #############################################################################################################################################################################################################################################################################################

        if li == 0 and len(boxes[3]['x']) != 0:

            nb_rows_G3 = nb_rows_G3 if 'nb_rows_G3' in locals() else len(set(boxes[3]['y']))
            nb_columns_G3 = nb_columns_G3 if 'nb_columns_G3' in locals() else len(set(boxes[3]['x']))
            length_von_level_G3 = length_von_level_G3 if 'length_von_level_G3' in locals() else min(boxes[3]['x'])

            if len(boxes[1]['x']) != 0:
                nb_rows_G1 = nb_rows_G1 if 'nb_rows_G1' in locals() else len(set(boxes[1]['y']))
                nb_columns_G1 = nb_columns_G1 if 'nb_columns_G1' in locals() else len(set(boxes[1]['x']))
                length_von_level_G1 = length_von_level_G1 if 'length_von_level_G1' in locals() else max(boxes[1]['x'])

                if len(boxes[4]['x']) != 0:
                    nb_rows_G4 = nb_rows_G4 if 'nb_rows_G4' in locals() else len(set(boxes[4]['y']))
                    nb_columns_G4 = nb_columns_G4 if 'nb_columns_G4' in locals() else len(set(boxes[4]['x']))
                    length_von_level_G4 = length_von_level_G4 if 'length_von_level_G4' in locals() else max(
                        boxes[4]['x'])

                    boxes_to_compare_g3 = []
                    for q in range(nb_rows_G1):
                        boxes_to_compare_g3.append((boxes[1]['x'][nb_columns_G1 * q + (nb_columns_G1 - 1)],
                                                    boxes[1]['y'][nb_columns_G1 * q + (nb_columns_G1 - 1)], 1, 0))
                    for c in range(nb_rows_G4):
                        boxes_to_compare_g3.append((
                            boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (nb_columns_G4 - 1) - c],
                            boxes[4]['y'][nb_rows_G4 - 1 + nb_rows_G4 * (nb_columns_G4 - 1) - c],
                            4, 0))
                else:
                    boxes_to_compare_g3 = []
                    for q in range(nb_rows_G1):
                        boxes_to_compare_g3.append((boxes[1]['x'][nb_columns_G1 * q + (nb_columns_G1 - 1)],
                                                    boxes[1]['y'][nb_columns_G1 * q + (nb_columns_G1 - 1)], 1, 0))
            elif len(boxes[4]['x']) != 0:
                nb_rows_G4 = nb_rows_G4 if 'nb_rows_G4' in locals() else len(set(boxes[4]['y']))
                nb_columns_G4 = nb_columns_G4 if 'nb_columns_G4' in locals() else len(set(boxes[4]['x']))
                length_von_level_G4 = length_von_level_G4 if 'length_von_level_G4' in locals() else max(boxes[4]['x'])

                boxes_to_compare_g3 = []
                for c in range(nb_rows_G4):
                    boxes_to_compare_g3.append((boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (nb_columns_G4 - 1) - c],
                                                boxes[4]['y'][nb_rows_G4 - 1 + nb_rows_G4 * (nb_columns_G4 - 1) - c], 4,
                                                0))
            else:
                boxes_to_compare_g3 = []

            ################
            if len(boxes[2]['y']) != 0:
                boxes_from_g2_to_compare = []
                for u in range(nb_rows_G3):
                    for p in range(nb_columns_G2):
                        if boxes[2]['y'][nb_columns_G2 * nb_rows_G2 - 1 - 0 * nb_columns_G2 - p] + length_val > \
                                boxes[3]['y'][nb_columns_G3 * nb_rows_G3 - 1 - 1 * 0 - nb_columns_G3 * u] and \
                                boxes[2]['x'][nb_columns_G2 * nb_rows_G2 - 1 - 0 * nb_columns_G2 - p] + width_val < \
                                boxes[3]['x'][nb_columns_G3 * nb_rows_G3 - 1 - 1 * 0 - nb_columns_G3 * u]:
                            boxes_from_g2_to_compare.append((boxes[2]['x'][
                                                                 nb_columns_G2 * nb_rows_G2 - 1 - 0 * nb_columns_G2 - p],
                                                             boxes[2]['y'][
                                                                 nb_columns_G2 * nb_rows_G2 - 1 - 0 * nb_columns_G2 - p],
                                                             2, 0))

                if len(boxes_from_g2_to_compare) != 0:
                    boxes_from_g2_to_compare = list(set(boxes_from_g2_to_compare))
                    boxes_to_compare_g3 = boxes_to_compare_g3 + boxes_from_g2_to_compare
            ################################################

            if 'boxes_to_compare_g2' in locals():
                if len(boxes_to_compare_g2) != 0:
                    if len(boxes_to_compare_g3) != 0:
                        for r in range(len(boxes_to_compare_g3)):
                            for e in range(len(boxes_to_compare_g2)):
                                if boxes_to_compare_g2[e][0] == boxes_to_compare_g3[r][0] and \
                                        boxes_to_compare_g2[e][1] == boxes_to_compare_g3[r][1] and \
                                        boxes_to_compare_g2[e][2] == boxes_to_compare_g3[r][2]:
                                    list_update = list(boxes_to_compare_g3[r])
                                    list_update[3] = boxes_to_compare_g2[e][3]
                                    tuple_update = tuple(list_update)
                                    boxes_to_compare_g3[r] = tuple_update
            else:
                if 'no_g2_box_moved_g4' in locals():
                    if len(no_g2_box_moved_g4) != 0:
                        if len(boxes_to_compare_g3) != 0:
                            for r in range(len(boxes_to_compare_g3)):
                                for e in range(len(no_g2_box_moved_g4)):
                                    if no_g2_box_moved_g4[e][0] == boxes_to_compare_g3[r][0] and \
                                            no_g2_box_moved_g4[e][1] == boxes_to_compare_g3[r][1] and \
                                            no_g2_box_moved_g4[e][2] == boxes_to_compare_g3[r][2]:
                                        list_update = list(boxes_to_compare_g3[r])
                                        list_update[3] = no_g2_box_moved_g4[e][3]
                                        tuple_update = tuple(list_update)
                                        boxes_to_compare_g3[r] = tuple_update
                if 'no_g2_box_moved_g1' in locals():
                    if len(no_g2_box_moved_g1) != 0:
                        if len(boxes_to_compare_g3) != 0:
                            for r in range(len(boxes_to_compare_g3)):
                                for e in range(len(no_g2_box_moved_g1)):
                                    if no_g2_box_moved_g1[e][0] == boxes_to_compare_g3[r][0] and \
                                            no_g2_box_moved_g1[e][1] == boxes_to_compare_g3[r][1] and \
                                            no_g2_box_moved_g1[e][2] == boxes_to_compare_g3[r][2]:
                                        list_update = list(boxes_to_compare_g3[r])
                                        list_update[3] = no_g2_box_moved_g1[e][3]
                                        tuple_update = tuple(list_update)
                                        boxes_to_compare_g3[r] = tuple_update
            if len(boxes_to_compare_g3) != 0:
                rows_moved_G3 = int(len(box_h_moved_g3) / (nb_columns_G3 - 1)) if nb_columns_G3 > 1 else len(
                    box_h_moved_g3)

                if 'nb_rows_G1' in locals():
                    rows_moved_G1 = int(len(box_h_moved_g1) / (nb_columns_G1 - 1)) if nb_columns_G1 > 1 else len(
                        box_h_moved_g1)

                for b in range(nb_rows_G3 - rows_moved_G3):
                    boxes_on_the_side = []
                    for c in range(len(boxes_to_compare_g3)):
                        if boxes_to_compare_g3[c][2] == 1:
                            list1 = [boxes[3]['y'][
                                         nb_columns_G3 * nb_rows_G3 - 1 - 1 * 0 - b * nb_columns_G3 - rows_moved_G3 * nb_columns_G3],
                                     boxes[3]['y'][
                                         nb_columns_G3 * nb_rows_G3 - 1 - 1 * 0 - b * nb_columns_G3 - rows_moved_G3 * nb_columns_G3] + width_val]
                            list2 = [boxes_to_compare_g3[c][1], boxes_to_compare_g3[c][1] + width_val]
                            if list1[1] > list2[0] and list2[1] > list1[0]:
                                boxes_on_the_side.append(boxes_to_compare_g3[c])

                        if boxes_to_compare_g3[c][2] == 4:
                            list1 = [boxes[3]['y'][
                                         nb_columns_G3 * nb_rows_G3 - 1 - 1 * 0 - b * nb_columns_G3 - rows_moved_G3 * nb_columns_G3],
                                     boxes[3]['y'][
                                         nb_columns_G3 * nb_rows_G3 - 1 - 1 * 0 - b * nb_columns_G3 - rows_moved_G3 * nb_columns_G3] + width_val]
                            list2 = [boxes_to_compare_g3[c][1], boxes_to_compare_g3[c][1] + length_val]
                            if list1[1] > list2[0] and list2[1] > list1[0]:
                                boxes_on_the_side.append(boxes_to_compare_g3[c])

                        if boxes_to_compare_g3[c][2] == 2:
                            list1 = [boxes[3]['y'][
                                         nb_columns_G3 * nb_rows_G3 - 1 - 1 * 0 - b * nb_columns_G3 - rows_moved_G3 * nb_columns_G3],
                                     boxes[3]['y'][
                                         nb_columns_G3 * nb_rows_G3 - 1 - 1 * 0 - b * nb_columns_G3 - rows_moved_G3 * nb_columns_G3] + width_val]
                            list2 = [boxes_to_compare_g3[c][1], boxes_to_compare_g3[c][1] + length_val]
                            if list1[1] > list2[0] and list2[1] > list1[0]:
                                boxes_on_the_side.append(boxes_to_compare_g3[c])
                    groups = [c[2] for c in boxes_on_the_side]

                    if len(set(groups)) >= 2:
                        val1_to_compare = None
                        val2_to_compare = None
                        val3_to_compare = None
                        for tup in boxes_on_the_side:
                            if tup[2] == 1:
                                if val1_to_compare is None or tup[0] + length_val > val1_to_compare: val1_to_compare = \
                                    tup[0] + length_val
                            if tup[2] == 4:
                                if val2_to_compare is None or tup[0] + width_val > val2_to_compare: val2_to_compare = \
                                    tup[0] + width_val
                            if tup[2] == 2:
                                if val3_to_compare is None or tup[0] + width_val > val3_to_compare: val3_to_compare = \
                                    tup[0] + width_val
                        LIST = [val1_to_compare, val2_to_compare, val3_to_compare]
                        index = LIST.index(max([i for i in LIST if i is not None]))
                        if index == 0:
                            group_max_value = 1
                        elif index == 1:
                            group_max_value = 4
                        elif index == 2:
                            group_max_value = 2
                        boxes_max_x_pos = [a for a in boxes_on_the_side if a[2] == group_max_value]
                        boxes_not_yet_hm = [t for t in boxes_max_x_pos if t[3] == 0]
                        if len(boxes_not_yet_hm) == 0:
                            if boxes_max_x_pos[0][2] == 1:
                                hole_distance = length_von_level_G3 - (boxes_max_x_pos[0][0] + length_val)
                            elif boxes_max_x_pos[0][2] == 4:
                                hole_distance = length_von_level_G3 - (boxes_max_x_pos[0][0] + width_val)
                            elif boxes_max_x_pos[0][2] == 2:
                                hole_distance = length_von_level_G3 - (
                                        boxes_max_x_pos[0][0] + len(boxes_max_x_pos) * width_val)

                            space_in_sections = hole_distance / (nb_columns_G3 - 1 + 1)
                            for n in range(nb_columns_G3 - 1):
                                boxes[3]['x'][
                                    nb_columns_G3 * nb_rows_G3 - 1 - b * nb_columns_G3 - 1 * n - rows_moved_G3 * nb_columns_G3] = \
                                    boxes[3]['x'][
                                        nb_columns_G3 * nb_rows_G3 - 1 - b * nb_columns_G3 - 1 * n - rows_moved_G3 * nb_columns_G3] - space_in_sections * (
                                            nb_columns_G3 - 1 - n)
                                box_h_moved_g3.append(
                                    nb_columns_G3 * nb_rows_G3 - 1 - b * nb_columns_G3 - 1 * n - rows_moved_G3 * nb_columns_G3)
                            continue
                    else:
                        boxes_not_yet_hm = [tup for tup in boxes_on_the_side if tup[3] == 0]

                    if len(boxes_not_yet_hm) == 0:
                        if len(boxes_on_the_side) == 0:
                            if 'nb_columns_G4' in locals():
                                if nb_columns_G4 > 1:
                                    list_g4_inside = []
                                    for c in range(nb_rows_G4):
                                        for d in range(nb_columns_G4):
                                            list1 = [boxes[3]['y'][
                                                         nb_columns_G3 * nb_rows_G3 - 1 - 1 * 0 - b * nb_columns_G3 - rows_moved_G3 * nb_columns_G3],
                                                     boxes[3]['y'][
                                                         nb_columns_G3 * nb_rows_G3 - 1 - 1 * 0 - b * nb_columns_G3 - rows_moved_G3 * nb_columns_G3] + width_val]
                                            list2 = [boxes[4]['y'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                    nb_columns_G4 - 1) - d * nb_rows_G4 - c], boxes[4]['y'][
                                                         nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                 nb_columns_G4 - 1) - d * nb_rows_G4 - c] + length_val]
                                            if list1[1] > list2[0] and list2[1] > list1[0]:
                                                list_g4_inside.append((boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                        nb_columns_G4 - 1) - d * nb_rows_G4 - c],
                                                                       boxes[4]['y'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                               nb_columns_G4 - 1) - d * nb_rows_G4 - c],
                                                                       4,
                                                                       0))
                                    if len(list_g4_inside) > 0:
                                        space_in_sections = (length_von_level_G3 - list_g4_inside[0][0] - width_val) / (
                                                nb_columns_G3 - 1 + 1) if nb_columns_G3 > 1 else (
                                                length_von_level_G3 - list_g4_inside[0][0] - width_val)
                                        for n in range(nb_columns_G3 - 1):
                                            boxes[3]['x'][
                                                nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - b * nb_columns_G3 - rows_moved_G3 * nb_columns_G3] = \
                                                boxes[3]['x'][
                                                    nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - b * nb_columns_G3 - rows_moved_G3 * nb_columns_G3] - space_in_sections * (
                                                        nb_columns_G3 - 1 - n)
                                            box_h_moved_g3.append(
                                                nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - b * nb_columns_G3 - rows_moved_G3 * nb_columns_G3)
                                        continue
                                    else:
                                        space_in_sections = length_von_level_G3 / (
                                                nb_columns_G3 - 1) if nb_columns_G3 > 1 else length_von_level_G3
                                        for n in range(nb_columns_G3 - 1):
                                            boxes[3]['x'][
                                                nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - b * nb_columns_G3 - rows_moved_G3 * nb_columns_G3] = \
                                                boxes[3]['x'][
                                                    nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - b * nb_columns_G3 - rows_moved_G3 * nb_columns_G3] - space_in_sections * (
                                                        nb_columns_G3 - 1 - n)
                                            box_h_moved_g3.append(
                                                nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - b * nb_columns_G3 - rows_moved_G3 * nb_columns_G3)
                                        continue
                                else:
                                    space_in_sections = length_von_level_G3 / (
                                            nb_columns_G3 - 1) if nb_columns_G3 > 1 else length_von_level_G3
                                    for n in range(nb_columns_G3 - 1):
                                        boxes[3]['x'][
                                            nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - b * nb_columns_G3 - rows_moved_G3 * nb_columns_G3] = \
                                            boxes[3]['x'][
                                                nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - b * nb_columns_G3 - rows_moved_G3 * nb_columns_G3] - space_in_sections * (
                                                    nb_columns_G3 - 1 - n)
                                        box_h_moved_g3.append(
                                            nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - b * nb_columns_G3 - rows_moved_G3 * nb_columns_G3)
                                    continue

                            else:
                                space_in_sections = length_von_level_G3 / (
                                        nb_columns_G3 - 1) if nb_columns_G3 > 1 else length_von_level_G3
                                for n in range(nb_columns_G3 - 1):
                                    boxes[3]['x'][
                                        nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - b * nb_columns_G3 - rows_moved_G3 * nb_columns_G3] = \
                                        boxes[3]['x'][
                                            nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - b * nb_columns_G3 - rows_moved_G3 * nb_columns_G3] - space_in_sections * (
                                                nb_columns_G3 - 1 - n)
                                    box_h_moved_g3.append(
                                        nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - b * nb_columns_G3 - rows_moved_G3 * nb_columns_G3)
                                continue
                        else:
                            if nb_columns_G3 > 1:
                                val1_to_compare = None
                                val2_to_compare = None
                                val3_to_compare = None
                                for tup in boxes_on_the_side:
                                    if tup[2] == 1:
                                        if val1_to_compare is None or tup[
                                            0] + length_val > val1_to_compare: val1_to_compare = tup[0] + length_val
                                    if tup[2] == 4:
                                        if val2_to_compare is None or tup[
                                            0] + width_val > val2_to_compare: val2_to_compare = tup[0] + width_val
                                    if tup[2] == 2:
                                        if val3_to_compare is None or tup[
                                            0] + width_val > val3_to_compare: val3_to_compare = tup[0] + width_val
                                LIST = [val1_to_compare, val2_to_compare, val3_to_compare]
                                index = LIST.index(max([i for i in LIST if i is not None]))
                                if index == 0:
                                    group_max_value = 1
                                elif index == 1:
                                    group_max_value = 4
                                elif index == 2:
                                    group_max_value = 2
                                boxes_on_the_side_closest = [a for a in boxes_on_the_side if a[2] == group_max_value]
                                if len(boxes_on_the_side_closest) > 1:
                                    x_values = [a[0] for a in boxes_on_the_side_closest]
                                    max_x_value = max(x_values)
                                else:
                                    max_x_value = boxes_on_the_side_closest[0][0]
                                if boxes_on_the_side_closest[0][2] == 1:
                                    hole_distance = length_von_level_G3 - (max_x_value + length_val)
                                elif boxes_on_the_side_closest[0][2] == 4:
                                    hole_distance = length_von_level_G3 - (max_x_value + width_val)
                                elif boxes_on_the_side_closest[0][2] == 2:
                                    hole_distance = length_von_level_G3 - (
                                            max_x_value + len(boxes_on_the_side_closest) * width_val)

                                space_in_sections = hole_distance / (nb_columns_G3 - 1 + 1)
                                for n in range(nb_columns_G3 - 1):
                                    boxes[3]['x'][
                                        nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - b * nb_columns_G3 - rows_moved_G3 * nb_columns_G3] = \
                                        boxes[3]['x'][
                                            nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - b * nb_columns_G3 - rows_moved_G3 * nb_columns_G3] - space_in_sections * (
                                                nb_columns_G3 - 1 - n)
                                    box_h_moved_g3.append(
                                        nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - b * nb_columns_G3 - rows_moved_G3 * nb_columns_G3)

                                set_list = set(boxes_on_the_side_closest)
                                result = [idx for idx, tup in enumerate(boxes_to_compare_g3) if tup in set_list]
                                for t in result:
                                    boxes_to_compare_g3[t] = (
                                        boxes_to_compare_g3[t][0], boxes_to_compare_g3[t][1], boxes_to_compare_g3[t][2],
                                        1)

                                continue
                            else:
                                continue

                    else:
                        val1_to_compare = None
                        val2_to_compare = None
                        val3_to_compare = None
                        for tup in boxes_not_yet_hm:
                            if tup[2] == 1:
                                if val1_to_compare is None or tup[0] + length_val > val1_to_compare: val1_to_compare = \
                                    tup[0] + length_val
                            if tup[2] == 4:
                                if val2_to_compare is None or tup[0] + width_val > val2_to_compare: val2_to_compare = \
                                    tup[0] + width_val
                            if tup[2] == 2:
                                if val3_to_compare is None or tup[0] + length_val > val3_to_compare: val3_to_compare = \
                                    tup[0] + width_val
                        LIST = [val1_to_compare, val2_to_compare, val3_to_compare]
                        index = LIST.index(max([i for i in LIST if i is not None]))
                        if index == 0:
                            group_max_value = 1
                        elif index == 1:
                            group_max_value = 4
                        elif index == 2:
                            group_max_value = 2
                        boxes_on_the_side_closest = [tup for tup in boxes_on_the_side if
                                                     tup[2] == group_max_value and tup[3] == 0]
                        if len(boxes_on_the_side_closest) != 0:
                            if boxes_on_the_side_closest[0][2] == 1:
                                hole_distance = length_von_level_G3 - (boxes_on_the_side_closest[0][0] + length_val)
                            elif boxes_on_the_side_closest[0][2] == 4:
                                hole_distance = length_von_level_G3 - (boxes_on_the_side_closest[0][0] + width_val)
                            elif boxes_on_the_side_closest[0][2] == 2:
                                hole_distance = length_von_level_G3 - (boxes_on_the_side_closest[0][0] + len(
                                    boxes_on_the_side_closest) * width_val)
                        else:
                            hole_distance = "Hole with pallet edge"

                    if hole_distance == "Hole with pallet edge":
                        space_in_sections = length_von_level_G3 / (
                                nb_columns_G3 - 1) if nb_columns_G3 > 1 else length_von_level_G3
                        for p in range(nb_rows_G3 - rows_moved_G3):
                            for n in range(nb_columns_G3 - 1):
                                boxes[3]['x'][
                                    nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - nb_columns_G3 * p - rows_moved_G3 * nb_columns_G3] = \
                                    boxes[3]['x'][
                                        nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - nb_columns_G3 * p - rows_moved_G3 * nb_columns_G3] - space_in_sections * (
                                            nb_columns_G3 - 1 - n)
                                box_h_moved_g3.append(
                                    nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - nb_columns_G3 * p - rows_moved_G3 * nb_columns_G3)
                        break
                    else:
                        if boxes_on_the_side_closest[0][2] != 2:
                            n_columns_g = locals()['nb_columns_G' + str(boxes_on_the_side_closest[0][2])]

                            if n_columns_g > 1:
                                if nb_columns_G3 > 1:

                                    space_in_sections = hole_distance / (nb_columns_G3 - 1 + n_columns_g - 1 + 1)

                                    for n in range(nb_columns_G3 - 1):
                                        boxes[3]['x'][
                                            nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - nb_columns_G3 * p - rows_moved_G3 * nb_columns_G3] = \
                                            boxes[3]['x'][
                                                nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - nb_columns_G3 * p - rows_moved_G3 * nb_columns_G3] - space_in_sections * (
                                                    nb_columns_G3 - 1 - n)
                                        box_h_moved_g3.append(
                                            nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - nb_columns_G3 * p - rows_moved_G3 * nb_columns_G3)

                                    if boxes_on_the_side_closest[0][2] == 1:

                                        val_start_row_1 = val_start_row_1 if 'val_start_row_1' in locals() and val_start_row_1 > 0 else 0
                                        for p in range(len(boxes_on_the_side_closest)):
                                            for m in range(nb_columns_G1 - 1):
                                                boxes[1]['x'][
                                                    nb_columns_G1 * p + (nb_columns_G1 - 1) - m + val_start_row_1] = \
                                                    boxes[1]['x'][nb_columns_G1 * p + (
                                                            nb_columns_G1 - 1) - m + val_start_row_1] + space_in_sections * (
                                                            n_columns_g - 1 - m)
                                                box_h_moved_g1.append(
                                                    nb_columns_G1 * p + (nb_columns_G1 - 1) - m + val_start_row_1)

                                                if m == 0:
                                                    result = [idx for idx, tup in enumerate(boxes_to_compare_g3) if
                                                              tup in {boxes_on_the_side_closest[p]}]

                                                    boxes_to_compare_g3[result[0]] = (boxes[1]['x'][
                                                                                          nb_columns_G1 * p + (
                                                                                                  nb_columns_G1 - 1) - m + val_start_row_1],
                                                                                      boxes_to_compare_g3[result[0]][1],
                                                                                      boxes_to_compare_g3[result[0]][2],
                                                                                      boxes_to_compare_g3[result[0]][3])

                                                    boxes_on_the_side_closest[p] = (boxes[1]['x'][nb_columns_G1 * p + (
                                                            nb_columns_G1 - 1) - m + val_start_row_1],
                                                                                    boxes_on_the_side_closest[p][1],
                                                                                    boxes_on_the_side_closest[p][2],
                                                                                    boxes_on_the_side_closest[p][3])
                                        val_start_row_1 = val_start_row_1 + nb_columns_G1 * len(
                                            boxes_on_the_side_closest)
                                        set_list = set(boxes_on_the_side_closest)
                                        result = [idx for idx, tup in enumerate(boxes_to_compare_g3) if tup in set_list]
                                        for t in result:
                                            boxes_to_compare_g3[t] = (
                                                boxes_to_compare_g3[t][0], boxes_to_compare_g3[t][1],
                                                boxes_to_compare_g3[t][2], 1)

                                    elif boxes_on_the_side_closest[0][2] == 4:
                                        val_start_row_4 = val_start_row_4 if 'val_start_row_4' in locals() and val_start_row_4 > 0 else 0
                                        for q in range(len(boxes_on_the_side_closest)):
                                            for j in range(nb_columns_G4 - 1):
                                                boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                        nb_columns_G4 - 1) - q - nb_rows_G4 * j - val_start_row_4] = \
                                                    boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                            nb_columns_G4 - 1) - q - nb_rows_G4 * j - val_start_row_4] + space_in_sections * (
                                                            nb_columns_G4 - 1 - j)
                                                box_h_moved_g4.append(nb_rows_G4 - 1 + nb_rows_G4 * (
                                                        nb_columns_G4 - 1) - q - nb_rows_G4 * j - val_start_row_4)
                                                if j == 0:
                                                    result = [idx for idx, tup in enumerate(boxes_to_compare_g3) if
                                                              tup in {boxes_on_the_side_closest[q]}]
                                                    boxes_to_compare_g3[result[0]] = (boxes[4]['x'][
                                                                                          nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                                                  nb_columns_G4 - 1) - q - nb_rows_G4 * j - val_start_row_4],
                                                                                      boxes_to_compare_g3[result[0]][1],
                                                                                      boxes_to_compare_g3[result[0]][2],
                                                                                      boxes_to_compare_g3[result[0]][3])
                                                    boxes_on_the_side_closest[q] = (boxes[4]['x'][
                                                                                        nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                                                nb_columns_G4 - 1) - q - nb_rows_G4 * j - val_start_row_4],
                                                                                    boxes_on_the_side_closest[q][1],
                                                                                    boxes_on_the_side_closest[q][2],
                                                                                    boxes_on_the_side_closest[q][3])

                                        val_start_row_4 = val_start_row_4 + len(boxes_on_the_side_closest)
                                        set_list = set(boxes_on_the_side_closest)
                                        result = [idx for idx, tup in enumerate(boxes_to_compare_g3) if tup in set_list]
                                        for t in result:
                                            boxes_to_compare_g3[t] = (
                                                boxes_to_compare_g3[t][0], boxes_to_compare_g3[t][1],
                                                boxes_to_compare_g3[t][2], 1)

                                else:

                                    space_in_sections = hole_distance / (n_columns_g - 1 + 1)

                                    if boxes_on_the_side_closest[0][2] == 1:

                                        val_start_row_1 = val_start_row_1 if 'val_start_row_1' in locals() and val_start_row_1 > 0 else 0
                                        for p in range(len(boxes_on_the_side_closest)):
                                            for m in range(nb_columns_G1 - 1):
                                                boxes[1]['x'][
                                                    nb_columns_G1 * p + (nb_columns_G1 - 1) - m + val_start_row_1] = \
                                                    boxes[1]['x'][nb_columns_G1 * p + (
                                                            nb_columns_G1 - 1) - m + val_start_row_1] + space_in_sections * (
                                                            n_columns_g - 1 - m)
                                                box_h_moved_g1.append(
                                                    nb_columns_G1 * p + (nb_columns_G1 - 1) - m + val_start_row_1)

                                                if m == 0:
                                                    result = [idx for idx, tup in enumerate(boxes_to_compare_g3) if
                                                              tup in {boxes_on_the_side_closest[p]}]

                                                    boxes_to_compare_g3[result[0]] = (boxes[1]['x'][
                                                                                          nb_columns_G1 * p + (
                                                                                                  nb_columns_G1 - 1) - m + val_start_row_1],
                                                                                      boxes_to_compare_g3[result[0]][1],
                                                                                      boxes_to_compare_g3[result[0]][2],
                                                                                      boxes_to_compare_g3[result[0]][3])

                                                    boxes_on_the_side_closest[p] = (boxes[1]['x'][nb_columns_G1 * p + (
                                                            nb_columns_G1 - 1) - m + val_start_row_1],
                                                                                    boxes_on_the_side_closest[p][1],
                                                                                    boxes_on_the_side_closest[p][2],
                                                                                    boxes_on_the_side_closest[p][3])
                                        val_start_row_1 = val_start_row_1 + nb_columns_G1 * len(
                                            boxes_on_the_side_closest)
                                        set_list = set(boxes_on_the_side_closest)
                                        result = [idx for idx, tup in enumerate(boxes_to_compare_g3) if tup in set_list]
                                        for t in result:
                                            boxes_to_compare_g3[t] = (
                                                boxes_to_compare_g3[t][0], boxes_to_compare_g3[t][1],
                                                boxes_to_compare_g3[t][2], 1)

                                    elif boxes_on_the_side_closest[0][2] == 4:
                                        val_start_row_4 = val_start_row_4 if 'val_start_row_4' in locals() and val_start_row_4 > 0 else 0
                                        for q in range(len(boxes_on_the_side_closest)):
                                            for j in range(nb_columns_G4 - 1):
                                                boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                        nb_columns_G4 - 1) - q - nb_rows_G4 * j - val_start_row_4] = \
                                                    boxes[4]['x'][nb_rows_G4 - 1 + nb_rows_G4 * (
                                                            nb_columns_G4 - 1) - q - nb_rows_G4 * j - val_start_row_4] + space_in_sections * (
                                                            nb_columns_G4 - 1 - j)
                                                box_h_moved_g4.append(nb_rows_G4 - 1 + nb_rows_G4 * (
                                                        nb_columns_G4 - 1) - q - nb_rows_G4 * j - val_start_row_4)
                                                if j == 0:
                                                    result = [idx for idx, tup in enumerate(boxes_to_compare_g3) if
                                                              tup in {boxes_on_the_side_closest[q]}]
                                                    boxes_to_compare_g3[result[0]] = (boxes[4]['x'][
                                                                                          nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                                                  nb_columns_G4 - 1) - q - nb_rows_G4 * j - val_start_row_4],
                                                                                      boxes_to_compare_g3[result[0]][1],
                                                                                      boxes_to_compare_g3[result[0]][2],
                                                                                      boxes_to_compare_g3[result[0]][3])
                                                    boxes_on_the_side_closest[q] = (boxes[4]['x'][
                                                                                        nb_rows_G4 - 1 + nb_rows_G4 * (
                                                                                                nb_columns_G4 - 1) - q - nb_rows_G4 * j - val_start_row_4],
                                                                                    boxes_on_the_side_closest[q][1],
                                                                                    boxes_on_the_side_closest[q][2],
                                                                                    boxes_on_the_side_closest[q][3])

                                        val_start_row_4 = val_start_row_4 + len(boxes_on_the_side_closest)
                                        set_list = set(boxes_on_the_side_closest)
                                        result = [idx for idx, tup in enumerate(boxes_to_compare_g3) if tup in set_list]
                                        for t in result:
                                            boxes_to_compare_g3[t] = (
                                                boxes_to_compare_g3[t][0], boxes_to_compare_g3[t][1],
                                                boxes_to_compare_g3[t][2], 1)

                            else:
                                if nb_columns_G3 > 1:
                                    space_in_sections = hole_distance / (nb_columns_G3 - 1 + 1)
                                    for n in range(1, nb_columns_G3):
                                        boxes[3]['x'][
                                            nb_columns_G3 * nb_rows_G3 - 1 * n - nb_columns_G3 * b - rows_moved_G3 * nb_columns_G3] = \
                                            boxes[3]['x'][
                                                nb_columns_G3 * nb_rows_G3 - 1 * n - nb_columns_G3 * b - rows_moved_G3 * nb_columns_G3] - space_in_sections * (
                                                    nb_columns_G3 - n)
                                        box_h_moved_g3.append(
                                            nb_columns_G3 * nb_rows_G3 - 1 * n - nb_columns_G3 * b - rows_moved_G3 * nb_columns_G3)

                                    set_list = set(boxes_on_the_side_closest)
                                    result = [idx for idx, tup in enumerate(boxes_to_compare_g3) if tup in set_list]
                                    for t in result:
                                        boxes_to_compare_g3[t] = (
                                            boxes_to_compare_g3[t][0], boxes_to_compare_g3[t][1],
                                            boxes_to_compare_g3[t][2],
                                            1)

                                else:
                                    space_in_sections = 0
                        else:
                            space_in_sections = hole_distance / (nb_columns_G3 - 1 + 1)
                            for n in range(1, nb_columns_G3):
                                boxes[3]['x'][
                                    nb_columns_G3 * nb_rows_G3 - 1 * n - nb_columns_G3 * b - rows_moved_G3 * nb_columns_G3] = \
                                    boxes[3]['x'][
                                        nb_columns_G3 * nb_rows_G3 - 1 * n - nb_columns_G3 * b - rows_moved_G3 * nb_columns_G3] - space_in_sections * (
                                            nb_columns_G3 - n)
                                box_h_moved_g3.append(
                                    nb_columns_G3 * nb_rows_G3 - 1 * n - nb_columns_G3 * b - rows_moved_G3 * nb_columns_G3)

            else:
                space_in_sections = length_von_level_G3 / (
                        nb_columns_G3 - 1) if nb_columns_G3 > 1 else length_von_level_G3
                rows_moved_G3 = int(len(box_h_moved_g3) / (nb_columns_G3 - 1)) if nb_columns_G3 > 1 else len(
                    box_h_moved_g3)
                for p in range(nb_rows_G3 - rows_moved_G3):
                    for n in range(nb_columns_G3 - 1):
                        boxes[3]['x'][
                            nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - nb_columns_G3 * p - rows_moved_G3 * nb_columns_G3] = \
                            boxes[3]['x'][
                                nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - nb_columns_G3 * p - rows_moved_G3 * nb_columns_G3] - space_in_sections * (
                                    nb_columns_G3 - 1 - n)
                        box_h_moved_g3.append(
                            nb_columns_G3 * nb_rows_G3 - 1 - 1 * n - nb_columns_G3 * p - rows_moved_G3 * nb_columns_G3)

    return boxes
