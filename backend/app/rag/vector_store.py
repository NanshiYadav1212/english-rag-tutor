import os, pickle, faiss

def _paths(user_id,course_id):
    base = f"vector_db/user_{user_id}/course_{course_id}"
    os.makedirs(base,exist_ok=True)
    return f"{base}/index.faiss", f"{base}/chunks.pkl"
    
def save_index(index, chunks,user_id,course_id):
    i,c = _paths(user_id,course_id)
    faiss.write_index(index,i)
    pickle.dump(chunks,open(c,"wb"))

def load_index(user_id,course_id):
    i,c = _paths(user_id,course_id)
    return faiss.read_index(i), pickle.load(open(c,"rb"))
