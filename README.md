# Vision Processing Tool / QGIS: setup

Hey!

So, you want to use the Kainos computer vision tool to do some detection in your satellite images? Great! Let me help you get setup.

If you get stuck, feel free to grab Jordan McDonald (He will be floating around) to get some help.


## Pre-requisites

1. Download Oracle Virtualbox and its extension from [here](https://www.virtualbox.org/wiki/Downloads) 

      a. This will host our virtual machine (so you don&#39;t have to deal with pesky dependencies!) 
      
      b. Go ahead and install Virtual Box (should be pretty straight forward!)
      
2. Once you have Virtaul Box installed - lets install the extension! it lets you do extra things (full screen functionality, potential usb transfer and more)

      a. in Virtual Box navigate to preferences - select the extensions tab - hit the breen arrow and navigate to the downloaded extension pack.
      
      ![](https://github.com/KainosSoftwareLtd/vision-processing-web-tool/blob/master/Screen%20Shot%202018-02-15%20at%2012.47.48.png)
      
2. Once you have it installed, download the Virtual machine image from here - ADD HERE.

3. Download QGIS from [here] (https://qgis.org/en/site/forusers/download.html)

      a. This is for viewing and cropping the dataset (recommended to do this outside the VM to avoid memory / storage issues)

4. Download the Airbus dataset from here - ADD HERE

      a. As mentioned above its recommended to do your dataset processing outside of the VM (large images can stress system memory, particulary in a VM!)
      
      b. You can upload a processed dataset to the likes and Google drive and then download in the VM when you need the tool.
      
      c. Inside the dataset is a read me describing the structure of the data - each image is connected to an XML file which           contains the coordinate information - they come as a pair, so keep the images and XML together.


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
      
5. If you want to change the tool and upload to your own repository (currently you have read access only), there a few steps you will need to take (Otherwise skip this step!)

      a. Set up your ssh key for your github account. Here&#39;s how to [generate the key](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/) and [add it to your account](https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/)
      
      b. Or you can do it any other way your familiar with! 
      
6. Only do step six if your not using the VM (its already cloned!)

      a. Now that that&#39;s set up you can clone the repo into the virtual machine (in the command line!)

      b. &#39;git clone https://github.com/KainosSoftwareLtd/vision-processing-web-tool.git&#39'

_Like magic, you have the tool on your virtual machine!_

## Installing QGIS

QGIS is a great tool for loading the airbus dataset and performing the processing required to chop the data into a format that can be used for machine learning classification tasks.

**MAC**

1. from the QGIS download page it will redirect you to another web page where you can download the tool.

      ![](https://github.com/KainosSoftwareLtd/vision-processing-web-tool/blob/master/Screen%20Shot%202018-02-14%20at%2016.47.24.png)

2. Double click on the download file - this folder will be opened.

      ![](https://github.com/KainosSoftwareLtd/vision-processing-web-tool/blob/master/Screen%20Shot%202018-02-14%20at%2016.50.52.png)
      
3. Double click to run each of the installers, 1-4, in order one at a time.
      a. The installer will look like the image below - keep hititng continue / agree to proceed.
      
      ![](https://github.com/KainosSoftwareLtd/vision-processing-web-tool/blob/master/installs.png)

**Windows**

1. For Window it seems to be a fair bit simpler - it provides a few installers - select whatever one you feel is appropriate, typically this is the 64bit installer.

_Hooray! you are now able to open any of the images in the space dataset and start creating your dataset! Ask Jordan McDonald if you need any help :)_

## QGIS: Dataset Prep Basics

You can only open the space images with a tool like QGIS - previews wont work as the image will reference the XML file associated as a pair

1. Load your image into QGIS

!["How to open a satellite image"](https://github.com/KainosSoftwareLtd/vision-processing-web-tool/blob/master/Screen%20Shot%202018-02-13%20at%2009.15.48.png?raw=true)

2. On the tool bar click on Raster - extraction - clipper.

3. Change the output file format to be a jpeg 2000 - drag your selection on the map itself and click okay when satisfied - this will split the larger image into one chip which can be used as part of a dataset.

!["How to crop a satellite image"](https://github.com/KainosSoftwareLtd/vision-processing-web-tool/blob/master/Screen%20Shot%202018-02-13%20at%2009.24.07.png?raw=true)

## Project Setup

At this stage an assumption will be made that you have the repository cloned in whatever permutation you prefer (VM / no VM)

1. With the repo cloned you&#39;ll need to change directory into vision-processing-web-tool

      a.The repository is already cloned for you in the VM!

2. To setup - check out the 'setup.txt' file in the parent folder for the project - follow each step.

3. On your browser of choice go to localhost:5000 to get to the web app

      a. I recommend downloading chrome as the browser (most tested)

4. After you&#39;ve opened the web app you can select images, tag them and train your own machine learning model and test it yourself!

### Adding Data to the Tool

1. Ensure you have your dataset in a single folder.

2. Can you upload the data through the tool using the 'upload' functionality.

3. If you want to move a lot of images at once (or seeing upload issues) you can manually put them in the directory /web-app/static/images/uploads/untagged

**Tips**

1. Make sure your images have different names - we use the name as an ID (for the visoon too!

2. To 'reset' and delete all the images / tags you will need delete the named tag folders (not the untagged folder) in these directories.

- webapp/static/images/uploads
- webapp/tensorflow_images/master
- webapp/tensorflow_images/split/training
- webapp/tensorflow_images/split/validation

The images when trained will be split in training and validation sets.

4. machine-learning.py is where you can tweak the key ML components (epochs etc)

5. the algorithm chosen is a 'binary_crossentropy' so if using > 2 labels - then switch this to something smore suited to > 2 labels.

6. ensure you change the 'settings.py' files size inputs to be as close as possible to the input (while maintaining a square)
      a if in doubt scale down rather up up (to amount features becoming blocky pixels)

7. In preprocessing we rescale inputs to between 0-1 for all pixel values - this is a great explanation why its useful - https://www.linkedin.com/pulse/keras-image-preprocessing-scaling-pixels-training-adwin-jahn/

8. You will not be able to connect a usb to the VM - if you know a solution please do inform an organiser.

9. If you have an issues installing the requirements.txt file you should update these two dependencies:
      - numpy==1.14.0
      - scipy==1.0.0
