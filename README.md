# Images2pdf

Python script to create pdf from a directory of images

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Images2pdf](#images2pdf)
	- [Goal of this project](#goal-of-this-project)
	- [Requirements](#requirements)
	- [How to use](#how-to-use)
		- [Config File](#config-file)
		- [Mode section](#mode-section)
		- [Running the script](#running-the-script)
	- [Annex A - Mode subdirectoriesToPdf](#annex-a-mode-subdirectoriestopdf)
	- [Annex B - Mode collectionToPdf](#annex-b-mode-collectiontopdf)

<!-- /TOC -->

## Goal of this project

I wanted to make pdfs from my entire collections of scans that I have. Every GUI that I found on the internet were not doing batch stuff.

Meaning I would have to manually go select my directory, select all of its images, specify were I want the pdf to be output. Repeat for every folder of scans that I had.

This is not very efficient.

This simple python script makes it way easier. Three mode can be used (see Mode section) and everything for the configuration stays in a json file.

**TODO** At this moment, this project relies on multiples modules and thus can be simplify.

## Requirements

This script requires different modules.

First you need python installed on your computer (tested with 3.5.2, but should worked with anything Python v3).

Then you gonna need these modules :
  - json => for loading the config file
  - img2pdf => to convert the images to pdf
  - zipfile => to make backup in .zip
  - mpipe => making a pipeline for processing

Just ```pip install``` all of them.

## How to use
Now the fun part, how to use this script!

First download the script you want in the "Code" folder.

Then either download (in the folder "Config Example") or create a config file in the same folder that you have the script.

### Config File
The config file needs these fields:
  - "path" => Path to fetch the data from
  - "mode" => mode to use, see Mode section
  - "backup" => Make a backup (true or false)
  - "remove_dir" => Remove directory that have the images (true or false)
  - "debug" => Print message on the status of the execution (true or false), errors will still shows if this is set to false
  - "name" => Optional field only use in "directoryToPdf" mode. Allows to specify the name for the pdf and the zip file(s).

It also needs to be a json file with this exact name : "config.json" and it needs to be in the same directory as the script when running (Or else you **WILL** get errors).

### Mode section
Three modes are availaible to you :
   1. "directoryToPdf"
    This mode allows to output a pdf file for a specific directory containing images. Can specify the name for ouput file(s)
  2. "subdirectoriesToPdf"
    This mode takes a path to a folder. This folder contains subdirectories that each have the images in them. It outputs the pdf file in the folder. Backups are in the "BACKUP" folder. Both the pdf and the backup have the subdirectory     name as filename (See Annex A for a tree representation)
  3. "collectionToPdf"
    This mode takes a path to a folder. This folder contains mutiple folders. Process each of these folders like in mode "subdirectoriesToPdf". (See Annex B for a tree representation)

### Running the script
Open a terminal (or a cmd) on your computer and type in ```python images2pdf.py```. If you have done the previous steps correctly, your images will be converted to pdf.

Note : If you are using the debug option, it is possible that a filename.pdf does not appear on the terminal output. This simply means this filename is not compatible with the python print() function. (it is in the todo)

## Annex A - Mode subdirectoriesToPdf
Before script :
```
---- Path Specify
-------- Folder1
------------ Image1.jpg
------------ Image2.jpg
------------ Image3.jpg
------------ Image4.jpg
-------- Folder2
------------ Image1.jpg
------------ Image2.jpg
------------ Image3.jpg
------------ Image4.jpg
```
with remove_dir set to true, backup to true, final results
```
---- Path Specify
-------- BACKUP
------------ Folder1.zip
------------ Folder2.zip
-------- Folder1.pdf
-------- Folder2.pdf
```

## Annex B - Mode collectionToPdf
Before script :
```
---- Path Specify
-------- Folder1
------------ Folder2
---------------- Image1.jpg
---------------- Image2.jpg
---------------- Image3.jpg
---------------- Image4.jpg
-------- Folder3
------------ Folder4
---------------- Image1.jpg
---------------- Image2.jpg
---------------- Image3.jpg
---------------- Image4.jpg
```
with remove_dir set to true, backup to true, final results
```
---- Path Specify
-------- Folder1
------------ BACKUP
---------------- Folder2.zip
------------ Folder2.pdf
-------- Folder3
------------ BACKUP
---------------- Folder4.zip
------------ Folder4.pdf
```
