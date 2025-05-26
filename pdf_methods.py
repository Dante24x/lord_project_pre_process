import fitz


# We make a list of chapters with starting and ending pages from the document outline
class Pages_List_Item:
    def __init__(self, title, start, end):
        self.title = title
        self.start = start
        self.end = end


# Chapter items, each one has the text of a chapter inside
class Chapter:
    def __init__(self, title, text):
        self.title = title
        self.text = text


# Convert the pdf to txt by chapter, so we can run it once at the start
def pdf_to_txt(path):
    path = "fellowship.pdf"
    chapters = get_chapters_from_pdf(path)
    write_chapters_on_txt_files(chapters)


# Create txt files for each chapter
def write_chapters_on_txt_files(chapters):
    for chapter in chapters:
        with open(chapter.title + ".txt", "w", encoding='utf-8') as text_file:
            text_file.write(chapter.text)


# Get the list of chapters with their titles and texts
def get_chapters_from_pdf(pdf_path):
    # 1.Get the pdf and read it with the fitz library
    pdf_document = fitz.open(pdf_path)
    # 2.Extract each section pages from the outline using section_list method
    chapter_list = get_section_list(pdf_document)
    chapters = []
    i = 1
    for chapter in chapter_list:
        # 3.Make a list of Chapter items and keep the story chapters only, they start with the word "Chapter"
        if chapter.title.startswith("Chapter"):
            # 4.Create the txt file title from the chapter title + the number of order and keep the clean text
            title = get_clean_text(str(i) + "_" + chapter.title.split(":")[1].strip().replace(" ", "_"))
            text = ""
            for page_number in range(chapter.start - 1, chapter.end):
                # 5.Insert in each chapter item the title and the text of the pages
                page_text = pdf_document[page_number].get_text("text") + "\n"
                # 6.Cut the first two lines that have the chapter name and page number
                page_text = page_text.split("\n", 2)[2]
                # 7.Keep the clean text
                text += get_clean_text(page_text)
            # 8.Remove empty lines
            # text = "".join([s for s in text.strip().splitlines(True) if s.strip()])
            chapters.append(Chapter(title, text))
            i = i + 1
    # 9.Return the chapters
    return chapters


def get_section_list(pdf_document):
    # 1.Get the Table of Contents (Outline)
    outline = pdf_document.get_toc()
    # 2.List to store chapter details
    pages_sections_list = []
    # 3.Extract chapter names, start pages, and compute end pages
    for i in range(len(outline)):
        level, title, start_page = outline[i]  # Get chapter level, name, and start page
        # 4.Determine the end page (the page before the next chapter starts)
        if i < len(outline) - 1:
            _, _, next_start_page = outline[i + 1]
            end_page = next_start_page - 1
        else:
            # 5.Last chapter ends at the last page
            end_page = pdf_document.page_count
        pages_sections_list.append(
            Pages_List_Item(title, start_page, end_page))
    return pages_sections_list


# Clean the text from ligatures, accent marks and non-text characters
def get_clean_text(text):
    # 1. Replace ligatures with their letter counterparts
    text = text.replace("\ufb01", "fi")
    text = text.replace("\ufb02", "fl")
    text = text.replace("\u0131", "i")
    # 2. Remove the accent marks that Tolkien use in his elvish languages to make the text more simple
    text = text.replace("´", "")
    text = text.replace("ˆ", "")
    text = text.replace("¨", "")
    # 3. remove the "*" char that is not used in text
    text = text.replace("*", "")
    # 4. replace the "——" and "—" char sequences with suspension points "..." that are used in these cases
    text = text.replace("——", "...")
    text = text.replace("—", "...")
    return text
