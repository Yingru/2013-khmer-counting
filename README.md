# <font color=red'> Running the khmer paper script pipeline </font>

#### 2018-07-26

## 1. Origin pipeline (AWS)
following original [github](git@github.com:dib-lab/2013-khmer-counting.git)

Here are some brief notes on how to run the pipeline for our 2013 khmer counting paper on an Amazon EC2 rental instance.  Using these commands you should be able to completely recapitulate the paper.

The instructions below will reproduce all of the figures in the paper, and will then compile the paper from scratch using the new figures. Starting up a machine and get necessary data for reproduction: 

=====================================================
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
`cd ../`
`make`

and voila, 'khmer-counting.pdf' will contain the paper with the figures you just created.

