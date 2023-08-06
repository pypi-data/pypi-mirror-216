# mod_docx
The purpose of this library is to serve as a reliable and simple library to reassemble docx documents after they have been treated using AI/machine learning text treatment.

## Example of library usage
import os

import sys

sys.path.insert(1, '/usr/lib/python3.11/site-packages')

import mod_docx


### [Step 0] Open the docx file as an XML object
#### Obtain the orignal docx file
fpath = ".../mod_docx/tests"

fichier = "test_document.docx"

docx_filename = os.path.join(fpath, fichier)
        
#### Create a class object for the name_of_file.class_name. Use the class object, to call the functions in the class.
md = mod_docx.mod_docx(docx_filename)

#### Convert the orignal docx file to XML
document_org = md.opendocx(docx_filename)


### [Step 1] Modify the document
#### [To be completed for next version] Modify the document as desired (ie: replace text, change style, change font)
doc_finale = document_org

### [Step 2] Save the changed XML document as a docx file
root_dir = f'{fpath}/'

desired_output_docx_name = 'test_document_out.docx'

md.savedocx_ver_fichier(docx_filename, root_dir, desired_output_docx_name, doc_finale)
