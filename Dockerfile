FROM python:3.10.7-slim

WORKDIR /user/cpb/Desktop/cryptoc/cryp
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn","cryp.appss:app","--host","0.0.0.0","--port","8000"]