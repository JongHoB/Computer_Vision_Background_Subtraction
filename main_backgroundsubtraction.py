import numpy as np
import cv2 as cv
import os
import evaluation as eval
from collections import deque
###############################################################
##### This code has been tested in Python 3.6 environment #####
###############################################################

def main():

		##### Set threshold
		threshold = 30

		##### Set path
		input_path = './input_image'    # input path
		gt_path = './groundtruth'       # groundtruth path
		result_path = './result'        # result path

		##### load input
		input = [img for img in sorted(os.listdir(input_path)) if img.endswith(".jpg")]

		##### first frame and first background
		frame_current = cv.imread(os.path.join(input_path, input[0]))
		frame_current_gray = cv.cvtColor(frame_current, cv.COLOR_BGR2GRAY).astype(np.float64)
		frame_prev_gray = frame_current_gray

		##### Set learning rate of the background
		alpha=0.75
		# small alpha 1 to 0.0001
		
		###deque for previous images
		deq=deque(maxlen=70)
		deq.append(frame_current_gray)

		##Close kernel
		close_kernel=np.ones((11,11),np.uint8)

		##### background substraction
		for image_idx in range(len(input)):

			### Median of previous images
			background_model_prev=np.median(deq,axis=0).astype(np.float64)

			##### Adaptive B/F Detection
			background_model_current=(1-alpha)*background_model_prev+alpha*frame_prev_gray

			##### calculate foreground region
			diff = frame_current_gray-background_model_current
			diff_abs = np.abs(diff).astype(np.float64)

			##### make mask by applying threshold
			frame_diff = np.where(diff_abs > threshold, 1.0, 0.0)



			##### apply mask to current frame
			current_gray_masked = np.multiply(frame_current_gray, frame_diff)
			current_gray_masked_mk2 = np.where(current_gray_masked > 0, 255.0, 0.0)

			##### final result
			result = current_gray_masked_mk2.astype(np.uint8)
			#cv.imshow('result', result) # colab does not support cv.imshow

			result=cv.morphologyEx(result,cv.MORPH_CLOSE,close_kernel,iterations=1)

			##### renew background
			frame_prev_gray = frame_current_gray	

			##### make result file
			##### Please don't modify path
			cv.imwrite(os.path.join(result_path, 'result%06d.png' % (image_idx + 1)), result)

			##### end of input
			if image_idx == len(input) - 1:
				break

			##### read next frame
			frame_current = cv.imread(os.path.join(input_path, input[image_idx + 1]))
			frame_current_gray = cv.cvtColor(frame_current, cv.COLOR_BGR2GRAY).astype(np.float64)
			deq.append(frame_current_gray)

			##### If you want to stop, press ESC key
			k = cv.waitKey(30) & 0xff
			if k == 27:
				break

		##### evaluation result
		eval.cal_result(gt_path, result_path)


if __name__ == '__main__':
	main()

