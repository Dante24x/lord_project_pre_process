import chunk_methods
import labeled_dataset_sampling

# The whole process from pdf to xlsx files with unprocessed chunks without labeling
chunk_methods.create_txt_and_excel_for_each_chapter()

# After the manual labeling and annotating process, we sample the Full Dataset
labeled_dataset_sampling.create_fellowship_sample()




