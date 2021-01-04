# Detect scene attribute
# PlacesCNN to predict the scene category, attribute, and class activation map in a single pass


# Importing packages
import torch
from torch.autograd import Variable as V
from torchvision import transforms as trn
from torch.nn import functional as F
import os
import numpy as np
import cv2
from PIL import Image
import urllib.request


tmp_path = os.path.abspath('..').replace('\\', '/')

# Download files needed with URL
def get_resource_by_url(file_path):
    folder_path = os.path.dirname(file_path)
    filename = os.path.split(file_path)[-1]
    with open(file_path, 'r') as f:
        lines = f.readlines()
        url_list = []
        for line in lines:
            url_list.append(line.strip('\n'))
        path_tmp = folder_path + "/{}"
        foldername = path_tmp.format(filename.split('.')[0])

    if not os.path.exists(foldername):
        os.makedirs(foldername)
    for url in url_list:
        print("Try downloading file: {}".format(url))
        filename = url.split('/')[-1]
        filepath = foldername + '/' + filename
        if os.path.exists(filepath):
            print("File have already exist. skip")
        else:
            try:
                urllib.request.urlretrieve(url, filename=filepath)
            except Exception as e:
                print("Error occurred when downloading file, error message:")
                print(e)
    return foldername


# download files
file_path = tmp_path + '/IngTagging/New_Tags/resource.txt'
folder_path = get_resource_by_url(file_path)


def load_labels():
    # prepare all the labels
    # scene category relevant

    file_name_category = folder_path + '/categories_places365.txt'
    classes = list()
    with open(file_name_category) as class_file:
        for line in class_file:
            classes.append(line.strip().split(' ')[0][3:])
    classes = tuple(classes)

    # type of environment - IO prediction
    file_name_IO = folder_path + '/IO_places365.txt'
    with open(file_name_IO) as f:
        lines = f.readlines()
        labels_IO = []
        for line in lines:
            items = line.rstrip().split()
            labels_IO.append(int(items[-1]) -1) # 0 is inside, 1 is outside
    labels_IO = np.array(labels_IO)

    # scene attribute relevant
    file_name_attribute = folder_path + '/labels_sunattribute.txt'
    with open(file_name_attribute) as f:
        lines = f.readlines()
        labels_attribute = [item.rstrip() for item in lines]

    file_name_W = folder_path + '/W_sceneattribute_wideresnet18.npy'
    W_attribute = np.load(file_name_W)

    return classes, labels_IO, labels_attribute, W_attribute


def hook_feature(module, input, output):
    features_blobs.append(np.squeeze(output.data.cpu().numpy()))


def returnCAM(feature_conv, weight_softmax, class_idx):

    # generate the class activation maps upsample to 256x256
    size_upsample = (256, 256)
    nc, h, w = feature_conv.shape
    output_cam = []
    for idx in class_idx:
        cam = weight_softmax[class_idx].dot(feature_conv.reshape((nc, h*w)))
        cam = cam.reshape(h, w)
        cam = cam - np.min(cam)
        cam_img = cam / np.max(cam)
        cam_img = np.uint8(255 * cam_img)
        output_cam.append(cv2.resize(cam_img, size_upsample))
    return output_cam


def returnTF():
# load the image transformer
    tf = trn.Compose([
        trn.Resize((224,224)),
        trn.ToTensor(),
        trn.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    return tf


def load_model():
    # this model has a last conv feature map as 14x14

    model_file = folder_path + '/wideresnet18_places365.pth.tar'
    file_wideresnet = folder_path + '/wideresnet.py'

    from New_Tags.resource import wideresnet
    model = wideresnet.resnet18(num_classes=365)
    checkpoint = torch.load(model_file, map_location=lambda storage, loc: storage)
    state_dict = {str.replace(k,'module.',''): v for k,v in checkpoint['state_dict'].items()}
    model.load_state_dict(state_dict)
    model.eval()

    # hook the feature extractor
    features_names = ['layer4','avgpool'] # this is the last conv layer of the resnet
    for name in features_names:
        model._modules.get(name).register_forward_hook(hook_feature)
    return model


def get_folder_path():
    return folder_path


def test_S_ME(image_path):

    global result_S_ME,features_blobs, model
    result_S_ME = []

    # load the labels
    classes, labels_IO, labels_attribute, W_attribute = load_labels()

    # load the model
    features_blobs = []
    model = load_model()

    # load the transformer
    tf = returnTF()  # image transformer

    # get the softmax weight
    params = list(model.parameters())
    weight_softmax = params[-2].data.numpy()
    weight_softmax[weight_softmax < 0] = 0

    # load the test image
    img = Image.open(image_path)
    input_img = V(tf(img).unsqueeze(0))

    # forward pass
    logit = model.forward(input_img)
    h_x = F.softmax(logit, 1).data.squeeze()
    probs, idx = h_x.sort(0, True)
    probs = probs.numpy()
    idx = idx.numpy()

    list_0 = image_path

    # output the IO prediction
    list_1 = []
    io_image = np.mean(labels_IO[idx[:10]]) # vote for the indoor or outdoor
    if io_image < 0.5:
        list_1.append("inside")
    else:
        list_1.append("outside")

    # output the prediction of scene category
    list_2 = []
    for i in range(0, 5):
        list_tmp = ['beauty_salon','house']
        if classes[idx[i]] in list_tmp or probs[i] >= 0.08:
            list_2.append(classes[idx[i]])

    # output the scene attributes
    responses_attribute = W_attribute.dot(features_blobs[1])
    idx_a = np.argsort(responses_attribute)
    for i in range(-1,-10,-1):
        list_2.append(labels_attribute[idx_a[i]])

    # generate class activation mapping
    CAMs = returnCAM(features_blobs[0], weight_softmax, [idx[0]])

    # Uncomment these lines below to generate and show the img with the informative region for predicting the category
    # # render the CAM and output
    # img = cv2.imread(image_path)
    # height, width, _ = img.shape
    # heatmap = cv2.applyColorMap(cv2.resize(CAMs[0],(width, height)), cv2.COLORMAP_JET)
    # result = heatmap * 0.4 + img * 0.5
    # Informative_region_img = image_path.split('.')[0] + '_SceneRegion.jpg'
    # cv2.imwrite(Informative_region_img, result)
    # img = cv2.imread(Informative_region_img)
    # cv2.imshow("show", img)

    snow_list = ['snow','mountain_snowy']
    ski_list = ['ski_slope']

    nature_list = ['natural']  # + outside
    city_list = ['cities','canal/urban','downtown','skyscraper','harbor','crosswalk','bus_station/indoor','street']  # + outside

    face_list = ['beauty_salon','arena/performance']

    sky_comb = ['natural light','sunny']  # + blue
    sky_list = ['clouds','sky','skyscraper']
    sun_list = []  # ????????
    house_comb = ['artists_loft']  # + inside
    house_list = ['house','cabins','manufactured_home','oast_house','courthouse','embassy','inn/outdoor','beach_house']
    tree_list = ['trees','forest']
    sea_list = ['canal/urban','canal/natural','ocean','coast','wave','beach','lagoon']
    water_list = ['still water']
    moutrain_list = ['mountains','hills','butte','mountain_snowy']

    list_1_in = []
    list_1_in.append(list_1[0])
    list_2_in = []
    list_3_in = []
    sky_num = 0
    for attr in list_2:
        if 'outside' in list_1:
            if attr in nature_list:
                list_1_in.append("nature")
            if attr in city_list:
                list_1_in.append("city")

        if attr in snow_list:
            list_2_in.append("snow")
        if attr in sky_comb:
            sky_num = sky_num + 1
        if attr in sky_list:
            list_2_in.append("sky")
        if attr in sun_list:
            list_2_in.append("sun")
        if 'inside' in list_1 and (attr in house_comb):
            list_2_in.append("house")
        if attr in house_list:
            list_2_in.append("house")
        if attr in tree_list:
            list_2_in.append("tree")
        if attr in sea_list:
            list_2_in.append("sea")
        if attr in water_list:
            list_2_in.append("water")
        if attr in moutrain_list:
            list_2_in.append("moutrain")

        if attr in ski_list:
            list_3_in.append("ski")
        if attr in face_list:
            list_3_in.append("face")

    if "sky" in list_2_in:
        pass
    elif sky_num == 2:
        list_2_in.append("sky_comb")

    result_S_ME.append(list_0)
    result_S_ME.append(list(set(list_1_in)))
    result_S_ME.append(list(set(list_2_in)))
    result_S_ME.append(list(set(list_3_in)))

    return result_S_ME