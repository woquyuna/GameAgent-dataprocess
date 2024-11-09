import cv2
import random
import numpy as np 



def img_argument(img_path, rx, ry, plot=False):
    scale_range = [0.4, 0.56]
    crop_ver_r_range = [0.9, 1.0]
    crop_hor_r_range = [0.88, 1.0]
    bound = 80
    # overall scale
    img = cv2.imdecode(np.fromfile(img_path,dtype=np.uint8),-1)
    # img = cv2.imread(img_path)
    H, W = img.shape[:2]
    if W < 1500:    # 小图不需要那么小的缩放比例
        scale_range = [2*x for x in scale_range]
    scale = random.uniform(scale_range[0], scale_range[1])
    img = cv2.resize(img, (int(scale * W), int(scale * H)))
    # 新的长宽
    H, W = img.shape[:2]
    # crop
    # box coordinates
    point_coord = [rx*W, ry*H]
    point_coord = [int(x) for x in point_coord]

    crop_hor_r = random.uniform(crop_hor_r_range[0], crop_hor_r_range[1])
    crop_ver_r = random.uniform(crop_ver_r_range[0], crop_ver_r_range[1])
    start_x = np.random.randint(0, W - int(W * crop_hor_r))
    start_x = min(point_coord[0] - bound, start_x)
    start_x = max(0, start_x)
    start_y = np.random.randint(0, H - int(H * crop_ver_r))
    start_y = min(point_coord[1] - bound, start_y)
    start_y = max(0, start_y)
    end_x = max(start_x + int(W*crop_hor_r), point_coord[0] + bound)
    end_x = min(W-1, end_x)
    end_y = max(start_y + int(H*crop_ver_r), point_coord[1] + bound)
    end_y = min(H-1, end_y)
    
    # crop image
    img = img[start_y:end_y, start_x:end_x]

    # adjust box coord after crop
    H_,W_ = img.shape[:2]
    point_coord[0] = max(0, point_coord[0] - start_x)
    point_coord[1] = max(0, point_coord[1] - start_y)

    if plot:
        cv2.circle(img, (int(point_coord[0]), int(point_coord[1])), 5, (0, 0, 255), -1)

    # convert to ratio
    point_coord[0] = point_coord[0]/W_
    point_coord[1] = point_coord[1]/H_


    return img, point_coord[0],point_coord[1]


def img_argument_center(img_path, rx=0.5, ry=0.5, plot=False):
    scale_range = [0.4, 0.56]
    crop_ver_r_range = [0.9, 1.0]
    crop_hor_r_range = [0.9, 1.0]
    bound = 80
    # overall scale
    img = cv2.imdecode(np.fromfile(img_path,dtype=np.uint8),-1)
    # img = cv2.imread(img_path)
    H, W = img.shape[:2]
    if W < 1500:    # 小图不需要那么小的缩放比例
        scale_range = [2*x for x in scale_range]
    scale = random.uniform(scale_range[0], scale_range[1])
    img = cv2.resize(img, (int(scale * W), int(scale * H)))
    # 新的长宽
    H, W = img.shape[:2]
    # crop
    # box coordinates
    point_coord = [rx*W, ry*H]
    point_coord = [int(x) for x in point_coord]

    crop_hor_r = random.uniform(crop_hor_r_range[0], crop_hor_r_range[1])
    crop_ver_r = random.uniform(crop_ver_r_range[0], crop_ver_r_range[1])
    start_x = np.random.randint(0, W - int(W * crop_hor_r))
    start_x = min(point_coord[0] - bound, start_x)
    start_x = max(0, start_x)
    start_y = np.random.randint(0, H - int(H * crop_ver_r))
    start_y = min(point_coord[1] - bound, start_y)
    start_y = max(0, start_y)
    end_x = max(start_x + int(W*crop_hor_r), point_coord[0] + bound)
    end_x = min(W-1, end_x)
    end_y = max(start_y + int(H*crop_ver_r), point_coord[1] + bound)
    end_y = min(H-1, end_y)
    
    # crop image
    img = img[start_y:end_y, start_x:end_x]

    # adjust box coord after crop
    H_,W_ = img.shape[:2]
    point_coord[0] = max(0, point_coord[0] - start_x)
    point_coord[1] = max(0, point_coord[1] - start_y)

    if plot:
        cv2.circle(img, (int(point_coord[0]), int(point_coord[1])), 5, (0, 0, 255), -1)

    # convert to ratio
    point_coord[0] = point_coord[0]/W_
    point_coord[1] = point_coord[1]/H_


    return img, point_coord[0],point_coord[1]


def img_argument_only_scale(img_path):
    scale_range = [0.4, 0.56]
    # overall scale
    img = cv2.imdecode(np.fromfile(img_path,dtype=np.uint8),-1)
    # img = cv2.imread(img_path)
    H, W = img.shape[:2]
    if W < 1500:    # 小图不需要那么小的缩放比例
        scale_range = [2*x for x in scale_range]
    scale = random.uniform(scale_range[0], scale_range[1])
    img = cv2.resize(img, (int(scale * W), int(scale * H)))
    return img


