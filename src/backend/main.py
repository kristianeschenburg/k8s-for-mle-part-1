import os
import time

import fastapi
from fastapi import status, HTTPException
import pandas as pd
import uvicorn

CACHED = False
SLEEP_DURATION = int(os.environ.get('SLEEP_DURATION', 10))


def long_function():
    global CACHED
    if not CACHED:
        time.sleep(SLEEP_DURATION)
        CACHED = True
    return True

        
app = fastapi.FastAPI(root_path="/backend")


@app.get('/healthz')
def health_check():
    return "OK", 200

@app.get('/ready')
def ready_check():
    long_function()
    return 'OK'

@app.get('/age')
def get_age(name: str):

    data_file = os.environ.get('DATA_FILE')

    df = pd.read_csv(data_file)

    is_name = df.loc[df['first_name'] == name]
    if is_name.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Name {name} not found"
        )

    return is_name.to_dict(orient='records')


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)