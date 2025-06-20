from fastapi import FastAPI
from Item import Item
app = FastAPI()
WhitePencil = Item(name="Pencil", description="The thing for writing", price=.5, tax=0)
items: list[Item] = [WhitePencil]

@app.get("/users")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id,
            "item": items[item_id],
            "name": items[item_id].name,
            "description": items[item_id].description,
            "price": items[item_id].price,
            "tax": items[item_id].tax}