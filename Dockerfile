FROM resin/raspberrypi3-python:3

ADD  requirements.txt requirements.txt
RUN  pip install -r   requirements.txt

ADD mcp.py    mcp.py
ADD templates templates

CMD ["python","-u","mcp.py"]
