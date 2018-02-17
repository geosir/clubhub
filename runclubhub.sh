docker build -t clubhub .

# Survive Migrations
docker exec clubhub cp -r /opt/clubhub/main/migrations /opt/staging/

# Replace Running Instance
docker rm -f clubhub
docker run -d --name clubhub -v $(pwd)/staging:/opt/staging -v $(pwd)/media:/opt/media --link clubhubdb:postgres clubhub

# Survive Migrations
docker exec clubhub mv /opt/staging/migrations /opt/clubhub/main/
docker exec clubhub /bin/bash /opt/clubhub/migrate.sh

docker inspect clubhub