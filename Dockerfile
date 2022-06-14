#  Base image
FROM python:3.10-slim AS compile-image
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

# Building business logic
COPY requirements.txt .
RUN pip install --user -r requirements.txt

WORKDIR /src
COPY src .
RUN rm -r test 

# Production image
FROM python:3.10-slim AS build-image
COPY --from=compile-image /root/.local /root/.local
COPY --from=compile-image /src /root/.local

# Starting the application
CMD [ "python","root/.local/main.py"]