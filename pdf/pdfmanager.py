from merge import *
from extract import *


mergeBtn = Button(window, text="Merge PDFs", bg="lightgray", fg="black", command=merge, font=("Bahnschrift SemiBold", 12))
mergeBtn.config(anchor=NW)
mergeBtn.place(x=10,y=65,width=100,height=32)

extractBtn = Button(window, text="Extract Pages", bg="lightgray", fg="black", command=extract, font=("Bahnschrift SemiBold", 11))
extractBtn.config(anchor=NW)
extractBtn.place(x=8,y=100,width=104,height=32)

debugLbl = Label(window, font=("Bahnschrift SemiBold", 10))
# ft = tkFont.Font(family='Times',size=10)
# debugLbl["font"] = font
# debugLbl["fg"] = "#333333"
debugLbl["justify"] = "center"
# debugLbl["text"] = "Output log."
debugLbl["text"] = ""
debugLbl.config(anchor=SE)
debugLbl.place(x=140,y=100,width=100,height=30)

window.mainloop()
