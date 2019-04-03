EXPECTED_ARGS=1
key_name="starry-battery-103809-d129914e1f44.json"
key_dir=`pwd`
spacy_dir=`pwd`

if [ ! -f $key_name ]
    then
    if [ $# -ne $EXPECTED_ARGS ]
    then
        echo "Usage: ./setup-dvc-GC.sh path_to_key or ./setup-dvc-GC.sh if key is in utils' root directory"
           exit 1
    else
        if [ ! -f $1 ]
        then
            echo "Key file doesn't exist!"
            exit 1
        else
            key_name=`basename $1`
            cd `dirname $1`
            key_dir=`pwd`
            cd $spacy_dir
        fi
    fi
fi
key_dir="$key_dir/$key_name"

echo "export GOOGLE_APPLICATION_CREDENTIALS=\"$key_dir\"" >> ~/.bashrc
source ~/.bashrc

echo "Type in 'source ~/.bashrc' or open a new terminal window for changes to take effect"

# should be done only once - saves in .dvc/config file
# dvc remote add gc gs://spacy-pl
# dvc config core.remote gc
