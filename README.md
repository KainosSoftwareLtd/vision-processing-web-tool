# vision-processing-web-tool

Hey!

So, you want to use the Kainos computer vision tool to do some detection in your satellite images? Great! Let me help you get setup.

If you get stuck, feel free to grab Jordan McDonald (I will be floating around) to get some help.


**Pre-requisites**

1. Download Oracle Virtualbox and its extension from [here](https://www.virtualbox.org/wiki/Downloads) 

      a. This will host our virtual machine (so you don&#39;t have to deal with pesky dependencies!) 
  
      b. Ensure you have free hard drive space (30gb)
2. Once you have it installed, download the Virtual machine image from [here](https://kainossoftwareltd.sharepoint.com/:u:/r/sites/appliedinnovation/Shared%20Documents/projects/space-lecture/space-hack.ova?csf=1&amp;e=6fQOpy)
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
