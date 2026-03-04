# from app.rag.vector_store import load_index
# from app.memory.chat_memory import add, get
# from app.rag.llm import generate
# from app.rag.prompts import qna_prompt
# from app.rag.embeddings import get_embedder

# embedder = get_embedder()

# def ask_rag(user_id, course_id, question):
#     index, chunks = load_index(user_id, course_id)
#     q_emb = embedder.encode([question]).astype("float32")
#     _, ids = index.search(q_emb, 3)
#     context = "\n".join(chunks[i] for i in ids[0])

#     history = get(user_id, course_id)
#     prompt = qna_prompt(context, question, history)
#     answer = generate(prompt)

#     add(user_id, course_id, "user", question)
#     add(user_id, course_id, "assistant", answer)

#     return answer



from app.rag.vector_store import load_index
from app.memory.chat_memory import add, get
from app.rag.llm import generate
from app.rag.prompts import qna_prompt
from app.rag.embeddings import get_embedder

embedder = get_embedder()

def ask_rag(user_id, course_id, question):
    index, chunks = load_index(user_id, course_id)
    q_emb = embedder.encode([question]).astype("float32")
    _, ids = index.search(q_emb, 3)
    context = "\n".join(chunks[i] for i in ids[0])

    history = get(user_id, course_id)
    prompt = qna_prompt(context, question, history)
    answer = generate(prompt)

    add(user_id, course_id, "user", question)
    add(user_id, course_id, "assistant", answer)

    return answer
