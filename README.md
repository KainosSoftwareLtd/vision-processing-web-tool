# Vision Processing Tool / QGIS: setup

Hey!

So, you want to use the Kainos computer vision tool to do some detection in your satellite images? Great! Let me help you get setup.

If you get stuck, feel free to grab Jordan McDonald (He will be floating around) to get some help.


## Pre-requisites

1. Download Oracle Virtualbox and its extension from [here](https://www.virtualbox.org/wiki/Downloads) 

      a. This will host our virtual machine (so you don&#39;t have to deal with pesky dependencies!) 
      
      b. Ensure you have free hard drive space (30gb)
      
2. Once you have it installed, download the Virtual machine image from here - ADD HERE.

3. Download QGIS from [here] (https://qgis.org/en/site/forusers/download.html)

4. Download the Airbus dataset from here - ADD HERE


Once you have all these things downloaded, lets focus on getting each of them setup - if you are confident in handling python dependencies feel free to ignore using the virtual machine and clone this repository directly.

Installing the virtual machine



3. Open the image with Virtual Box 

      a. File – Import Appliance – then select your downloaded VM
      
      b. Double click on the new appliance to start the VM
  
![](https://i.imgur.com/VM8tRFP.png)

4. Log in using the password &#39;machinelearning&#39;

      a. It might be slow loading the login page.
      
5. The first thing you need to do in the virtual machine is set up your ssh key for your github account. Here&#39;s how to [generate the key](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/) and [add it to your account](https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/)
      
      a. Or you can do it any other way your familiar with!
      
6. Now that that&#39;s set up you can clone the repo into the virtual machine (in the command line!)

      a. &#39;git clone https://github.com/KainosSoftwareLtd/vision-processing-web-tool.git&#39'

_Like magic, you have the tool on your virtual machine!_


**Project Setup**

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
