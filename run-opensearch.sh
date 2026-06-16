#!/bin/bash

echo "Ensuring the docker command is available."
echo "Ensuring running the ./generate-certs.sh script by yourself firstly."

echo "Running the OpenSearch Docker Compose is started."

sudo sysctl -w vm.max_map_count=512000

if [[ $? != 0 ]]; then
    echo "It's failed to generate certs."
    exit 1;
fi;

docker compose down
docker compose up -d

echo "Wait for 30 seconds."
sleep 60

echo "Enabling the securityadmin plugin..."
docker compose exec os01 bash -c "chmod +x plugins/opensearch-security/tools/securityadmin.sh && bash plugins/opensearch-security/tools/securityadmin.sh -cd config/opensearch-security -icl -nhnv -cacert config/certificates/ca/ca.pem -cert config/certificates/ca/admin.pem -key config/certificates/ca/admin.key -h localhost"

echo "Running the OpenSearch Docker Compose is done."
