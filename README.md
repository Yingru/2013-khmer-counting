# <font color='red'> Running the khmer paper script pipeline </font>

#### 2018-07-26
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/Yingru/2013-khmer-counting.git/master)

# Table of content
===================================================
- [1. Original pipeline AWS](# 1. Origin pipeline (AWS))
- [2. Jetstream pipeline](# 2. Jetstream pipeline)
- [3.Docker container pipeline](# 3. Docker container pipeline)
- [4. Singularity container pipeline](# 4. Docker container pipeline)
- [5. ipython notebook]() [![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/Yingru/2013-khmer-counting.git/master)
## 1. Origin pipeline (AWS)
following original [github](git@github.com:dib-lab/2013-khmer-counting.git)

Here are some brief notes on how to run the pipeline for our 2013 khmer counting paper on an Amazon EC2 rental instance.  Using these commands you should be able to completely recapitulate the paper.

The instructions below will reproduce all of the figures in the paper, and will then compile the paper from scratch using the new figures. Starting up a machine and get necessary data for reproduction: 

-------------------------------------------------------------------------
### 1.1 First, start up an EC2 instance using starcluster
` starcluster start -o -s 1 -i m2.2xlarge -n ami-999d49f0 pipeline`


You can also do this via the AWS console; just use ami-999d49f0, and start an instance with 30gb or more of memory. Make sure that port 22 (SSH) and port 80 (HTTP) are open; you'll need the first one to log in, and the second one to connect to the ipython notebook.

### 1.2 Now, log in!
` starcluster sshmaster pipeline `

(or just ssh in however you would normally do it.)

### 1.3.1 Installing software and running script
```bash
#a. First go to /mnt/ because we do not have enough space in home directory
cd /mnt

#b. Now, check out the source repository and grab the initial datasets
git clone https://github.com/ngs-docs/ngs-scripts

git clone https://github.com/ged-lab/2013-khmer-counting.git
cd 2013-khmer-counting

curl -O http://public.ged.msu.edu.s3.amazonaws.com/2013-khmer-counting/2013-khmer-counting-data.tar.gz

tar xzf 2013-khmer-counting-data.tar.gz

```

### 1.3.2 Installing necessary software

Before we get started, we need to install all the necessary software(including khmer), including:

 - Tallymer
 - Jellyfish
 - DSK
 - KMC
 - BFCount
 - Turtle
 - QUAST
 - FASTX-toolkit
 - seqtk
 - ipython
 - LaTex
 - Velvet
 - Java
 - screed
 - khmer
 
 ```bash
 cd /mnt/2013-khmer-counting/pipeline
 bash software_install.sh
 ```
 
### 1.3.3 Running the pipeline
Now go into the pipeline directory and run the pipeline.  This will take a few hours, so you might want to do it in 'screen' (see [**Running long jobs on UNIX**](http://ged.msu.edu/angus/tutorials-2011/unix_long_jobs.html) )
```
cd /mnt/2013-khmer-counting/pipeline
make KHMER=/usr/local/src/khmer
```

### 1.3.4 Producing the paper
```
# Once the job successfully completes, copy the data over to the ../data/ directory
make copydata

# Run the ipython notebook server
cd ../notebook
ipython notebook --no-browser --ip=* --port=80 &
```


Connect into the ipython notebook (it will be running at 'http://<your EC2 hostname>'); if the above command succeeded but you can't connect in, you probably forgot to enable port 80 on your EC2 firewall.

Once you're connected in, select the 'khmer-counting' notebook (should be the only one on the list) and open it.  Once open, go to the 'Cell...' menu and select 'Run all'.

Now go back to the command line and execute:
```
cd ../
make
```

and voila, 'khmer-counting.pdf' will contain the paper with the figures you just created.

-------------------------------------------------------------------------
## 2. Jetstream pipeline
<font color='red'> Key concept is that it is actually working at this moment. Today: 2018-07-26 </font>

### 2.1 Create a Jetstream instance
- Log onto Jetstream here: https://jetstream-cloud.org/
- Create Jetstream instance (Project -> New -> Instance):
    - Instance Name: Ubuntu 14 (with docker) if you want to use the same instance later to test docker images
    - Flavor:  m1.large (CPU: 10, Mem: 30 GB, Disk: 60 GB)
    - Volume: if you want to run the full analysis, require additional 1 TB volume. If testing smaller test file, 100 GB volume would be enough.
        - Create new volume (Project -> New -> Volume)
        -  Make sure your volume is on the same provider as your instance
        - Set it for ~100GB
        - When you create this volume there is a 'bug' in Atmosphere that will say you are 'over quota' - please ignore
    - [Jetstream wiki on volume](https://iujetstream.atlassian.net/wiki/spaces/JWT/pages/32899126/Attach+a+Volume)
    -  To attach your volume to your instance
    `df -lh` will show you the name and size of your volume (e.g., /vol_b)
    - Go to the 'Project' page, click the Volume you just created, click 'Attach' in the bar on the right side of the page, and select your instance.

### 2.2 Download the datasets and corrected software_install.sh file
```
#a. login into your jetstream instance
ssh usrname@ip_adress 

#b. Navigate to your volume (or any other directory you'd like to work, such as /home/$USER)
cd /vol_b  

#c. Download or clone the git repository and dataset
git clone https://github.com/ngs-docs/ngs-scripts
git clone https://github.com/Yingru/2013-khmer-counting.git

cd 2013-khmer-counting/

#d. Download the dataset
curl -O http://public.ged.msu.edu.s3.amazonaws.com/2013-khmer-counting/2013-khmer-counting-data.tar.gz

tar xzf 2013-khmer-counting-data.tar.gz  # size: 5731M => 19 GB

#e. Install the softwares
cd pipeline/
bash software_install.sh
```

NOTE: we are aware that sometimes the installing will get interrupted, due to there are two links for the softwares are not stable. If you are lucky, clean the ` rm -r /usr/local/src/*` and re-run `bash software_install.sh` a few times, it should work.

 If you are super in-patient, try to download the files by hand: it should be the two links to `KAnalyze` and `QUAST` causing the issue.


### 2.3 Run the pipeline
- option A, you can choose to run the origin files, which may take up to a good few hours
- option B, or you can run a smaller test files, just to get a taste of how's the workflow looks like

```bash
#a. for option A (run the full files, ignore this step), to selected 1/1000 of the original size, if you want a larger test_file, use ./subset_files_10 one
./subset_files_1000   

#b. run the pipeline
make KHMER=/usr/local/src/khmer
```
- Note, you can run the **Makefile** step-by-step, for example:
`make khmer` will only run `khmer`, `make jellyfish` will only run `jelly` fish. 

Now you suppose to have all the files produced and ready to make plots.

### 2.4 Generate paper
This would be the same as in [1.3.4](# 1.3.4 producing the paper)
```
#a. copyig data
make copydata

#b. Run the ipython notebook server
cd ../notebook
ipython notebook --no-browser --ip=* --port=80 &

#c. checking hostname and loggin in your brower: http://hostname
echo $hostname

#d. on the top cell, click run all

cd ../
make 
```
The final results will be the paper itself. :)

-------------------------------------------------------------------------
## 3. Docker container pipeline

### 3.1 Build container from scratch
If you like to build the docker container from scratch (which may take around 30 mins), you can build from the dockerfile/Dockerfile
```
#a. login into Jetstream instance (make sure you actually have the docker installed)
ssh username@ip_address

#b. configure container in the instance
sudo -s
edz  

#b. If you already have the github repository and the datasets, ignore this step
git clone https://github.com/Yingru/2013-khmer-counting.git
cd 2013-khmer-counting/
curl -O http://public.ged.msu.edu.s3.amazonaws.com/2013-khmer-counting/2013-khmer-counting-data.tar.gz

tar xzf 2013-khmer-counting-data.tar.gz
cd pipeline/
./subset_files_1000

#c. go get the Dockerfile, which is in the dockerfile folder. The building takes a while
cd ../dockerfile
docker build -t khmer_yingru:v1 .

#d. run the docker images
cd ../pipeline/
docker run -v `pwd`:/tmp khmer_yingru:v1 make KHMER=/usr/local/src/khmer

# If you like to only run a few command
docker run -v `pwd`:/tmp khmer_yingru:v1 make khmer

# If you like to play around with docker container interactively
docker run  -it -v `pwd`:/tmp khmer_yingru:v1 
```

### 3.2 Get the docker container from dockerhub
A more convenient way is to pull the docker container from the dockerhub, in that way you don't need to wait for building it.
```
#a. b.  steps are similar to previous one
#c. pull the docker image
docker pull yingruxu/khmer_yingru:latest

#d. run the docker images
cd ../pipeline/
docker run -v `pwd`:/tmp yingruxu/khmer_yingru:latest make KHMER=/usr/local/src/khmer
```

----------------------------------------------------------------------------

## 4. Singularity pipeline

### 4.1 An easier way (current broken! need to fix)
An easier/dirtier way to create a `singularity` images would be convert from a **Dockerfile**. Try this command:
```
#a. first install singularity
sudo apt-get install libtool
git clone https://github.com/singularityware/singularity.git
cd singularity/
git checkout 2.3.1
./autogen.sh 
./configure --prefix=/usr/local --sysconfdir=/etc
make
sudo make install


#b. check your docker image list
sudo docker images

#c. create singularity image with 4024MB space and exts file system 
singularity create -s 4024 khmer_yingru.simg

#d. build the singularity imag from dockerhub
singularity import khmer_yingru.simg docker://yingruxu/khmer_yingru:latest

#e. run the singularity image
```

----------------------------------------------------------------------------

## [5. ipython notebook]() [![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/Yingru/2013-khmer-counting.git/master)

- Click the label, and launch to a Jupyter notebook environment. 
- Go to folder `notebook`
- You will find the `ipython-notebook`, play around with it !

