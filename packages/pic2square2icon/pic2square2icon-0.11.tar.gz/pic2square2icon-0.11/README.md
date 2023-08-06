# 2 functions that provide convenient and efficient ways to resize images to a square with custom backgrounds and convert images to the ICO format

## pip install pic2square2icon

### Tested against Windows 10 / Python 3.10 / Anaconda 

The functions resize_with_background and pic2ico can be used by developers or individuals who work with 
image processing or need to manipulate images for various purposes. Here are some potential use cases for each function:

### resize_with_background:

- Graphic designers who want to resize an image to a specific size (square) while maintaining its aspect ratio and adding a background

- Web developers who need to generate thumbnail images with a consistent size and background for their websites.
- Content creators who want to resize and add a background to their images for social media posts (instagram or facebook timeline) or presentations.


### pic2ico:

- Software developers who need to convert image files to the ICO (icon) format for use in applications or software interfaces.
- Designers who want to create custom icons from their existing image assets.
- System administrators or IT professionals who need to generate ICO files for use as desktop icons or shortcuts.



```python

from pic2square2icon import resize_with_background, pic2ico
import cv2

test = 1
fg = r"C:\test\fg.png"
bg = r"C:\test\bg.png"
target_size = 512
resized_image = resize_with_background(fg, target_size, bg)
pic2ico(src=resized_image, dst=rf"C:\test\{test}.ico")
resized_image.save(rf"C:\test\{test}.png")


test = 2
fg = r"C:\test\fg.png"
bg = "orange"
target_size = 512
resized_image = resize_with_background(fg, target_size, bg)
pic2ico(src=resized_image, dst=rf"C:\test\{test}.ico")
resized_image.save(rf"C:\test\{test}.png")

test = 3
fg = r"C:\test\fg.png"
bg = (255, 255, 0)
target_size = 512
resized_image = resize_with_background(fg, target_size, bg)
pic2ico(src=resized_image, dst=rf"C:\test\{test}.ico")
resized_image.save(rf"C:\test\{test}.png")

test = 4
fg = r"C:\test\bg.png"
bg = cv2.imread(r"C:\test\fg.png")
target_size = 512
resized_image = resize_with_background(fg, target_size, bg, background_ratio=2)
pic2ico(src=resized_image, dst=rf"C:\test\{test}.ico")
resized_image.save(rf"C:\test\{test}.png")

test = 5
fg = r"C:\test\fg.png"
bg = None
target_size = 512
resized_image = resize_with_background(fg, target_size, bg, background_ratio=2)
resized_image.save(rf"C:\test\{test}.png")
pic2ico(src=resized_image, dst=rf"C:\test\{test}.ico")

```



#### bg.png

![](https://github.com/hansalemaos/screenshots/blob/main/create_ico/bg.png?raw=true)



#### fg.png

![](https://github.com/hansalemaos/screenshots/blob/main/create_ico/fg.png?raw=true)



#### 1.png

![](https://github.com/hansalemaos/screenshots/blob/main/create_ico/1.png?raw=true)



#### 2.png

![](https://github.com/hansalemaos/screenshots/blob/main/create_ico/2.png?raw=true)



#### 3.png

![](https://github.com/hansalemaos/screenshots/blob/main/create_ico/3.png?raw=true)



#### 4.png

![](https://github.com/hansalemaos/screenshots/blob/main/create_ico/4.png?raw=true)


#### 5.png

![](https://github.com/hansalemaos/screenshots/blob/main/create_ico/5.png?raw=true)
