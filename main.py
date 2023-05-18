from fastapi import FastAPI
from typing import Dict, List
import crewl
import json

app = FastAPI()


@app.get("/")
def read_root():
    return {"msg": "早安"}


@app.get("/bookPage")
async def bookPage(urlObj: str) -> crewl.queryReturnType:
    print(urlObj)
    url = json.loads(urlObj).get('url')
    print(url)
    result: crewl.queryReturnType = crewl.simpleQuery(url=url)
    return result


@app.get("/query")
async def query(searchtype: str = 'all',
                search: str = '',
                title: str = '',
                author: str = '',
                url: str = '') -> crewl.queryReturnType:
    print(search)
    result: crewl.queryReturnType = crewl.simpleQuery(
        params={
            'newQuery': 'true',
            'searchtype': searchtype,
            'search': search,
            'title': title,
            'author': author
        })
    # print(result)
    return result


@app.get("/findBook")
async def findBook(urlObj: str):
    '''
    # Parameters
    ```javascript
    urlObj = JSON.stringify({ url: url })
    ```
    ```python
    urlObj = json.dumps({'url':url})
    ```

    
    # Responses 
    ## single book:

    ```json
    {'position', 'call_number', 'barcode', 'status'}

    [ 
        { 
            detail: [ '公館分館6F新類號專區', '312.32C 8866-6', 'BM0789936', '可外借' ] 
        } 
    ]
    ```

    ## multi books:

    ```json
    [
        {
            href: 'http://www.lib.ntnu.edu.tw/holding/doQuickSearch.jsp?action=view&param=%2Fsearch*cht%3F%2Ft%257Bu6F14%257D%257Bu7B97%257D%257Bu6CD5%257D%2Ft%257B214852%257D%257B21502c%257D%257B21472a%257D%2F1%252C24%252C31%252CB%2Fframeset%26FF%3Dt%7B214852%7D%7B21502c%7D%7B21472a%7D%261%252C%252C4',
            name: '圖說演算法 : 使用C# : 理解零負擔.採功能強大C#語言實作 / 吳燦銘, 胡昭民著',
            detail: [ '公館分館6F新類號專區', '312.32C 8866-6', 'BM0789936', '可外借' ]
        },
        {
            href: 'http://www.lib.ntnu.edu.tw/holding/doQuickSearch.jsp?action=view&param=%2Fsearch*cht%3F%2Ft%257Bu6F14%257D%257Bu7B97%257D%257Bu6CD5%257D%2Ft%257B214852%257D%257B21502c%257D%257B21472a%257D%2F1%252C24%252C31%252CB%2Fframeset%26FF%3Dt%7B214852%7D%7B21502c%7D%7B21472a%7D%262%252C%252C4',
            name: '圖說演算法 : 使用C語言 / 吳燦銘, 胡昭民著',
            detail: [ '公館分館6F新類號專區', '312.32C 8866-2', 'BM0736996', '可外借' ]
        },
        {
            href: 'http://www.lib.ntnu.edu.tw/holding/doQuickSearch.jsp?action=view&param=%2Fsearch*cht%3F%2Ft%257Bu6F14%257D%257Bu7B97%257D%257Bu6CD5%257D%2Ft%257B214852%257D%257B21502c%257D%257B21472a%257D%2F1%252C24%252C31%252CB%2Fframeset%26FF%3Dt%7B214852%7D%7B21502c%7D%7B21472a%7D%263%252C%252C4',
            name: '圖說演算法 : 使用Python / 吳燦銘, 胡昭民著',
            detail: [ '總館6F新類號專區', '312.32P999 8866 2018', 'BM0757623', '到期 09-02-23' ]
        },
        {
            href: 'http://www.lib.ntnu.edu.tw/holding/doQuickSearch.jsp?action=view&param=%2Fsearch*cht%3F%2Ft%257Bu6F14%257D%257Bu7B97%257D%257Bu6CD5%257D%2Ft%257B214852%257D%257B21502c%257D%257B21472a%257D%2F1%252C24%252C31%252CB%2Fframeset%26FF%3Dt%7B214852%7D%7B21502c%7D%7B21472a%7D%264%252C%252C4',
            name: '演算法 / Anany V. Levitin原著 ; 莊承翃譯.',
            detail: [ '公館分館', '000.5131 117', 'BM0474069', '可外借' ]
        }
    ]
    ```

    '''
    url = json.loads(urlObj).get('url')
    # print(url)
    result = crewl.findBook(url)
    return result


@app.get("/correction")
def correction(wrong_text: str):
    return crewl.correctWords(wrong_text)