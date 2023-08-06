import os
import gdown
import torch
import  cv2
import numpy as np
from ultralytics import YOLO

import downloadweights

# Load a model
model = YOLO('best_test_platform_elas.pt')  # load a custom model

# Predict with the model

def background(img):
	results = model(img)  # predict on an image
	image = cv2.imread('1.jpg',0)
	# print("shape of image",image.shape)

	for result in results:
	    # get array results
		image = cv2.imread('1.jpg')
		image = cv2.resize(image, (512, 384))
		masks = result.masks.masks
		masks1=masks.cpu().numpy()
		masks1 = cv2.resize(masks1, (988, 1344))
		masks1 = np.expand_dims(masks1, axis=-1)
		boxes = result.boxes.boxes  
		clss = boxes[:, 5]  # get indices of results where class is 0 (people in COCO)
		part_indices = torch.where(clss == 0)  
		part_masks = masks[part_indices] # use these indices to extract the relevant masks

		part_mask = torch.any(part_masks, dim=0).int() * 255 # scale for visualizing results #foreground mask
		# save to file
		cv2.imwrite('merged_segs.jpg', part_mask.cpu().numpy())
		im = cv2.imread("merged_segs.jpg",0)
		dest_not1 = cv2.bitwise_not(im, mask = None)

		part_mask = [part_mask.cpu().numpy()]
		part_mask = np.array(part_mask)
		part_mask = np.moveaxis(part_mask, 0, -1)
		part_mask = part_mask.astype(bool)

		background_mask = np.abs(1-part_mask)
		background_mask = np.concatenate([background_mask, background_mask, background_mask], axis=-1)
		masked_photo = image * part_mask

		background_mask = background_mask * [238, 221, 130]
		final_photo = masked_photo + background_mask
		cv2.imwrite(f"finallyhopefully.png", final_photo)
		# cv2.imwrite(f"outpt1.png", image * part_mask.cpu().numpy())



# if __name__ == '__main__':
# 	background('1.jpg')


