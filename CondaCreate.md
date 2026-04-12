conda env create -f env/environment.yml -p fastapi-env
conda activate fastapi-env
conda remove -p fastapi-env

uvicorn main:app --reload
sudo kill -9 12345

http://127.0.0.1:8000/docs

python -m uvicorn OPE_DBSQLite.api:app --reload --port 8000

curl -X POST http://127.0.0.1:8000/xyz/SCHE \
  -H "Content-Type: application/json" \
  -d '{
    "node_uuid": "11111111-1111-1111-1111-111111111111",
    "attribute_id": 1,
    "value": "Initial schema value"
  }'

curl http://127.0.0.1:8000/xyz/SCHE

curl -X PUT http://127.0.0.1:8000/xyz/SCHE/<UUID> \
  -H "Content-Type: application/json" \
  -d '{
    "node_uuid": "11111111-1111-1111-1111-111111111111",
    "attribute_id": 1,
    "value": "Updated schema value"
  }'

curl -X POST http://127.0.0.1:8000/xyz/SCHE \
  -H "Content-Type: application/json" \
  -d '{
    "node_uuid": "22222222-2222-2222-2222-222222222222",
    "attribute_id": 1,
    "value": null
  }'