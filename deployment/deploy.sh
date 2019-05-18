#!/bin/bash

echo "Make sure to run this from utils root folder and in the virtual environment"
echo ""

# --- SETTINGS ---

PACKAGE_DIR="release"  # same as passed to combine or spacy.cli.package
MODEL_NAME="pl_model-0.2.0"  # same as inputted in spacy.cli.package

BUCKET_NAME="gs://spacy-pl-public-models"
BUCKET_PUBLIC_URL="https://storage.googleapis.com/spacy-pl-public-models"

# --- SCRIPT ---

echo "Using model package location: $PACKAGE_DIR/$MODEL_NAME/"
echo "Using Google Cloud key: $GOOGLE_APPLICATION_CREDENTIALS"
echo ""

pushd $PACKAGE_DIR/$MODEL_NAME/ >/dev/null
rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi

python setup.py --quiet sdist
rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi

gsutil cp dist/$MODEL_NAME.tar.gz $BUCKET_NAME
rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi

popd  >/dev/null

echo ""

# --- DEPLOYMENT INFO ---

echo "Model deployed to $BUCKET_NAME/$MODEL_NAME.tar.gz"
echo ""

INSTALLED_MODEL_NAME=$(echo $MODEL_NAME | sed -e 's/[^a-zA-Z_]//g')
echo "To install the model:"
echo "wget $BUCKET_PUBLIC_URL/$MODEL_NAME.tar.gz"
echo "pip install $MODEL_NAME.tar.gz"
echo "spacy.load('$INSTALLED_MODEL_NAME')"
