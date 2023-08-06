# Generation-image_Gaston
## Description
Génération-image_Gaston is a Python package that allows you to generate images from a given prompt using the craiyon.com site. This package uses Selenium to automate the image build and upload process.

## Facility
You can install the Génération-image_Gaston package using pip:

pip install Generation-image_Gaston
Make sure you have the following dependencies installed:

undetected_chromedriver
selenium
It settles down on its own normally.
## Use
Here is an example of using the package:


from Generation_Image_Gaston import SelectStyle

SelectStyle("Three Crying Cat...", "PHOTO")
The SelectStyle function takes two parameters:

Prompt: The text to use as a prompt to generate the image.
Style: The desired image style. The available options are "PHOTO", "DRAWING" and "ART".
The function performs the following steps:

Opens the craiyon.com website.
Accept cookies (if necessary).
Selects the specified Picture Style.
Enters the given prompt.
Generates the image.
Download the image to your computer.
Please note that the build process may take some time. When the download is complete, the message "Download is complete" will be displayed.

Make sure you have Chrome installed on your system, as the package uses Chrome to interact with the website.