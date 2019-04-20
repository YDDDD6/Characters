from PIL import Image

file = "./result/1.png"

image = Image.open(file)
width, height = image.size

fh = open('1.txt', 'w')
for i in range(height):
    for j in range(width):
        #获取像素点颜色
        color=image.getpixel((j,i))
        colorsum=color[0]+color[1]+color[2]
        if(colorsum == 0):
            fh.write('1')
        else:
            fh.write('0')
    fh.write('\n')
fh.close()
