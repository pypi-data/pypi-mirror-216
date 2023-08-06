# --------------
# Purpose
# --------------
# The purpose of this library is to serve as a reliable and simple library to reassemble docx documents after they have been treated using AI/machine learning text treatment. Many AI libraries exist that extract text from documents and treat text (ie: translation, similarity of words, sumarization of text, etc), however there lacks robust libraries that automatically reassemble documents in a coherent manner. This library reassembles docx files in a simple manner.


# --------------
# Example: using the package to open and close a file
# --------------
# Using PyPI repository 
# import os
# import sys
# sys.path.insert(1, '/usr/lib/python3.11/site-packages')

# import name_of_folder
# import mod_docx

# from name_of_folder import name_of_file as nickname
# from mod_docx import mod_docx as mdocx

# --------------------------------------

# [Step 0] Open the docx file as an XML object
# Obtain the orignal docx file
# fpath = "/usr/lib/python3.11/site-packages/mod_docx/tests"
# fichier = "test_document.docx"
# docx_filename = os.path.join(fpath, fichier)
        
# Create a class object for the name_of_file.class_name. Use the class object, to call the functions in the class.
# md = mdocx(docx_filename)

# Convert the orignal docx file to XML
# document_org = md.opendocx(docx_filename)

# --------------------------------------

# [Step 1] Modify the document
# [To be completed for next version] Modify the document as desired (ie: replace text, change style, change font)
# doc_finale = document_org

# --------------------------------------

# [Step 2] Save the changed XML document as a docx file
# root_dir = f'{fpath}/'
# desired_output_docx_name = 'test_document_out.docx'
# md.savedocx_ver_fichier(docx_filename, root_dir, desired_output_docx_name, doc_finale)

# ---------------------------------------------


# --------------
# Version explaination
# --------------
# Beta version library is inspired by docx.py Pypi libary, however this is a simplier version of the library where it only includes: 0) opening a docx file and 2) saving a modified docx file. The saving prodecure in docx.py was difficult to understand, so a simplier saving procedure was created.

# Next version will include : simple text search and replacement


# --------------
# References: 
# --------------
# https://realpython.com/python-zipfile/
# https://docs.python.org/fr/3/library/zipfile.html
# https://realpython.com/working-with-files-in-python/
# https://www.geeksforgeeks.org/reading-and-writing-xml-files-in-python/
# https://www.geeksforgeeks.org/create-xml-documents-using-python/
# https://docs.python.org/3/library/xml.etree.elementtree.html
# https://www.geeksforgeeks.org/unzipping-files-in-python/




import os
import zipfile
from lxml import etree
import shutil

class mod_docx:
    def __init__(self, filename='', root_dir='', desired_output_docx_name='', doc_finale=''):
        self.filename = filename
        self.root_dir = root_dir
        self.desired_output_docx_name = desired_output_docx_name
        self.doc_finale = doc_finale
  
  
    # ---------------------------------------------
    # Open a docx file 
    # ---------------------------------------------
    def opendocx(self, filename):
        '''Opens a docx file and return a document XML tree.
        
        Example: converting a docx file to original XML
        filepath = ".../data"
        filename_docx = "filename.docx"
        docx_filename = os.path.join(filepath, filename_docx)
        document_org = opendocx(docx_filename)
        '''
        doc = zipfile.ZipFile(filename)
        xmlcontent = doc.read('word/document.xml')
        document = etree.fromstring(xmlcontent)
        return document
    
    
    
      
    # ---------------------------------------------
    # Complex text manipulation : replace, etc [To be completed for next version]
    # ---------------------------------------------
    # To be completed for next version
    
    

    # ---------------------------------------------
    # Save a docx file 
    # ---------------------------------------------
    def un_pass(self, main_path, full_paths_files, temp_paths_dir):

        for i in temp_paths_dir:
            search_path = f'{main_path}/{i}'
            
            if os.path.isdir(search_path) == False:
                full_paths_files.append(f'{main_path}/{i}')
            else:
                subfilenom = os.listdir(f'{main_path}/{i}')
                for j in subfilenom:
                    temp_paths_dir.append(f'{i}/{j}')
            temp_paths_dir.remove(i)
            
        return full_paths_files, temp_paths_dir 


    def sel_section(self, text, el_st, el_end):
        ind_st = text.find(el_st)
        ind_end = text.find(el_end)
        content = text[ind_st:ind_end]
        return content
        
        
    def savedocx_ver_fichier(self, filename, root_dir, desired_output_docx_name, doc_finale):
        
        # loading the temp.zip and creating a zip object
        with zipfile.ZipFile(filename, 'r') as zObject:
            # Extraction location
            extract_path = root_dir+'/temp'
            zObject.extractall(path=extract_path)
        
        import xml.etree.ElementTree as gfg
        from bs4 import BeautifulSoup
        from lxml.etree import tostring
        
        # ---------------------------------------------------
        # root_dir = le reporitoire ou vous souhaitez (ie: root_dir='/directory/where/the/docx_file/is/located')
        # desired_output_docx_name = le nom de fichier que vous desirez (ie: desired_output_docx_name = 'output.docx')
        
        # ---------------------------------------------------
        
        # [0] Créer un fichier vide, remplir le zip file correctement et inserer l'information de body que vous avez changé
        output = os.path.join(root_dir, desired_output_docx_name)
        docxfile = zipfile.ZipFile(output, mode='w', compression=zipfile.ZIP_DEFLATED)

        # [1] Verification uniquement : Verifier que le docxfile, type zipfile.ZipFile, est vide
        # print('type: ', type(docxfile))
        # print('infolist : ', docxfile.infolist())
        # print('printdir : ', docxfile.printdir())
        # print('namelist : ', docxfile.namelist())

        # [2] Obtenir toutes paths pour le dummy_zip_fichier 
        main_path = f'{root_dir}temp'
        listes_de_fichiers = os.listdir(main_path)
        full_paths_files = []
        temp_paths_dir = listes_de_fichiers
        while any(temp_paths_dir):
            full_paths_files, temp_paths_dir = self.un_pass(main_path, full_paths_files, temp_paths_dir)
        
        cles = ['document', 'coreprops', 'appprops', 'fontTable', 'styles', 'contenttypes', 'settings', 'wordrelationships', 'rels']
        values0 = ['word/document.xml', 'docProps/core.xml', 'docProps/app.xml',
                  'word/fontTable.xml', 'word/styles.xml', 
                 '[Content_Types].xml', 'word/settings.xml', 'word/_rels/document.xml.rels',
                  '_rels/.rels']
        values = [f'{root_dir}temp/{i}' for i in values0]
        # -------------------

        # -------------------
        # Prendez des informations de document changé : body text, 'word/fontTable.xml', 'word/styles.xml',
        inner_html_bytes = tostring(doc_finale)
        # type(inner_html) = bytes
        inner_html_str = inner_html_bytes.decode("utf-8") 

        content_finale = self.sel_section(inner_html_str, '<w:body>', '</w:body>')
        # -------------------

        # -------------------
        # [3] Mettez des valeurs cles et values dans XML
        # Definer la racine element d'arbre
        root = gfg.Element("docx_format")
        
        # Definer des sous elements d'arbre
        for ind, cle_elm in enumerate(cles):
            m1 = gfg.Element(cle_elm)
            root.append(m1)
            subpath = values0[ind]
            b1 = gfg.SubElement(root, subpath)
            file2open = f'{root_dir}temp/{subpath}'
            
            with open(file2open, 'r') as f:
                data = f.read()
            
            # IMPORTANT : Faites à jour votre docx avec vos changements
            if cle_elm == 'document':
                content = self.sel_section(data, '<w:body>', '</w:body>')
                data = data.replace(content, content_finale)
                
            # Enregister des donnes (string XML) de fichier    
            b1.text = data

        tree = gfg.ElementTree(root)
        
        # Index le objet XML
        text_nom = []
        tag_cle = []
        text_value = []
        for ind, child in enumerate(root):
            if ind % 2 != 0:
                # Le impair 'child.tag' sont le nom de l'SubElement (on veut le valueur de nom de SubElement)
                tag_cle.append(child.tag)
                text_value.append(child.text)
            else:
                # Le pair 'child.tag' sont le nom de l'Elément
                text_nom.append(child.tag)
        # -------------------

        # Créez et chargez des dossiers/fichiers XML dans le zipfile document docxfile; le docx fichiers est composé des fichiers zip
        for ind, val in enumerate(tag_cle):
            docxfile.writestr(val, text_value[ind])
        
        # Enregistez le fichier docx à le reporitoire que vous avez specifié     
        docxfile.close()
        
        # -------------------

	# Remove unzip temp folder
	shutil.rmtree(extract_path)

        return
