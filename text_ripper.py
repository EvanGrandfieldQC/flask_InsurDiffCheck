# importing required modules
import PyPDF2
import argparse
import difflib

parser = argparse.ArgumentParser(description="provide pdf for text ripper")
parser.add_argument("pdf")

args = parser.parse_args()
pdf = args.pdf

print("ripping text from {0}.".format(pdf))

# creating a pdf file object
pdfFileObj = open(pdf, "rb")

# creating a pdf reader object
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

# printing number of pages in pdf file
print(pdfReader.numPages)

text_name = pdf.split(".")[0]
text_name_second = pdf.split(".")[1]

new_file = open("{0}.txt".format(text_name), "w")

for i in range(0, 30):
    try:
        print(i)
        pageObj = pdfReader.getPage(i)
        # extracting text from page
        pageText = pageObj.extractText()
        new_file.write(pageText)
    except IndexError:
        break
print("exit loop")

pdfFileObj.close()
new_file.close()
