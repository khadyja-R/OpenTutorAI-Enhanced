from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


memory = []

class Message(BaseModel):
 user_input: str

@app.post("/chat")
def chat(msg: Message):
	# stocker message
	memory.append(msg.user_input)

	# réponse simple
	response = f"I remember {len(memory)} messages. You said: {msg.user_input}"

	return {"response": response}