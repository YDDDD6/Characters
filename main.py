import picture_to_matrix

pm = picture_to_matrix.PictureToMartix('./origin/demo.bmp')
num = pm.runCut(pm.base_dir, pm.min_val, pm.min_range)  # 得到生成图片数量
pm.chartomartix()
