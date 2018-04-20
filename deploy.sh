#!/bin/bash


# ssh hasker@37.139.2.116 -i .travis/key_hasker
# 
eval "$(ssh-agent -s)" # Start ssh-agent cache
chmod 600 .travis/key_hasker # Allow read access to the private key
ssh-add .travis/key_hasker # Add the private key to SSH

git config --global push.default matching
git remote add deploy ssh://git@$IP:$PORT$DEPLOY_DIR
git push deploy master

# Skip this command if you don't need to execute any additional commands after deploying.
ssh hasker@$IP -p $PORT -i .travis/key_hasker <<EOF
  cd $DEPLOY_DIR
  make build
  make run
EOF