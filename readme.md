pip freeze > requirements.txt
pip install -r requirements.txt


# build docker image api-base-image
docker build -t api-base-image .

# run images
docker run -d --restart always \
  -v "D:/DNC/thuctapthaykhoi/docker-demo/crawl_data/data":/_app_/crawl_data/data \
  --name api-base-container \
  -p 55006:60074 \
  api-base-image