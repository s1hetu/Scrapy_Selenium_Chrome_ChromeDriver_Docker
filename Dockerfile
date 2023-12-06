FROM python:3.8

WORKDIR /

RUN apt-get update && apt-get install -y curl

RUN curl -o chromedriver.zip 'https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip'
RUN unzip chromedriver.zip
RUN chmod +x /chromedriver
RUN rm /chromedriver.zip

RUN curl -o chrome-linux64.zip 'https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/114.0.5735.26/linux64/chrome-linux64.zip'
RUN unzip chrome-linux64.zip
RUN chmod +x /chrome-linux64
RUN rm chrome-linux64.zip

ADD lambda_function.py /lambda_function.py

RUN pip3 install selenium webdriver_manager scrapy

RUN apt-get update && apt-get install -y libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2

CMD ["python", "lambda_function.py"]


