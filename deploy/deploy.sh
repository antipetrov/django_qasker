#!/bin/bash


# ssh hasker@37.139.2.116 -i .travis/key_hasker
# 
eval "$(ssh-agent -s)" # Start ssh-agent cache

openssl aes-256-cbc -K $encrypted_65a296283a37_key -iv $encrypted_65a296283a37_iv -in deploy/key_hasker.enc -out deploy/key_hasker -d

chmod 600 deploy/key_hasker # Allow read access to the private key
ssh-add deploy/key_hasker # Add the private key to SSH

# git config --global push.default matching
# git remote add deploy ssh://git@$IP:$PORT$DEPLOY_DIR
# git pull deploy master

# ls

ssh hasker@$IP -p $PORT -i deploy/key_hasker <<EOF
  cd $DEPLOY_DIR
  git pull
  make prod
EOF