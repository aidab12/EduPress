FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /app

COPY ./ /app
RUN uv sync

CMD ["uv", "run", "python3", "manage.py", "runserver", "0:8000"]

# docker build -t online_pdp_image .
# docker run --name online_pdp_ct -p 8000:8000 -d online_pdp_image