import uvicorn
import datetime
from fastapi import FastAPI, Query, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import sqlite3

SHICHIGO_COLUMNS = ['id', 'poem', 'writer', 'fav', 'replies', 'ts']
PAGING_AMOUNT = 10

dbname = 'shichigo.db'
conx = sqlite3.connect(dbname)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# 静的ファイル配信
app.mount(
    '/templates/static',
    StaticFiles(directory='templates/static'),
    name='static'
)

# ページルーティング
@app.get('/', response_class=RedirectResponse)
async def page_redirect_index():
    return RedirectResponse('/compose')

@app.get('/compose', response_class=HTMLResponse)
async def page_compose(req: Request):
    return templates.TemplateResponse(
        'compose.jinja.html',
        {
            'succeed': False,
            'failed': False,
            'request': req
        }
    )

@app.get('/appreciation', response_class=HTMLResponse)
async def page_appreciation(req: Request, timestamp: str = Query(default='0')):
    param = {'timestamp': timestamp
                            if timestamp != '0'
                            else datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    cur = conx.cursor()
    try:
        cur.execute(
            'SELECT * FROM shichigo\
                WHERE ts < ? \
                ORDER BY id DESC\
                LIMIT ?',
            [param['timestamp'], PAGING_AMOUNT]
        )
        res = cur.fetchall()
        shichigos = [dict(zip(SHICHIGO_COLUMNS, shichigo)) for shichigo in res]
        print(shichigos, len(shichigos))
        return templates.TemplateResponse(
            'appreciation.jinja.html',
            {
                'request': req,
                'shichigos': shichigos,
                'available_shichigoes': len(shichigos) > 0,
                'available_next': len(shichigos) >= PAGING_AMOUNT,
                'last_poem_created_at': shichigos[-1]['ts'] if len(shichigos) > 0 else 0
            }
        )
    except Exception as e:
        print(e)
        print(e.__traceback__)
    finally:
        cur.close()

# APIルーティング
@app.post('/shichigo', response_class=HTMLResponse)
async def post_shichigo(req: Request, poem: str = Form(), writer: str = Form()):
    cur = conx.cursor()
    try:
        cur.execute(
            'INSERT INTO shichigo(poem, writer)\
                VALUES(\
                    ?,\
                    ?\
                )',
            [poem, writer]
        )
        conx.commit()
        return templates.TemplateResponse(
            'compose.jinja.html',
            {
                'succeed': True,
                'failed': False,
                'request': req
            }
        )
    except Exception as e:
        print(e)
        return templates.TemplateResponse(
            'compose.jinja.html',
            {
                'succeed': False,
                'failed': True,
                'request': req
            }
        )
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