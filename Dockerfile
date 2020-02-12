FROM python:3.7

ENV PYTHONPATH=":/auto_analys"

COPY . /auto_analys

CMD ["/bin/bash"]