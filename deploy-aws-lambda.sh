#!/bin/bash
set -xeu

# 引数チェック
if [ $# -ne 4 ]; then
  echo "pre: you need to install aws-cli and setup temporary lambda function"
  echo "params: 1.lambda-name 2.region 3.alias 4.bucket" 1>&2
  echo "ex1) ./deploy.sh covid19chiba-tool ap-northeast-1 test covid19chiba-deploy" 1>&2
  exit 1
fi
FUNCTION_NAME=$1
REGION_NAME=$2
ALIAS_NAME=$3
BUCKET_NAME=$4

# 定数定義
CURRENT_PATH=$(pwd)
VERSION="$(date '+%Y%m%d.%H%M%S')"
ZIP_NAME="${FUNCTION_NAME}-${VERSION}.zip"
S3_KEY="tool/${ZIP_NAME}"

working_dir=$(mktemp -d)
trap "rm -rf $working_dir" 0

cp -a $CURRENT_PATH/* $working_dir
cd $working_dir

pip install -t . -r requirements.txt

zip -r ${ZIP_NAME} ./* -x ./data/\*xlsx

# S3 にコピー
aws s3 cp "${ZIP_NAME}" "s3://${BUCKET_NAME}/${S3_KEY}"

# Zip を Lambda にデプロイ & 新しいバーションをpublish
LAMBDA_RESULT=$(aws --region ${REGION_NAME} lambda update-function-code --function-name ${FUNCTION_NAME} --s3-bucket ${BUCKET_NAME} --s3-key ${S3_KEY} --publish)

# Lambda のエイリアスの付け替え
NEW_LAMBDA_VERSION=$(echo ${LAMBDA_RESULT} | jq -r .Version)
aws --region ${REGION_NAME} lambda update-alias --function-name ${FUNCTION_NAME} --name ${ALIAS_NAME} --function-version ${NEW_LAMBDA_VERSION}
