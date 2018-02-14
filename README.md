# Vision Processing Tool / QGIS: setup

Hey!

So, you want to use the Kainos computer vision tool to do some detection in your satellite images? Great! Let me help you get setup.

If you get stuck, feel free to grab Jordan McDonald (He will be floating around) to get some help.


## Pre-requisites

1. Download Oracle Virtualbox and its extension from [here](https://www.virtualbox.org/wiki/Downloads) 

      a. This will host our virtual machine (so you don&#39;t have to deal with pesky dependencies!) 
      
      b. Go ahead and install it (should be pretty straight forward!)
      
2. Once you have it installed, download the Virtual machine image from here - ADD HERE.

3. Download QGIS from [here] (https://qgis.org/en/site/forusers/download.html)

      a. This is for viewing and cropping the dataset (recommended to do this outside the VM to avoid memory / storage issues)

4. Download the Airbus dataset from here - ADD HERE

      a. As mentioned above its recommended to do your dataset processing outside of the VM
      
      b. You can upload a processed dataset to the likes and Google drive and then download in the VM when you need the tool.
      
      c. Inside the dataset is a read me describing the strcture of the data - each image is connected to an XML file which           contains the coordinate information - they come as a pair, so keep the images and XML together.


Once you have all these things downloaded, lets focus on getting each of them setup - if you are confident in handling python dependencies feel free to ignore using the virtual machine and clone this repository directly.

## Installing the virtual machine

This section will take you through installing the virtual machine which will host the Kainos vision processing tool (good option if you are not familiar with handling Python dependencies)

1. Open VirtualBox

2. Open the image with Virtual Box 

      a. File – Import Appliance – then select your downloaded VM
      
      ![](https://i.imgur.com/VM8tRFP.png)
      
      b. Hit 'Continue' and then 'Import'
      
      c. Double click on the new appliance to start the VM - a new option in the VirtualBox list.
  

4. Log in using the password &#39;machinelearning&#39;

      a. It might be slow loading the login page.
      
5. The first thing you need to do in the virtual machine is set up your ssh key for your github account. Here&#39;s how to [generate the key](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/) and [add it to your account](https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/)
      
      a. Or you can do it any other way your familiar with!
      
6. Now that that&#39;s set up you can clone the repo into the virtual machine (in the command line!)

      a. &#39;git clone https://github.com/KainosSoftwareLtd/vision-processing-web-tool.git&#39'

_Like magic, you have the tool on your virtual machine!_

## Installing QGIS

QGIS is a great tool for loading the airbus dataset and performing the processing required to chop the data into a format that can be used for machine learning classification tasks.

**MAC**

1. from the QGIS download page it will redirect you to another web page where you can download the tool.

      ![](https://github.com/KainosSoftwareLtd/vision-processing-web-tool/blob/master/Screen%20Shot%202018-02-14%20at%2016.47.24.png)

2. Double click on the download file - this folder will be opened.

      ![](https://github.com/KainosSoftwareLtd/vision-processing-web-tool/blob/master/Screen%20Shot%202018-02-14%20at%2016.50.52.png)
      
3. Add more here...

MORE TO ADD

**Windows**

1. For Window it seems to be a fair bit simpler - it provides a few installers - select whatever one you feel is appropriate, typically this is the 64bit installer.


Hooray! you are now able to open any of the images in the space dataset and start creating your dataset! Ask Jordan McDonald if you need any help :)


At this stage an assumption will be made that you have the repository cloned in whatever permutation you prefer (VM / no VM)

## Project Setup

1. With the repo cloned you&#39;ll need to change directory into vision-processing-web-tool
2. Set up a virtual environment to work in using the command &#39;virtualenv vision-processing&#39; in the terminal.
3. activate the virtual environment (see read me in foler if unsure)
4. Change directory into web-app and run &#39;pip install –r requirements.txt&#39;
  
      a. This grabs our dependencies
  
5. Once that&#39;s done you can run the app with &#39;python app.py&#39;
6. I&#39;d recommend downloading chromium to view the web app
7. On your browser of choice go to localhost:5000 to get to the web app
8. After you&#39;ve opened the web app you can select images, tag them and train your own machine learning model and test it yourself!

**Adding data**

- Get the dataset you want to use in the virtual machine
- From there you can upload them on the website to append them
- However, if you need to add a lot of images at once put them in the directory /web-app/static/images/uploads/untagged

**Note: The base dataset we provide can ONLY be opened in QGIS - ask Jordan for guidance is unsure**

**How to chop a large satelite image into a dataset:**

Download QGIS -> https://qgis.org/en/site/forusers/download.html

1. Load your image into QGIS

!["How to open a satellite image"](https://github.com/KainosSoftwareLtd/vision-processing-web-tool/blob/master/Screen%20Shot%202018-02-13%20at%2009.15.48.png?raw=true)

2. On the tool bar click on Raster - extraction - clipper.

3. Change the output file format to be a jpeg 2000 - drag your selection on the map itself and click okay when satisfied - this will split the larger image into one chip which can be used as part of a dataset.

!["How to crop a satellite image"](https://github.com/KainosSoftwareLtd/vision-processing-web-tool/blob/master/Screen%20Shot%202018-02-13%20at%2009.24.07.png?raw=true)

**Tips**
1. Make sure your images have different names - we use the name as an ID!
2. To 'reset' and delete all the images / tags you will need delete the named tags (not the untagged folder) in these directories.

- webapp/static/images/uploads
- webapp/tensorflow_images/master
- webapp/tensorflow_images/split/training
- webapp/tensorflow_images/split/validation

The images when trained will be split in training and validation sets.

3. If you want to change the tool, please create a new branch and dont merge into master (keep this clean for everyones benefit)
4. If you dont need the VM / have experience handling python depedencies, feel free not to use it! :)
5. machine-learning.py is where you can tweak the key ML components (epochs etc)
6. the algorithm chosen is a 'binary_crossentropy' so if using > 2 labels - then switch this to something suited to this.
7. ensure you change the 'settings.py' files size inputs to be as close as possible to the input (while maintaining a square)
8. In preprocessing we rescale inputs to between 0-1 for all pixel values - this is a great explanation why its useful - https://www.linkedin.com/pulse/keras-image-preprocessing-scaling-pixels-training-adwin-jahn/
9. Keras handles the CNN part of the code - if you see some weird quirks, please do upgrade using pip in the venv.
10. I recommend using QGIS outside of the VM to avoid loading large images into memory - leverage the VM as a means to use the vision processing tool.
