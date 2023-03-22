from fastapi import FastAPI 
import crewl
import json

app = FastAPI()

@app.get("/")
def read_root():
	return {"msg": "早安"}

@app.get("/bookPage")
async def booksPage(urlObj:str):
	url=json.loads(urlObj).get('url')
	print(url)
	result = crewl.simpleQuery(url=url)
	return result

@app.get("/query")
async def query(searchtype: str = 'all',
					search: str = '',
					title: str = '',
					author: str = '',
					url: str = ''):
	result = ''
	print(search)
	result = crewl.simpleQuery(params={
		'newQuery': 'true',
		'searchtype': searchtype,
		'search': search,
		'title': title,
		'author': author
	})
	print(result)
	return {"result":result}

@app.get("/findBook")
async def findBook(urlObj:str):
	url=json.loads(urlObj).get('url')
	# print(url)
	result = crewl.findBook(url)
	return result