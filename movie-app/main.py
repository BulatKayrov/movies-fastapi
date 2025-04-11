import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title='Movies',
    version='1.0',
    description='Movie app',
    docs_url='/docs',
)

if __name__ == '__main__':
    uvicorn.run(app)
