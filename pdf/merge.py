""" Merge PDF documents into a single document. By default, the files are
    merged in the order that they were selected. """

# https://stackoverflow.com/questions/3579568/choosing-a-file-in-python-with-simple-dialog

# import PyPDF2
from PyPDF2 import PdfFileMerger
# from tkinter import Tk, messagebox
# from tkinter.filedialog import askopenfilename, askopenfilenames, asksaveasfile

# from pdfmanager import debugLbl

def merge(pdfs=None):
    defaultfiles = [("PDF File", "*.pdf")]
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    if pdfs is None: # allow file list to be overriden by default
        pdfs = askopenfilenames(title="Select files to merge:", filetypes=defaultfiles) # show an "Open" dialog box and return a list of file location strings

    # print(type(pdfs))

    if pdfs == "":
        print("Operation cancelled.")
        # debugLbl["text"] = "Operation cancelled."
        return -2

    print(f"Merging: {pdfs}")

    # merger = PdfFileMerger()
    merger = PdfFileMerger(strict=False) # Enforcing strict=False allows us to avoid the 'xref not zero-indexed' error from scanned documents.

    for pdf in pdfs:
        try:
            merger.append(pdf)
        except:
            print(f"Error merging '{pdf}'. Operation cancelled.")
            # debugLbl["text"] = f"Error merging '{pdf}'. Operation cancelled."
            errString = f"Error reading file '{pdf}'. Make a copy by opening it in another program, then running 'File -> Save As', then try again."
            messagebox.showerror('Read Error', errString)
            return -1

    file = asksaveasfile(title="Output File:", initialfile = "Merged result", filetypes = defaultfiles, defaultextension = defaultfiles)
    if file is None: # asksaveasfile return `None` if dialog closed with "cancel".
        print("Operation cancelled.")
        # debugLbl["text"] = "Operation cancelled."
        return -2
    file.close()

    output = str(file).split("'")[1] # extract filename from file object
    try:
        merger.write(output)
    except:
        print("Error writing output file. Operation cancelled.")
        errString = f"Error writing output file. Try again?"
        messagebox.showerror('Write Error', errString)
        return -1

    print(f"Wrote '{output}'.")
    merger.close()
    return 0

if __name__ == "__main__":
    merge()
