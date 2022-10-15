import pdfplumber

def scriptUpload(filePath):
    pdf_file = 'F:/MNF/project3'+filePath
    outputfile, ext = pdf_file.split(".")
    #outfile  = open('F:/MNF/project3'+filePath[:-3]+"txt", encoding="UTF-8", mode="w")
    #outfile1= open ("F:/MNF/project3/media/scripts/test_file.txt", "w")
    tables=[]
    mystr = []
    str1 = ""
    
    with pdfplumber.open(pdf_file) as pdf:
        #outfile.write(str(pdf.metadata))
        #outfile.write(str("\n"))
        page_text=[]
        pages = pdf.pages
        prev_top=0
        prev_bottom=0
        for i,pg in enumerate(pages):
            page_text=pages[i].extract_words(x_tolerance=3, y_tolerance=3, keep_blank_chars=False)    
            #outfile1.write(str(page_text))
            #outfile1.write("\n")
            prev_end_margin =0
            for a_text in page_text:
                space_ct = int(a_text["x0"]/8)
                end_margin = int(a_text["x1"]/8)
                top = a_text["top"]
                bottom= a_text["bottom"]
                if ( top -prev_bottom >= 12):
                    #outfile.write("\n")
                    mystr.append('\n')
                if (prev_bottom != bottom):
                    #outfile.write("\n")
                    mystr.append('\n')
                    #new_text = a_text["text"].rjust(space_ct +len(a_text["text"]))
                    new_text =  str(a_text["text"]).replace(str(a_text["text"]), "\xa0"*space_ct +str(a_text["text"]))
                elif (space_ct - prev_end_margin > 2):
                    #new_text = str(a_text["text"]).replace(str(a_text["text"]), str(a_text["text"])+ ("\xa0"*space_ct)+("\r"*prev_end_margin))
                    new_text = a_text["text"].rjust(len(a_text["text"])+ space_ct-prev_end_margin)
                else:
                    new_text = a_text["text"].rjust(len(a_text["text"])+1)
                    #new_text = str(a_text["text"]).replace(str(a_text["text"]),"\xa0"+str(a_text["text"]))
                    
                #outfile.write(str(new_text))
                mystr.append(str(new_text))
                prev_top =top
                prev_bottom = bottom
                prev_end_margin = end_margin


    for i in mystr:
        str1 += i 
    
    return str1
