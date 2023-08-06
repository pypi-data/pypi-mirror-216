import json
import os
from xml.dom.minidom import parse


def obfuscate_xml(pal_path: str, *, use_new_product_codes: bool = True, use_new_description: bool = True) -> dict:
    def create_box(product_code: str, dimension_x: float | str, dimension_y: float | str, dimension_z: float | str,
                   anchor_x: float | str, anchor_y: float | str, anchor_z: float | str, approach: int | str):
        dimension_x = float(dimension_x)
        dimension_y = float(dimension_y)
        dimension_z = float(dimension_z)
        anchor_x = float(anchor_x)
        anchor_y = float(anchor_y)
        anchor_z = float(anchor_z)
        approach = str(approach)
        if use_new_product_codes:
            product_code = new_product_codes[product_code]
        return {
            "product_code": product_code,
            "anchor": {
                "x": anchor_x,
                "y": anchor_y,
                "z": anchor_z
            },
            "dimension": {
                "x": dimension_x,
                "y": dimension_y,
                "z": dimension_z
            },
            "approach": approach,
        }

    def load_articles(path: str) -> tuple[dict, dict]:
        doc = parse(path)
        out = {}
        orderLines = {}
        for orderLine in doc.getElementsByTagName("orderLines"):
            orderLines[orderLine.getAttribute("articleID")] = orderLine.getAttribute("shippingGroup")

        new_product_code = {}
        for i, ar in enumerate(doc.getElementsByTagName("articles")):
            art_id = ar.getAttribute("articleID")
            new_product_code[art_id] = str(i)
            description = ar.getAttribute("description")
            if use_new_description:
                description = orderLines[art_id] + art_id
            res = {
                "description": description,
                "weight": float(ar.getAttribute("weight")),
                "shippingGroup": orderLines[art_id]
            }
            if use_new_product_codes:
                out[str(i)] = res
            else:
                out[str(ar.getAttribute("articleID"))] = res
        return out, new_product_code

    # check pal_path is not ord path instead, if so change it
    if pal_path.endswith(".ord.xml"):
        pal_path = pal_path.replace(".ord.xml", ".pal.xml")

    # check if pal_path exists and if not raise an error
    if not os.path.exists(pal_path):
        raise FileNotFoundError(f'File not found: {pal_path}')

    if not os.path.exists(pal_path.replace(".pal.xml", ".ord.xml")):
        raise FileNotFoundError(f'File not found: {pal_path.replace(".pal.xml", ".ord.xml")}')

    pallets = []
    articles, new_product_codes = load_articles(pal_path.replace(".pal.xml", ".ord.xml"))
    document = parse(pal_path)

    for stackedPallet in document.getElementsByTagName("stackedPallet"):
        dimension = stackedPallet.getElementsByTagName("dimesion")  # not my typo it is in the xml file :O
        if len(dimension) == 0:
            dimension = stackedPallet.getElementsByTagName("dimension")
        dimension = dimension[0]
        # palletNr are the last 3 digits of the palletNr
        pallet = {
            "palletNr": stackedPallet.getAttribute("palletNr")[-3:],
            "palletType": stackedPallet.getAttribute("usedPalletType"),
            "palletDimension": {
                "x": float(dimension.getAttribute("x")),
                "y": float(dimension.getAttribute("y"))
            },
            "boxes": []
        }

        for stackedItem in stackedPallet.getElementsByTagName("stackedItem"):
            # print(stackedItem.getAttribute("sequenceNumber"))
            s = stackedItem.getElementsByTagName("shape")[0]
            a = stackedItem.getElementsByTagName("anchor")[0]
            app = stackedItem.getAttribute("approach")
            el_id = stackedItem.getElementsByTagName("articleAlternative")[0].getAttribute("articleID")
            pallet["boxes"].append(
                create_box(el_id, s.getAttribute("x"), s.getAttribute("y"), s.getAttribute("z"), a.getAttribute("x"),
                           a.getAttribute("y"), a.getAttribute("z"), app))
        pallets.append(pallet)
    return {
        "pallets": pallets,
        "articles": articles,
        "orderID": document.getElementsByTagName("replyResult")[0].getAttribute("orderID"),
    }


def main() -> None:
    import sys
    import tqdm
    # check if the user has provided a path to the xml file or to a directory if it is a directory then we will
    # search for all the pal.xml files in the directory and subdirectories and add it to a list if it is a file then
    # we will add it to the list if the user has not provided a path give an error message and exit
    if len(sys.argv) == 1:
        print("Please provide a path to the xml file or to a directory")
        exit(1)
    elif len(sys.argv) == 2:
        import os
        path = sys.argv[1]
        xml_files = []
        if path.endswith(".pal.xml"):
            xml_files.append(path)
        else:
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.endswith(".pal.xml"):
                        xml_files.append(os.path.join(root, file))
        # if list is empty then no xml files were found give an error message and exit
        if len(xml_files) == 0:
            print("No xml files found")
            exit(1)
        # iterate over the list of xml files and obfuscate them, and save each pallet and articles to 2 json files
        # called *.pal.json and *art.json where * is the name of the xml file after the . in the name everything will
        # be in a folder called obfuscated output on the same level as the program

        # create the obfuscated folder if it does not exist
        if not os.path.exists("obfuscated_output"):
            os.makedirs("obfuscated_output")

        for xml_file in tqdm.tqdm(xml_files, desc="Obfuscating xml files", unit="files", dynamic_ncols=True):
            order = obfuscate_xml(xml_file)
            name = xml_file.split(".")[-3]
            with open(f"obfuscated_output/{name}.order.json", "w") as f:
                json.dump(order, f, indent=4)
    else:
        print("Please provide only one path")
        exit(1)


if __name__ == '__main__':
    main()
