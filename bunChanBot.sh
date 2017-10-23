#!/bin/zsh
export CURRENT_PATH=`echo $(cd $(dirname $0) && pwd)`
export ENV_NAME=Bun-chan-Bot
export VIRTUALENV_PATH=$CURRENT_PATH/$ENV_NAME

source $VIRTUALENV_PATH/bin/activate
python $CURRENT_PATH/bunChanBot.py
