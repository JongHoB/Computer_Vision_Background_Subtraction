## Background_Subtraction

### Notice

#### Main Algorithm

- Baseline method is made by Adaptive Background and Foreground Detection

<img width="500" alt="image" src="https://github.com/JongHoB/Computer_Vision_Background_Subtraction/assets/78012131/f3bf7f3b-c83e-4073-afc2-4e05113d5631">

(1) f_i: current frame (ith frame)

(2) μ_i: background image (ith frame)

(3) Adapted Background is made by  

<img width="236" alt="image" src="https://github.com/JongHoB/Computer_Vision_Background_Subtraction/assets/78012131/fba975a8-a450-4246-bfdc-d593bee37cf8">

(4) <img width="110" alt="image" src="https://github.com/JongHoB/Computer_Vision_Background_Subtraction/assets/78012131/678b7fdf-555a-4cac-b6e6-74dadf8a38f0"> : difference image (or difference image between the current frame and the designed background)

(5) <img width="110" alt="image" src="https://github.com/JongHoB/Computer_Vision_Background_Subtraction/assets/78012131/eed2abd5-e8ea-4dc1-99c5-a445e3a837a9"> : Binarized image compared with threshold

- The above-mentioned method will be recursively executed.

- You will have the following images
  - Groundtruth: The true moving objects images

    (From 1 to 469 frames, there is no GT because you need some time for adapting the background models)
  
    ** GT image consists of black(background), white(foreground), and gray(shadow or boundary)

    ** In this assignment, **we only use black and white (Don’t use other pixel values) regions**

    <img width="150" alt="image" src="https://github.com/JongHoB/Computer_Vision_Background_Subtraction/assets/78012131/1673b589-cff7-4080-8935-59d503ae3774">

  - input_image: from 1 to 1700 frames

    <img width="150" alt="image" src="https://github.com/JongHoB/Computer_Vision_Background_Subtraction/assets/78012131/fba3ad2c-4b01-425e-b5e9-9d7c70144eb1">

  - result: You should save your result images in this directory

    ** Foreground is white and background is black

    <img width="150" alt="image" src="https://github.com/JongHoB/Computer_Vision_Background_Subtraction/assets/78012131/ea040210-ac06-43a5-8486-b659a4c9c47e">


- Evaluation code is provided (Please, check the example code)
- The Baseline performance (made by TA) is recall: 78% and precision: 78%
- Provided frame difference makes recall: 44% and precision: 90% (This is not the baseline!)
  - https://en.wikipedia.org/wiki/Precision_and_recall

#### Constraints
- Don’t use opencv backgroundMOG function simply. If you want to make more advanced background estimation method, please, implement it by yourself. 
- The baseline method is the “mentioned B/F detection” and you can improve them using different parameters (alpha and threshold) or the method you implement by yourself. 
- Use small alpha. Change it from 1 to 0.001 and check the outputs according to the different alpha values.  


---

### Result


<img width="800" alt="image" src="https://github.com/JongHoB/Computer_Vision_Background_Subtraction/assets/78012131/817da207-89c8-4a3b-b409-33484b416d29">

The final performance was 95.251% for Recall and 94.694% for Precision.

- Before
  
In the case of the previously provided code, 
the model using **frame difference** compares only the current frame and the existing frame to obtain a foreground. 

At this time, if the background is regarded as an existing frame, it is not a constant background,
but an irregular background that keeps changing is pulled out, so the result is not good.

- Basis
  
After that, when I used the **Adaptive B/F detection**, 
I thought I should use a median filter for many existing frames because the background model was strong against changes in vehicles or leaves, 

In order to increase **Precision**, 
I tried to increase the threshold value because I had to lower the non-correct part. 

In order to increase **Recall**, I need to reduce false negatives.
To create as many areas as possible that are correct, there should be no empty parts in the painted area of the car.

- Methods
  
For up to 70 previable images, 
a **medium filter** was used to obtain an image that is resistant to change, 

and since you shouldn't stay too long, 
the adaptive background model was created using the previous frame. 

At the same time, I increased the **threshold value** to increase Precision. 

In the case of area coloring, the parts separated between pixels were connected using **the closing technique** that the professor mentioned briefly in class. 

As the size of the kernel used in closing increases, more connections will be possible, 
so I tried to increase the size as much as possible. 

Therefore, the learning rate of **the background model calculation is 0.75, the threshold is 32, and the closing kernel is 13*13.**

