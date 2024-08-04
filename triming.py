import os
import numpy as np
from PIL import Image

def find_golden_border(image_path):
    image = Image.open(image_path).convert('RGBA')  # RGBAに変換
    img_array = np.array(image)
    
    lower_golden = np.array([180, 140, 0, 255])
    upper_golden = np.array([255, 210, 100, 255])
    
    # RGBAでマスクを作成
    mask = np.all(np.logical_and(img_array >= lower_golden, img_array <= upper_golden), axis=-1)

    coords = np.argwhere(mask)
    if coords.size == 0:
        raise ValueError("Golden border not found in the image.")
    
    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0)

    padding = 1  # paddingを整数に変更
    x0 = max(0, x0 - padding + 1)
    y0 = max(0, y0 - padding + 2)
    x1 = min(img_array.shape[1], x1 + padding + 1)
    y1 = min(img_array.shape[0], y1 + padding)

    return (x0, y0, x1, y1)

def trim_color_paper(image_path, output_path):
    bbox = find_golden_border(image_path)
    image = Image.open(image_path)  # ここで画像を一度だけ開く
    trimmed_image = image.crop(bbox)
    trimmed_image.save(output_path)

def batch_process_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
            input_image_path = os.path.join(input_folder, filename)
            output_image_path = os.path.join(output_folder, filename)
            trim_color_paper(input_image_path, output_image_path)

input_folder_path = "./input_folder"
output_folder_path = "./output_folder"
batch_process_images(input_folder_path, output_folder_path)
