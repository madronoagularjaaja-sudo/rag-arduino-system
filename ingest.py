import fitz
import os
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.documents import Document

load_dotenv()

PDF_FOLDER="data/pdfs"
IMAGE_FOLDER="extracted_images"

os.makedirs(IMAGE_FOLDER,exist_ok=True)

docs=[]

for pdf_file in os.listdir(PDF_FOLDER):

    if not pdf_file.endswith(".pdf"):
        continue

    pdf_path=os.path.join(
        PDF_FOLDER,
        pdf_file
    )

    print(f"\nProcesando {pdf_file}")

    pdf=fitz.open(pdf_path)

    for page_num in range(len(pdf)):

        page=pdf[page_num]

        text=page.get_text()

        image_list=page.get_images(full=True)

        image_paths=[]

        for img_index,img in enumerate(image_list):

            try:

                xref=img[0]

                base_image=pdf.extract_image(xref)

                image_bytes=base_image["image"]

                image_ext=base_image["ext"]

                width=base_image.get("width",0)
                height=base_image.get("height",0)

                # ignorar mini iconos
                if width < 60 or height < 60:
                    continue

                image_name=(
                    f"{pdf_file}_p{page_num+1}_{img_index}.{image_ext}"
                )

                image_path=os.path.join(
                    IMAGE_FOLDER,
                    image_name
                )

                with open(image_path,"wb") as f:
                    f.write(image_bytes)

                image_paths.append(image_path)

            except Exception as e:
                print(e)

        docs.append(
            Document(
                page_content=text,
                metadata={
                    "document":pdf_file,
                    "page":page_num+1,
                    "images":",".join(image_paths) if image_paths else "No image",
                    "image_count":len(image_paths)
                }
            )
        )

print("Separando chunks...")

splitter=RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks=splitter.split_documents(docs)

print("Creando embeddings...")

embeddings=OpenAIEmbeddings()

db=Chroma.from_documents(
    chunks,
    embeddings,
    persist_directory="chroma_db"
)

print("LISTO")
print(f"Chunks:{len(chunks)}")