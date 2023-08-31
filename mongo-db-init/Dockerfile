# FROM mongo

# COPY init.json /init.json
# CMD mongoimport --host mongodb --db reach-engine --collection MyDummyCollection --type json --file /init.json --jsonArray

FROM mongo:latest

COPY ./0-init-usage-stats /docker-entrypoint-initdb.d/0-init-usage-stats