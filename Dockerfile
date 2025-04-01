FROM python:3
WORKDIR /app

# Currently, there is nothing in requirements.txt, but like, just in case something gets added, that can be done here
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD [ "python", "./grader.py" ]