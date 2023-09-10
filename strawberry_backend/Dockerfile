FROM adefe/strawberry_env:aerial

WORKDIR /home

COPY . /home

CMD ["uvicorn", "--app-dir", ".", "--host", "0.0.0.0", "--port", "14565", "routers.server:app"]
