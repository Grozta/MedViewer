#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import time

from cv2 import cv2

from Operative.Module.seg_test2 import deal_single_image, operative_load_model

if __name__ == '__main__':
    path = r'film_frame.avi'
    t1 = time.time()
    model = operative_load_model()
    t2 = time.time()-t1
    print(f'load model cost:{t2} s')
    cap = cv2.VideoCapture(path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        t1 = time.time()
        seg_mask, origin_seg, seg = deal_single_image(model, frame)
        t2 = time.time() - t1
        print(f'cost:{t2} s')
        cv2.imshow('image', seg)
        k = cv2.waitKey(500)
        # q键退出
        if k & 0xff == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
