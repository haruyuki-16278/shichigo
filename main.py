import uvicorn
import datetime
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import sqlite3
import json

class Shichigo(BaseModel):
    poem: str
    writer: str

dbname = 'shichigo.db'
conx = sqlite3.connect(dbname)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# ページルーティング
@app.get('/', response_class=RedirectResponse)
async def page_redirect_index():
    return RedirectResponse('/compose')

@app.get('/compose', response_class=HTMLResponse)
async def page_compose(req: Request):
    return templates.TemplateResponse('compose.jinja.html', {'request': req})

@app.get('/appreciation', response_class=HTMLResponse)
async def page_appreciation(req: Request):
    return templates.TemplateResponse('appreciation.jinja.html', {'request': req})

# APIルーティング
@app.get('/shichigo', response_class=JSONResponse)
async def get_shichigo(timestamp: str = Query(default='0')):
    param = {
        'timestamp': timestamp
                        if timestamp != '0'
                        else datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    print(param)
    cur = conx.cursor()
    try:
        cur.execute(
            'SELECT * FROM shichigo\
                WHERE ts < ? \
                LIMIT 20',
            [param['timestamp']]
        )
        res = cur.fetchall()
        print(res)
        return json.dumps(res)
    except Exception as e:
        print(e)
        return {'error': 'E-001'}
    finally:
        cur.close()

@app.post('/shichigo')
async def post_shichigo(shichigo: Shichigo):
    cur = conx.cursor()
    try:
        cur.execute(
            'INSERT INTO shichigo(poem, writer)\
                VALUES(\
                    ?,\
                    ?\
                )',
            [shichigo.poem, shichigo.writer]
        )
        conx.commit()
        return {'message': 'success'}
    except Exception as e:
        return {'error': 'E-001'}
    finally:
        cur.close()

@app.get('/hc')
async def index():
    return {'message': 'Healty'}

def main() -> None:
    print('-------------------main-------------------')
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True, workers=2)

if __name__ == '__main__':
    main()