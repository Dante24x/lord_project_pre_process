import chunk_methods
import pdf_methods

# The whole process from pdf to xlsx files with unprocessed chunks without labeling

# Convert the pdf to txt by chapter and then to excel
path = "fellowship.pdf"

chapters = pdf_methods.get_chapters_from_pdf(path)

pdf_methods.write_chapters_on_txt_files(chapters)

chunk_methods.get_excel_files(chapters)

