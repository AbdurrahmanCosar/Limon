FROM python:3.11.1

WORKDIR /usr/src/sscord

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8000

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "launcher.py"]
