conda env create -f env/environment.yml -p fastapi-env
conda activate fastapi-env
conda remove -p fastapi-env

uvicorn main:app --reload
sudo kill -9 12345

http://127.0.0.1:8000/docs