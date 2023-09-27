# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
IMAGE_EXT = [".jpg", ".jpeg", ".webp", ".bmp", ".png"]

class UNDISTORTION_IMG: 
    def __init__(self,path):
        # camera parameters
        cam_param = []
        with open(path, 'r') as f:
            data = f.readlines()
            for content in data:
                content_str = content.split()
                for compo in content_str:
                    cam_param.append(float(compo))
        self.camera_matrix = np.array([[cam_param[0], cam_param[1], cam_param[2]], 
                                        [cam_param[3], cam_param[4], cam_param[5]], 
                                        [cam_param[6], cam_param[7], cam_param[8]]])
        self.dist_coeffs = np.array([[cam_param[9]], [cam_param[10]], [cam_param[11]], [cam_param[12]]])
        self.no_init = False

    def distortion_img(self, img):
        if not self.no_init:
            mapx, mapy = cv2.initUndistortRectifyMap(self.camera_matrix,self.dist_coeffs, None,self.camera_matrix, img.shape[1::-1], 5)
            self.no_init = True
            
        img_msg = cv2.remap(img, mapx, mapy, interpolation=cv2.INTER_LINEAR)
        return img_msg

def get_image_list(path):
    image_names = []
    for maindir, subdir, file_name_list in os.walk(path):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            ext = os.path.splitext(apath)[1]
            if ext in IMAGE_EXT:
                image_names.append(apath)
    return image_names

def mkdir(dir):
    if(not os.path.exists(dir)):
        os.makedirs(dir)

def main(img_list, undis_img, save_dir):
    for img_msg in img_list:
        img_name = img_msg.split(os.sep)[-1]
        dist_img = undis_img.distortion_img(cv2.imread(img_msg))
        cv2.imwrite(save_dir + os.sep + img_name, dist_img)

if __name__ == '__main__':
    img_dir = './raw/'
    img_list = sorted(get_image_list(img_dir))

    intrinsic_dir = './param/r120.txt'
    undis_img = UNDISTORTION_IMG(intrinsic_dir)

    save_dir = './dis_d/'
    mkdir(save_dir)
    
    main(img_list, undis_img, save_dir)
