from setuptools import setup

# with open("README.adoc", "r", encoding="utf-8") as fh:
#     long_description = fh.read()

long_description = """\

## a2dl | (A)sciidoc(2D)rawio(L)ibrary

This script generates a draw.io library from AsciiDoc-based descriptions.

- It recursively searches for adoc files in a given folder and scans for specific lines within these files.
- These lines are merged into HTML tooltips of draw.io icons.
- The Icons are bundled into an draw.io / diagrams.net library

I had the need to visualize the relationship within already written content. 
i wrote this script to extract  portions of articles into tooltips for draw.io icons, 
such i can focus on networking the articles and show contextual info during presentation.

### Install

    python3 -m pip install a2dl

### CLI Usage

    python3 -m a2dl ./data ./data/test-generated-library.xml

or

    a2dl ./data ./data/test-generated-library.xml


### Prepare Asciidoc files

To use this script, simply add the identifiers to any adoc file.

Set these variables at the top of the file

* :icon_image_rel_path: images/generated/3.png
   -> Path to an Icon Image PNG
   
* :icon_name: Icon3
   -> Name for the Icon
   
* :read_more: #sec-icon3
  -> Link for more info, to be appended to the tooltips end

These two lines form the start of a Tooltips content, 
while the first line will also work as a stop sign for the content extraction:

* == or === up to =====

* :variable_name: short_description
  -> choose any name for your variable, but do not include whitespace

### Example Adoc

    :toc:
    :icon_image_rel_path: images/generated/3.png
    :icon_name: Icon3
    :read_more: #sec-icon3
    
    [[sec-icon3]]
    == Icon 3
    
    image::{icon_image_rel_path}[The Icon 3s Alternative Text,160,160,float="right"]
    
    === Short Description
    :variable_name: short_description
    
    This is short Text to Describe the icon
    A short abstract of the Topic
    
    WARNING: Not Safe For Work
    
    
    === XML Attribute 1
    :variable_name: xml_attribute_1
    
    Some part of the text to add to the icons data 

"""

setup(
    name='a2dl',
    version='0.1.1',
    packages=['a2dl'],
    package_data={'a2dl': ['data/**/*']},
    install_requires=[],
    url='https://tigabeatz.net',
    author='tigabeatz',
    author_email='tigabeatz@cccwi.de',
    description='Generate draw.io icon libraries from AsciiDoc-based descriptions.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Development Status :: 3 - Alpha"
    ],
    entry_points={
        'console_scripts': [
            'a2dl=a2dl.a2dl:cli'
        ]
    },
)

