#!/bin/bash

dir="$(dirname "$(dirname "$(readlink -f $0)")")/dynamodb"
archive_name="dynamodb.tar.gz"
jar_name="DynamoDBLocal.jar"

mkdir -p "${dir}"

(
    cd "${dir}"

    if [ ! -f "$archive_name" ]; then
        echo "Downloading archive..."
        curl -o "${archive_name}" "https://s3-us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_latest.tar.gz"
    fi

    if [ ! -f "${jar_name}" ]; then
        echo "Unpacking archive..."
        tar -xf "${archive_name}"
    fi

    echo "Running DynamoDB..."
    java -Djava.library.path=./DynamoDBLocal_lib -jar "${jar_name}" -sharedDb -port 3000
)

# vim: ts=4 sts=4 sw=4 expandtab
