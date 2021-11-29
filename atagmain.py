# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 22:19:31 2021

@author: rkasumi87
"""
import sys
import os
import argparse
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Table, TableStyle, Image
from reportlab.lib.units import cm

def main(argv):
    #Opens AprilTag File
    linklist = []
    parser = argparse.ArgumentParser(description="Usage: python atagmain.py -i <input file> -l <list of links>")
    parser.add_argument("-i", "--tag_folder", dest='tagfolder', 
                        help='File name containing AprilTag images', required = True)
    
    parser.add_argument("-l", "--list", nargs="+", dest ='linklist', type=int,
                        help='List of links to generate AprilTags for. Ex: 1 5 3', required = True)
    
    args = parser.parse_args()
    tagfolder = args.tagfolder
    image_list = os.listdir(tagfolder)
    linklist = args.linklist
    
    #print(image_list[:20])
    
    canvas = Canvas('tags.pdf', pagesize = A4, bottomup=0)
    
    im_list0 = []
    num_list0 = []
    tag_data0 = []
    
    im_list1 = []
    num_list1 = []
    tag_data1 = []
    
    for i in linklist:
        #Clear im_list0, num_list0, and tag_data0
        im_list0.clear()
        num_list0.clear()
        tag_data0.clear()
        
        #Clear im_list1, num_list1, tag_data1
        im_list1.clear()
        num_list1.clear()
        tag_data1.clear()
        for a in range(12 * (i), 12 * i + 6):
            
            #Create list of images and numbers for first strip
            im0 = Image(os.path.join(tagfolder, image_list[a]))
            im0.drawHeight = 2 * cm
            im0.drawWidth = 2 * cm
            im_list0.append(im0)
            
            num_list0.append(str(a))
            
            #Create list of images and numbers for second strip
            im1 = Image(os.path.join(tagfolder, image_list[a + 6]))
            im1.drawHeight = 2 * cm
            im1.drawWidth = 2 * cm
            im_list1.append(im1)
            
            num_list1.append(str(a + 6))
    
        #Append images and numbers of first strip
        tag_data0.append(im_list0)
        tag_data0.append(num_list0)
        
        #Append images and numbers of second strip
        tag_data1.append(im_list1)
        tag_data1.append(num_list1)
        
        #Format strip 1
        table0 = Table(tag_data0, colWidths = 55, rowHeights = 50)
        table0.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),                      #Horizontal center aligns all entities
            ('VALIGN', (0, 0), (-1, 0), 'CENTER'),                      #Vertical center aligns AprilTags
            ('BOTTOMPADDING', (0, 1), (-1, 1), 40),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.white),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
            ]))
        table0.wrapOn(canvas, 0, 0)
        table0.drawOn(canvas, 20, 210 * i + 30)
        
        #Format strip 2
        table1 = Table(tag_data1, colWidths = 55, rowHeights = 50)
        table1.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'CENTER'), 
            ('BOTTOMPADDING', (0, 1), (-1, -1), 40), 
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.white),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.white),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
            ]))
        table1.wrapOn(canvas, 0, 0)
        table1.drawOn(canvas, 20, 210 * i + 135)
        
        canvas.rect(350, 210 * i + 30, 55, 100)
        canvas.rect(350, 210 * i + 135, 55, 100)
            
    canvas.showPage()
    canvas.save()
    print("Successfully generated tags!")
     
if __name__ == "__main__":
    main(sys.argv)
