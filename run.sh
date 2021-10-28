#!/usr/bin/env bash
set -e 

# make sure python3 exists
if [[ $(type -P python3) ]]; then
    echo "Python test okay"
else
    echo "Python test failed"
    echo "Python 3 is required, please install python interpreter to continue"
    exit 1
fi

# make sure pip is installed
if [[ $(python3 -m pip --version) ]]; then
    echo "Python pip test okay"
else
    echo "Python pip test failed"
    echo "pip is required to install python3 dependencies, please install to continue"
    exit 1
fi

# create venv to isolate programs python deps from rest of system
if [[ ! -d $(pwd)/venv ]]; then
    echo "Could not find the python virtual environment, creating one now"
    python3 -m venv venv
else
    echo "Found virtual environment, moving on to next step"
fi

echo "Activating python virtual environment"
source venv/bin/activate

FILE=$(pwd)/requirements.txt
if [[ -f $FILE ]]; then
    echo "Checking to see what dependencies need to be installed, if any"
    python3 -c "import pkg_resources; pkg_resources.require(open('requirements.txt',mode='r'))" &>/dev/null || python3 -m pip install --ignore-installed -r requirements.txt
else
    echo "requirements.txt is needed to ensure correct python dependencies are installed"
    echo "please make sure you are in the right directory and run this again"
    exit 1
fi

echo ""
echo ""
if [[ $# -lt 1 ]]; then
    python3 src/multihop_mtu_wrapper.py --help 2> /dev/null
else 
    python3 src/multihop_mtu_wrapper.py "$@" 2> /dev/null
fi

deactivate