import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
import chromadb

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

load_dotenv()

st.set_page_config(
    page_title="RAG Raspberry Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 RAG Raspberry Assistant")
st.caption(
    "Consulta documentación técnica con contexto e imágenes"
)


# memoria del chat
if "messages" not in st.session_state:
    st.session_state.messages=[]


embeddings=OpenAIEmbeddings()

client_db=chromadb.PersistentClient(
    path="./chroma_db"
)

db=Chroma(
    client=client_db,
    collection_name="langchain",
    embedding_function=embeddings
)

client=OpenAI()



# historial
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.write(msg["content"])

        if "sources" in msg:

            with st.expander("📄 Fuente e imagen relacionada"):

                shown_pages=set()

                for s in msg["sources"]:

                    page_key=(
                        f"{s['document']}_{s['page']}"
                    )

                    if page_key in shown_pages:
                        continue

                    shown_pages.add(page_key)

                    st.write(
                        f"📄 {s['document']}"
                    )

                    st.write(
                        f"Página: {s['page']}"
                    )

                    if s["image"]:

                        st.image(
                            s["image"],
                            width=600
                        )



question=st.chat_input(
    "Escribe una pregunta..."
)


if question:

    st.session_state.messages.append(
        {
            "role":"user",
            "content":question
        }
    )


    with st.chat_message("user"):

        st.write(question)



    docs=db.similarity_search(
        question,
        k=3
    )



    context=""

    sources=[]

    used_images=set()



    for d in docs:

        text=d.page_content.strip()

        context+=text+"\n\n"



        image=None

        images=d.metadata.get(
            "images",
            ""
        )


        if images and images!="No image":

            imgs=images.split(",")


            best=None


            for img in imgs:

                img=img.strip()

                if (
                    img
                    and img not in used_images
                ):

                    best=img
                    break


            if best:

                image=best

                used_images.add(best)



        sources.append(
            {
                "document":
                d.metadata.get(
                    "document",
                    "desconocido"
                ),

                "page":
                d.metadata.get(
                    "page",
                    "?"
                ),

                "image":image
            }
        )



    prompt=f"""

Eres un experto en:

-Raspberry Pi
-electrónica
-Arduino
-programación
-documentación técnica
-hardware

REGLAS IMPORTANTES:

1. Usa primero la información recuperada del PDF.

2. Si el PDF tiene información parcial:
completa usando conocimiento técnico.

3. Si el usuario hace preguntas básicas:

¿qué es Raspberry Pi?

¿qué significa GPIO?

¿qué es un cable USB?

Responde normalmente usando razonamiento.

4. NO respondas:

"No encontré información"

o

"No tengo suficiente contexto"

a menos que realmente sea imposible.

5. Prioriza resolver la necesidad real del usuario.

6. Si ves varias fuentes mezcladas:
elige las más coherentes.

7. Ignora información repetida.

8. Responde de manera natural y útil.

9. Explica sencillo.

10. Si una imagen aparece asociada,
asume que puede ser una referencia visual
aproximada del tema.

11. Nunca menciones que estás usando un PDF.

12. Si la pregunta requiere explicar conceptos,
hazlo aunque no aparezcan exactamente escritos.

CONTEXTO:

{context}


PREGUNTA:

{question}

"""



    response=client.chat.completions.create(

        model="gpt-4o",

        temperature=0.3,

        messages=[

            {
                "role":"system",
                "content":"Eres un experto técnico."
            },

            {
                "role":"user",
                "content":prompt
            }

        ]
    )



    answer=(
        response
        .choices[0]
        .message
        .content
    )



    st.session_state.messages.append(

        {
            "role":"assistant",
            "content":answer,
            "sources":sources
        }

    )


    st.rerun()