FROM pytorch/pytorch:2.7.1-cuda12.8-cudnn9-runtime

WORKDIR /src

RUN pip install uv

COPY pyproject.toml /src/
COPY uv.lock /src/

RUN uv pip compile pyproject.toml -o requirements.txt \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir sentence-transformers

COPY . /src/

RUN pip install --no-cache-dir -e .
    
ENV PYTHONUNBUFFERED=1

EXPOSE 7860

CMD ["python", "app/main.py"]
