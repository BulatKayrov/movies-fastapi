import uvicorn
from fastapi import FastAPI, Request

app = FastAPI(
    title='Movies',
    version='1.0',
    description='Movie app',
    docs_url='/docs',
)


@app.get('/')
async def root(request: Request):
    path = request.url.replace(path='/docs')
    return {'docs': path}

if __name__ == '__main__':
    uvicorn.run(app)
