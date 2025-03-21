import cv2
import os


def create_video():

    imgs_path = './data/'
    output_path = './output/result.mp4'
    

    pre_imgs = sorted([f for f in os.listdir(imgs_path) if f.endswith(('.png', '.jpg', '.jpeg'))])
    #print(pre_imgs)
    img = []
    for i in pre_imgs:
        i = imgs_path + i
        img.append(i)


    # vid writer, get dimesnions
    cv2_fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    frame = cv2.imread(img[0])
    size = list(frame.shape)[:2]
    size.reverse()

    video = cv2.VideoWriter(output_path, cv2_fourcc, 30, size)

    for path in pre_imgs:
        frame = cv2.imread("data/" + path)
        if frame is None:
            continue
        video.write(frame)
    
    video.release()


