from PIL import Image
import os
import cv2
import numpy as np


class PictureToMartix:
    """实现图片根据字符分割，并挨个以01矩阵的形式保存"""
    def __init__(self, file):
        self.base_dir = "./origin/"
        self.dst_dir = "./result/"
        self.martix_dir = "./martix/"
        self.min_val = 10
        self.min_range = 19
        self.count = 0
        self.image = cv2.imread(file)

    def extract_peek(self, array_vals, minimun_val, minimun_range):
        start_i = None
        end_i = None
        peek_ranges = []
        for i, val in enumerate(array_vals):
            if val > minimun_val and start_i is None:
                start_i = i
            elif val > minimun_val and start_i is not None:
                pass
            elif val < minimun_val and start_i is not None:
                if i - start_i >= minimun_range:
                    end_i = i
                    # print(end_i - start_i)
                    peek_ranges.append((start_i, end_i))
                    start_i = None
                    end_i = None
            elif val < minimun_val and start_i is None:
                pass
            else:
                raise ValueError("cannot parse this case...")
        return peek_ranges

    def cutImage(self, img, peek_range, peek_ranges, vertical_peek_ranges2d, dst_dir, count):
        # global count
        for i, peek_range in enumerate(peek_ranges):
            for vertical_range in vertical_peek_ranges2d[i]:
                x = vertical_range[0]
                y = peek_range[0]
                w = vertical_range[1] - x
                h = peek_range[1] - y
                pt1 = (x, y)
                pt2 = (x + w, y + h)
                count += 1
                img1 = img[y:peek_range[1], x:vertical_range[1]]
                new_shape = (150, 150)
                img1 = cv2.resize(img1, new_shape)
                cv2.imwrite(dst_dir + str(count) + ".png", img1)
                # cv2.rectangle(img, pt1, pt2, color)

    def runCut(self, base_dir, min_val, min_range):
        for fileName in os.listdir(base_dir):
            img = cv2.imread(base_dir + fileName)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                                       cv2.THRESH_BINARY_INV, 11, 2)
            horizontal_sum = np.sum(adaptive_threshold, axis=1)
            peek_ranges = self.extract_peek(horizontal_sum, self.min_val, self.min_range)
            line_seg_adaptive_threshold = np.copy(adaptive_threshold)
            for i, peek_range in enumerate(peek_ranges):
                x = 0
                y = peek_range[0]
                w = line_seg_adaptive_threshold.shape[1]
                h = peek_range[1] - y
                pt1 = (x, y)
                pt2 = (x + w, y + h)
                cv2.rectangle(line_seg_adaptive_threshold, pt1, pt2, 255)
            vertical_peek_ranges2d = []
            for peek_range in peek_ranges:
                start_y = peek_range[0]
                end_y = peek_range[1]
                line_img = adaptive_threshold[start_y:end_y, :]
                vertical_sum = np.sum(line_img, axis=0)
                vertical_peek_ranges = self.extract_peek(
                    vertical_sum, min_val, min_range)
                vertical_peek_ranges2d.append(vertical_peek_ranges)
            self.cutImage(img, peek_range, peek_ranges, vertical_peek_ranges2d, self.dst_dir, 0)

    def chartomartix(self):
        namelist = os.listdir(self.dst_dir)
        for name in namelist:
            order, other = name.split('.')
            image = Image.open(self.dst_dir+name)
            fh = open(self.martix_dir+str(order)+'.txt', 'w')
            width, height = image.size
            for i in range(width):
                for j in range(height):
                    color = image.getpixel((j, i))
                    if (color[0] + color[1] + color[2] < 150*3):
                        fh.write('1')
                    else:
                        fh.write('0')
                fh.write('\n')
            fh.close()

