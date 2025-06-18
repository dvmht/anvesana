FROM pytorch/pytorch:2.7.1-cuda12.8-cudnn9-runtime

RUN useradd -m -u 1000 user
USER user

WORKDIR /src

RUN pip install uv

COPY --chown=user pyproject.toml /src/
COPY --chown=user uv.lock /src/

RUN uv pip compile pyproject.toml -o requirements.txt \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir sentence-transformers

COPY --chown=user . /src/

RUN pip install --no-cache-dir -e .
    
ENV PYTHONUNBUFFERED=1

EXPOSE 7860

CMD ["python", "app/main.py"]
