FROM python:3
ADD test.py /
RUN pip install nltk
CMD [ "python", "./test.py" ]