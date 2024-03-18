FROM python:latest

# Create app directory
WORKDIR /app

# Copy the files


COPY . .

#install the dependecies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5006
ENTRYPOINT ["python", "app.py"]