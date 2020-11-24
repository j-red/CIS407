from common import *
from PyPDF2 import PdfFileWriter, PdfFileReader
from tkinter import Tk, messagebox
from tkinter.filedialog import askopenfilename, askopenfilenames, asksaveasfile

# from pdfmanager import window

pdf = None
gPages = ""
pageBox = None
pageLbl = None

def sendExtractPages(junk):
    global gPages, pdf
    global pageBox, pageLbl


    pages = pageBox.get()

    pageBox.destroy()
    pageLbl.destroy()
    window.geometry(f"{width}x{height}")

    pagelistraw = pages.split(",")
    # pagelistraw = gPages.split(",")
    pagelist = []
    for p in pagelistraw:
        pagelist.append(p.strip())

    pagesToExtract = []

    for p in pagelist:
        try:
            pagesToExtract.append(int(p) - 1) # offset by 1
        except:
            # if a simple int conversion doesn't work, it's probably a page range
            pageRange = p.split("-")
            try:
                start = int(pageRange[0])
                end = int(pageRange[1])
                assert(start <= end)

                while (start <= end):
                    pagesToExtract.append(start - 1) # offset by 1
                    start += 1

            except:
                print(f"Error reading page range {pageRange}.")
                errString = f"Invalid input range '{pageRange}'."
                messagebox.showerror('Read Error', errString)
                return -1
    infile = PdfFileReader(pdf, 'rb')
    output = PdfFileWriter()

    numPages = infile.getNumPages()

    for i in pagesToExtract:
        if i < numPages:
            p = infile.getPage(i)
            output.addPage(p)
            # print(f"Adding page {i+1}")
        else:
            print(f"Page {i+1} out of range.")

    output_file = pdf.split(".pdf")[0] + "_" + pages + ".pdf"

    with open(output_file, 'wb') as f:
        output.write(f)
    print("Operation complete.")
    return 0

def extract(inputPdf=None, pages=None):
    """ Returns -2 if cancelled, -1 if error, 0 if successful. """
    global gPages
    global pageBox
    global pdf, pageLbl
    window.geometry(f"{largeWidth}x{height}")

    defaultfiles = [("PDF File", "*.pdf")]
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    # if inputPdf is None: # allow file list to be overriden by default
    pdf = askopenfilename(title="Select file:", filetypes=defaultfiles) # show an "Open" dialog box and return a file location string

    if pdf == "":
        print("Operation cancelled.")
        return -2

    if pages is None:
        # pages = input("Pages to extract (example: 1-3, 5, 8): ") # page numbering starts from 0

        # extractWindow = Toplevel(window)
        # popupWidth = 150
        # popupHeight = 100
        # extractWindow.title("Pages to extract")
        # extractWindow.resizable(width=False, height=False)
        # screenwidth = extractWindow.winfo_screenwidth()
        # screenheight = extractWindow.winfo_screenheight()
        # alignstr = '%dx%d+%d+%d' % (popupWidth, popupHeight, (screenwidth - popupWidth) / 2 + width, (screenheight - popupHeight) / 2)
        # extractWindow.geometry(alignstr)

        pageLbl = Label(window)
        pageLbl["fg"] = "#333333"
        pageLbl["text"] = "Input pages to extract."
        pageLbl.place(x=120,y=35, width=120, height=30)

        pageBox = Entry(window)
        pageBox["borderwidth"] = "1px"
        pageBox["fg"] = "#333333"
        pageBox["justify"] = "center"
        # pageBox["text"] = "INPUT"
        pageBox["validatecommand"] = "sendExtractPages"
        pageBox.place(x=125,y=70, width=100, height=30)

        window.bind("<Return>", sendExtractPages)

    gPages = pages


    # pagelistraw = pages.split(",")
    # pagelist = []
    # for p in pagelistraw:
    #     pagelist.append(p.strip())
    #
    # pagesToExtract = []
    #
    # for p in pagelist:
    #     try:
    #         pagesToExtract.append(int(p) - 1) # offset by 1
    #     except:
    #         # if a simple int conversion doesn't work, it's probably a page range
    #         pageRange = p.split("-")
    #         try:
    #             start = int(pageRange[0])
    #             end = int(pageRange[1])
    #             assert(start <= end)
    #
    #             while (start <= end):
    #                 pagesToExtract.append(start - 1) # offset by 1
    #                 start += 1
    #
    #         except:
    #             print(f"Error reading page range {pageRange}.")
    #             errString = f"Invalid input range '{pageRange}'."
    #             messagebox.showerror('Read Error', errString)
    #             return -1

    # print(f"Extracting pages {pagesToExtract} from {pdf}")
    # infile = PdfFileReader(pdf, 'rb')
    # output = PdfFileWriter()
    #
    # numPages = infile.getNumPages()
    #
    # for i in pagesToExtract:
    #     if i < numPages:
    #         p = infile.getPage(i)
    #         output.addPage(p)
    #         # print(f"Adding page {i+1}")
    #     else:
    #         print(f"Page {i+1} out of range.")
    #
    # output_file = pdf.split(".pdf")[0] + "_" + pages + ".pdf"
    #
    # with open(output_file, 'wb') as f:
    #     output.write(f)
    # print("Operation complete.")
    # return 0

if __name__ == "__main__":
    extract()
