"""
    a2dl | (A)sciidoc(2D)rawio(L)ibrary | https://tigabeatz.net | MIT Licence
    This script generates a draw.io library from AsciiDoc-based descriptions.
"""

import base64
import glob
import hashlib
import json
import logging
import re
import struct
import sys
import uuid
import xml.etree.ElementTree as ET
from os import getcwd, makedirs
from os.path import abspath, join, dirname, basename
from shutil import copytree

# The following string determines the file search pattern:
GLOB_STRING = '**/*.adoc'  # Search for all adoc files recursively

# Detecting relevant lines in files can be customized with the following strings:
ADOC_VARIABLE_IDENTIFIER = [["==", "===", "====", "====="],
                            ":variable_name:"]  # Extract content afer each identifier until the next occurrence of i in [0]
ADOC_ICON_IDENTIFIER = ":icon_image_rel_path:"
ADOC_ICON_TITLE_IDENTIFIER = ":icon_name:"
ADOC_ICON_MORE_IDENTIFIER = ":read_more:"
LINES2SKIP = ['[quote', 'image::']  # skips lines starting with

# Formatting of the Tooltip can be customized with the following strings:
HTML_TOOLTIP = '<h1 class="dio_tooltip" >%name%</h1>'  # The HTML for each section will get appended to this string
HTML_SECTION = '<h2 class="dio_tooltip" >{}</h2>%{}%'  # variable['title'], variable['name']
HTML_WARNING = '<b class="dio_tooltip" >{}</b>'

# "read more" will be the last line in the html tooltip
HTML_MORE_BASEURL = '{}'  # 'or: use a base ur like https://example.com/{}
#      if articles details page share the same base url'
HTML_MORE = '<br> <a href="{}" target="_more">Image generated with Stable Diffusion</a>'

# Icon styling
ICON_STYLE = "rounded=1;whiteSpace=wrap;html=1;"

# If sections include images as .png, these will be encoded and included. The image styling can be modified:
IMAGE_STYLE = 'fillColor=none;rounded=1;shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image=data:image/{},{};'  # The type and image data are set from the file

# Generator settings
ARTICLE_TEMPLATE = 'data/template_article.adoc'
IMAGES_PATH = 'data/images'
IMAGES_GLOB_STRING = '**/*.png'
IMAGES_WIDTH = "70"
IMAGES_HEIGHT = "70"

# create logger
logger = logging.getLogger('a2dl')
logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)
logger.addHandler(sh)


class Diagicon:
    """
    The `diagicon` class is responsible for generating diagram icons from AsciiDoc files.

    Usage:
    >>> my_icon = Diagicon()
    >>> x= my_icon.from_adoc('./docs/example.adoc')
    >>> my_icon.write_diagram('./test/test-icon.drawio')

    """

    def __init__(self, iconid=None, name=None):
        """
        Initializes a new diagicon instance.

        Args:
        iconid (str): The unique ID for the icon. If none is provided, a UUID is generated.
        name (str): The name for the icon. If none is provided, the id is used.
        """
        self.tooltip = HTML_TOOLTIP
        self.html_section = HTML_SECTION

        if not iconid:
            self.iconid = str(uuid.uuid1())
        else:
            self.iconid = iconid
        if not name:
            self.name = self.iconid
        else:
            self.name = name

        self.placeholders = "1"
        self.link = None
        self.image = None
        self.variables = None  # [{"title":label, "name":label, "content":[] }]
        self.parent = "1"
        self.vertex = "1"
        self.x = "80"  # NEED 4 DIAGRAM
        self.y = "160"  # NEED 4 DIAGRAM
        self.width = "160"  # NO FUNCTION
        self.height = "160"  # NO FUNCTION
        self.style = ICON_STYLE

    @staticmethod
    def __read_diagram2dict__(filename):
        """
        read a draw.io diagram and return as dict

        >>> hashlib.sha256(json.dumps(Diagicon.__read_diagram2dict__('./data/icon.drawio'), sort_keys=True).encode('utf-8')).hexdigest()

        """

        tree = ET.parse(filename)
        root = tree.getroot()

        # data = base64.b64decode(root.text)
        # xml = zlib.decompress(data, wbits=-15)
        # xml = unquote(xml.decode('utf-8'))

        xmlobjects = []

        for xmldict in root:
            for xmlobject in xmldict[0][0]:
                if xmlobject.tag == 'object':
                    icon = {"tag": xmlobject.tag, "attrib": xmlobject.attrib, "elements": []}
                    for el in xmlobject:
                        icon['elements'].append({"tag": el.tag, "attrib": el.attrib, "elements": []})
                        for shape in el:
                            icon['elements'].append({"tag": shape.tag, "attrib": shape.attrib})
                    xmlobjects.append(icon)

        return xmlobjects

    @staticmethod
    def __get_base64_encoded_image__(image_path):
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
        except FileNotFoundError as err:
            logger.error(err)

    @staticmethod
    def __get_image_size__(file_path):
        with open(file_path, 'rb') as f:
            data = f.read(24)
        if len(data) != 24:
            logger.warning(f'The file {file_path} is not a PNG image.')
            return None, None
        if data[:8] != b'\x89PNG\r\n\x1a\n':
            logger.warning(f'The file {file_path} is not a PNG image.')
            return None, None

        width, height = struct.unpack('>LL', data[16:24])
        logger.debug(f'The file {file_path} is a PNG image with width: {width} and height: {height}.')

        return width, height

    def __as_object__(self, parent=None):
        if parent:
            xmlobject = ET.SubElement(parent, "object")
        else:
            xmlobject = ET.Element("object")

        xmlobject.set("id", self.iconid)
        xmlobject.set("label", self.name)  # SPECIAL used when icon is used library
        xmlobject.set("name", self.name)
        xmlobject.set("placeholders", self.placeholders)
        xmlobject.set("tooltip", self.tooltip)

        # any custom fields
        for variable in self.variables:
            vt = ''
            for l in variable['content']:
                vt = vt + str(l)
            xmlobject.set(variable['name'], vt)
            self.tooltip = self.tooltip + self.html_section.format(variable['title'], variable['name'])

        # add readmore
        if self.link:
            xmlobject.set("link", HTML_MORE_BASEURL.format(self.link))
            self.tooltip = self.tooltip + HTML_MORE.format(HTML_MORE_BASEURL.format(self.link))

        mxCell = ET.SubElement(xmlobject, "mxCell")
        mxCell.set("parent", self.parent)
        mxCell.set("vertex", self.vertex)

        # image
        if self.image:
            if self.image.endswith('.png'):
                self.width, self.height = self.__get_image_size__(self.image)
                if self.width:
                    mxCell.set("style", IMAGE_STYLE.format('png', self.__get_base64_encoded_image__(self.image)))
            else:
                logger.warning('fileformat for {} not implemented'.format(self.image))

        mxGeometry = ET.SubElement(mxCell, "mxGeometry")
        mxGeometry.set("x", str(self.x))
        mxGeometry.set("y", str(self.y))
        mxGeometry.set("width", str(self.width))
        mxGeometry.set("height", str(self.height))
        mxGeometry.set("as", "geometry")

        return xmlobject

    def __as_diagram__(self):
        # The element tree
        mxfile = ET.Element("mxfile")
        diagram = ET.SubElement(mxfile, "diagram",
                                name="Page-1", id=str(uuid.uuid1()))
        mxGraphModel = ET.SubElement(diagram, "mxGraphModel",
                                     dx="1114", dy="822", grid="1", gridSize="10",
                                     guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1",
                                     pageScale="1", pageWidth="1169", pageHeight="827", math="0", shadow="0")
        root = ET.SubElement(mxGraphModel, "root")
        mxCelldiag1 = ET.SubElement(root, "mxCell",
                                    id="0")
        mxCelldiag2 = ET.SubElement(root, "mxCell",
                                    id="1", parent="0")
        xmlobject = self.__as_object__(root)
        return mxfile

    def as_object(self, parent=None):
        """to embed in other xml structures"""
        return self.__as_object__(parent)

    def as_object_s(self):
        """to embed in other library xml structures"""
        mxGraphModel = ET.Element("mxGraphModel")
        root = ET.SubElement(mxGraphModel, "root")
        mxCelldiag1 = ET.SubElement(root, "mxCell",
                                    id="0")
        mxCelldiag2 = ET.SubElement(root, "mxCell",
                                    id="1", parent="0")
        asd = self.__as_object__(parent=root)
        rt = None
        try:
            rt = ET.tostring(mxGraphModel).decode(encoding='utf-8')
        except Exception as err:
            logger.error(f'{self.name} {self.iconid} {err}')
        return rt

    def as_diagram_s(self):
        """return a string of diagram xlm"""
        xmlstr = ET.tostring(self.__as_diagram__())
        return xmlstr

    def write_diagram(self, file):
        """write as a diagram file"""
        tree = ET.ElementTree(self.__as_diagram__())
        tree.write(abspath(file))

    @staticmethod
    def linerules(oline):
        """add special line handling, like make ascidoc url to html url"""
        # exchange link
        if "http" in oline:
            # get url, domain, link description "(^http.?://(.*))\[(.*)\]"
            words = oline.split()
            uline = oline
            for word in words:
                m = re.search("(^http.?://(.*))\[(.*)\]", word)
                # todo: change regex, such that any text inside the [] works (breaks with whitespace, actually)
                if m:
                    # logger.debug(m.group(3))
                    if len(m.group(3)) < 3:
                        mn = '<a href="{}" target="_blank">{}<a>'.format(m.group(1), m.group(2))
                    else:
                        mn = '<a href="{}" target="_blank">{}<a>'.format(m.group(1), m.group(3))
                    uline = oline.replace(m.group(0), mn)
                    # logger.debug(uline)
            logger.debug(f'replacing {oline} with {uline}')
            return uline

        # replace Warning
        elif oline.startswith('WARNING:'):
            uline = HTML_WARNING.format(oline.strip("WARNING:").strip())
            logger.debug(f'replacing {oline} with {uline}')
            return uline

        else:

            # strip adoc image lines, quotes and such
            for stripsign in LINES2SKIP:
                if oline.startswith(stripsign):
                    uline = ''
                    logger.debug(f'replacing {oline} with {uline}')
                    return uline

            return oline

    def from_adoc(self, filename, parent=None):
        """set from adoc and return as object"""

        def get_data(lines):
            variables = []
            icon_full_path = None
            starts = []

            def extract(s, e):
                c = []
                i = 0
                for eline in lines:
                    if s + 3 <= i <= e:
                        # c.append(line)
                        found = False
                        for l2_ident in ADOC_VARIABLE_IDENTIFIER[0]:
                            if eline.startswith(l2_ident):
                                found = True
                        if not found:
                            # special line handling, like make url tags ...
                            nline = self.linerules(eline)
                            c.append(nline)
                        else:
                            break
                    i += 1
                return c

            # start
            line_number = 0
            for line in lines:
                # --> the variables are repeated
                for l1_ident in ADOC_VARIABLE_IDENTIFIER[0]:
                    if line.startswith(l1_ident) and lines[line_number + 1].startswith(ADOC_VARIABLE_IDENTIFIER[1]):
                        variables.append({
                            "title": line.strip(l1_ident).strip(),
                            "name": lines[line_number + 1].strip(ADOC_VARIABLE_IDENTIFIER[1]).strip(),
                            "start": line_number,
                        })
                        starts.append(line_number)
                        break

                if line.startswith(ADOC_ICON_IDENTIFIER):
                    icon_full_path = abspath(join(dirname(filename), line.strip(ADOC_ICON_IDENTIFIER).strip()))
                    self.icon = icon_full_path

                if line.startswith(ADOC_ICON_TITLE_IDENTIFIER):
                    self.name = line.strip(ADOC_ICON_TITLE_IDENTIFIER).strip()

                if line.startswith(ADOC_ICON_MORE_IDENTIFIER):
                    self.link = line.strip(ADOC_ICON_MORE_IDENTIFIER).strip()

                line_number += 1

            # end
            for variable in variables:
                cnt = 0
                for start in starts:
                    if variable['start'] == start:
                        try:
                            variable['end'] = starts[cnt + 1] - 1
                        except Exception as err:
                            variable['end'] = len(lines)
                            logging.debug(err)
                    cnt += 1

            # content
            for variable in variables:
                variable['content'] = extract(variable['start'], variable['end'])

            return variables, icon_full_path

        try:
            with open(filename, "r") as file:
                fileslines = file.readlines()

            self.variables, self.image = get_data(fileslines)
            logger.debug(f'{filename} {len(self.variables)} {self.image}')

            if len(self.variables) == 0 and not self.image:
                raise ValueError('is not an icon file and will be sKipped')
            else:
                return self.__as_object__(parent)

        except FileNotFoundError as err:
            logger.error(err)

        return None


class Diaglibrary:
    """
    >>> my_icon = Diagicon(name='tigabeatz')
    >>> x = my_icon.from_adoc('./data/example.adoc')
    >>> my_library = Diaglibrary()
    >>> my_library.icons.append(my_icon)
    >>> my_library.write('./data/test-generated-library.xml')

    >>> my_library2 = Diaglibrary()
    >>> my_library2.from_folder('./data')
    >>> my_library2.write('./data/test-generated-library2.xml')

    """

    def __init__(self, libraryid=None, name=None):

        if not libraryid:
            self.libraryid = str(uuid.uuid1())
        else:
            self.libraryid = libraryid

        self.name = name
        self.icons = []  # instances of type icon
        self.w = 50
        self.h = 50

    def __as_object__(self):

        mxlibrary = ET.Element("mxlibrary")
        tmpl = []
        for icn in self.icons:
            tmpl.append(
                {
                    "xml": icn.as_object_s(),
                    "w": self.w,
                    "h": self.h
                })

        mxlibrary.text = json.dumps(tmpl, indent=2)
        return mxlibrary

    @staticmethod
    def __read_library2dict__(filename):
        """
        read a draw.io library and return as dict

        >>> hashlib.sha256(json.dumps(Diaglibrary.__read_library2dict__('data/library.xml'), sort_keys=True).encode('utf-8')).hexdigest()

        """

        tree = ET.parse(abspath(filename))
        root = tree.getroot()
        data = json.loads(root.text)
        xmlobjects = []

        for xmldict in data:
            xmlobject = ET.fromstring(xmldict['xml'])
            icon = {"tag": xmlobject[0].tag, "elements": []}
            for el in xmlobject[0]:
                icon['elements'].append({"tag": el.tag, "attrib": el.attrib})
            xmlobjects.append(icon)

        return xmlobjects

    def write(self, file):
        """write as a library file"""
        try:
            tree = ET.ElementTree(self.__as_object__())
            tree.write(abspath(file))
        except TypeError as err:
            logger.critical(f'{file} {err}')

    def from_folder(self, path):
        files = glob.glob(join(abspath(path), GLOB_STRING), recursive=True)
        for file in files:
            try:
                icn = Diagicon()
                icn.from_adoc(file)
                self.icons.append(icn)
            except ValueError as wrn:
                logger.warning(f'{file}, {wrn}')
            except Exception as err:
                logger.error(f'{file}, {err}')

        logger.info(f'files: {len(files)} ')
        logger.info(f'icons: {len(self.icons)} ')

        for logicon in self.icons:
            logger.debug(f'{logicon.variables} {logicon.image}')


def make_example(target_path='test/'):
    """
    Generates a folder with articles images library

    >>> make_example()

    :param target_path: like "./test/"
    :return:
    """
    def apply_template(image_name="", image_link="", image_alt_text="", image_h=IMAGES_HEIGHT, image_w=IMAGES_WIDTH,
                       image_rel_path=""):
        """
        :icon_image_rel_path: {{image_rel_path}}
        :icon_name: {{image_name}}
        :read_more: {{image_link}}
        [[sec-{{image_name}}]]
        == {{image_name}}
        image::{icon_image_rel_path}[{{image_alt_text}},{{image_w}},{{image_h}},float="right"]
        === {{image_name}} Summary
        """

        searchies = [
            ('{{image_name}}', image_name.strip('\n').strip())
            , ('{{image_link}}', image_link.strip('\n').strip())
            , ('{{image_alt_text}}', image_alt_text.strip('\n').strip())
            , ('{{image_h}}', image_h.strip('\n').strip())
            , ('{{image_w}}', image_w.strip('\n').strip())
            , ('{{image_rel_path}}', image_rel_path.strip('\n').strip())
        ]

        try:
            nt = []
            with open(abspath(ARTICLE_TEMPLATE), "r") as file:
                fileslines = file.readlines()
                for line in fileslines:
                    for searcher in searchies:
                        if searcher[0] in line:
                            line = line.replace(searcher[0], str(searcher[1]))
                    nt.append(line)
            return nt
        except FileNotFoundError as err:
            logger.error(err)

        return None

    # create dir
    makedirs(dirname(abspath(target_path)), exist_ok=True)

    # images
    images = glob.glob(join(abspath(IMAGES_PATH), IMAGES_GLOB_STRING), recursive=True)
    copytree(IMAGES_PATH, abspath(target_path), dirs_exist_ok=True)

    # generate icons, articles and library
    library = Diaglibrary()
    for imagepath in images:
        icon = Diagicon()

        # article
        article = (
            apply_template(
                image_name=basename(imagepath).strip(".png"),
                image_rel_path=join(abspath(target_path), basename(imagepath)),
                image_link=f"#{basename(imagepath).strip('.png')}",
                image_alt_text=f'image {basename(imagepath)} is a random generated image',
                image_h=IMAGES_WIDTH,
                image_w=IMAGES_HEIGHT
            ),
            basename(imagepath)
        )
        tap = join(abspath(target_path), f'{basename(imagepath).strip(".png")}.adoc')

        targetarticle = open(tap, "w")
        targetarticle.writelines(article[0])
        targetarticle.close()

        # icon
        x = icon.from_adoc(tap)
        icon.image = imagepath
        icon.width = IMAGES_WIDTH
        icon.height = IMAGES_HEIGHT

        library.icons.append(icon)

    # library
    library.w = IMAGES_WIDTH
    library.h = IMAGES_HEIGHT
    library.write(join(target_path, 'test-generated-library.xml'))


def cli():
    if not len(sys.argv) == 3:
        logger.critical(
            "The script is called with {} arguments, but needs 2: 'a2dl path/to/folder-to-scan path/to/library-file-to-write.xml' ".format(
                len(sys.argv) - 1))
    else:
        if sys.argv[1] == '--example' and sys.argv[2]:
            logger.info(f'Creating Example {sys.argv[2]}')
            make_example(sys.argv[2])
            logger.info(f'Done with creating example {sys.argv[2]}')
        else:
            cwd = getcwd()
            logger.info(f'workdir: {cwd}')
            logger.info('source: {} '.format(sys.argv[1]))
            logger.info('target: {} '.format(sys.argv[2]))

            logger.info('Creating library')
            my_library2 = Diaglibrary()
            my_library2.from_folder(sys.argv[1])
            my_library2.write(sys.argv[2])
            logger.info('Done with creating library')


if __name__ == '__main__':
    cli()
