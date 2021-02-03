import numpy as np
import cv2 as cv
import argparse
import os

global net


def Load_model():
    path = os.getcwd()
    # Specify the paths for the 2 model files
    protoFile = os.path.join(path, "mylibtest/colorization/models/colorization_deploy_v2.prototxt")
    weightsFile = os.path.join(path, "mylibtest/colorization/models/colorization_release_v2.caffemodel")

    # Load the cluster centers
    pts_in_hull = np.load(os.path.join(path, 'mylibtest/colorization/pts_in_hull.npy'))

    # Read the network into Memory
    global net
    net = cv.dnn.readNetFromCaffe(protoFile, weightsFile)

    # populate cluster centers as 1x1 convolution kernel
    pts_in_hull = pts_in_hull.transpose().reshape(2, 313, 1, 1)
    net.getLayer(net.getLayerId('class8_ab')).blobs = [pts_in_hull.astype(np.float32)]
    net.getLayer(net.getLayerId('conv8_313_rh')).blobs = [np.full([1, 313], 2.606, np.float32)]


def colorized_img(src=None, W_in=224, H_in=224):
    assert src is not None, "Image is None ...."
    img_rgb = (src[:,:,[2, 1, 0]] * 1.0 / 255).astype(np.float32)
    img_lab = cv.cvtColor(img_rgb, cv.COLOR_RGB2Lab)
    img_l = img_lab[:,:,0] # pull out L channel

    # resize lightness channel to network input size
    img_l_rs = cv.resize(img_l, (W_in, H_in)) #
    img_l_rs -= 50 # subtract 50 for mean-centering

    net.setInput(cv.dnn.blobFromImage(img_l_rs))
    ab_dec = net.forward()[0,:,:,:].transpose((1,2,0)) # this is our result

    (H_orig,W_orig) = img_rgb.shape[:2] # original image size
    ab_dec_us = cv.resize(ab_dec, (W_orig, H_orig))

    # concatenate with original image L
    img_lab_out = np.concatenate((img_l[:,:,np.newaxis],ab_dec_us),axis=2) 
    img_bgr_out = np.clip(cv.cvtColor(img_lab_out, cv.COLOR_Lab2BGR), 0, 1)

    return (img_bgr_out*255).astype(np.uint8)
