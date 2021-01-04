# Get new tags


# Importing packages
from New_Tags import Colors, Scene_Main_Elements_1_2, ImgConvert, Main_Elements_1, Quality, Complexity


def new_detect(file_path):
    list_0_path = []
    list_1_colors = []
    list_2_scene = []
    list_3_ME1 = []
    list_4_ME2 = []
    list_5_quality = []
    list_6_complexity = []
    result_S_ME = []
    global new_keywords
    new_keywords = ''

    # 00 file path
    list_0_path.append(file_path)

    print("---------------------------------------------")
    print("Image: ", file_path)

    # 01 colors
    list_1_colors = list_1_colors + Colors.get_color(file_path)

    # 02 scene
    file_path_tmp = file_path
    file_path = ImgConvert.convertPNGtoJPG(file_path)
    result_S_ME = result_S_ME + Scene_Main_Elements_1_2.test_S_ME(file_path)
    file_path = ImgConvert.deletePNG_JPG(file_path_tmp)
    list_2_scene = list_2_scene + result_S_ME[1]

    # 03 Main elements 1
    folder_path = Scene_Main_Elements_1_2.get_folder_path()
    result_ME1 = Main_Elements_1.test_ME(file_path, folder_path)
    if 'face' in result_S_ME[3] and 'human' in result_ME1:
        result_ME1.remove('human')
    list_3_ME1 = list_3_ME1 + result_ME1 + result_S_ME[3]
    print("list_3_ME1: ", list_3_ME1)

    # 04 Main elements 2
    if 'sky_comb' in result_S_ME[2]:
        if 'blue' in list_1_colors:
            result_S_ME[2].remove('sky_comb')
            result_S_ME[2].append('sky')
        else:
            result_S_ME[2].remove('sky_comb')
    list_4_ME2 = list_4_ME2 + result_S_ME[2]
    print("list_4_ME2: ", list_4_ME2)

    # 05 quality
    imageVar = Quality.getImageVar(file_path)
    sharpness = list(set(Quality.getSharpness(imageVar)))
    darkness = list(set(Quality.getBlackPiex(file_path)))
    list_5_quality = list_5_quality + sharpness + darkness

    # 06 complexity
    complexity = list(set(Complexity.getComplexity()))
    list_6_complexity = list_6_complexity + complexity

    new_keywords = list_1_colors + list_2_scene + list_3_ME1 + list_4_ME2 + list_5_quality + list_6_complexity
    print("New_tags: ", new_keywords)

    return new_keywords