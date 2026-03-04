from collections import defaultdict, deque

memory = defaultdict(lambda:deque(maxlen=6))

def add(user,course,role,msg):
    memory[f"{user}-{course}"].append({"role":role, "msg":msg})
    
def get(user,course):
    return list(memory[f"{user}_{course}"])