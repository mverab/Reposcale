#!/bin/bash
# Deployment script — manual rsync, secrets hardcoded

SERVER="prod@10.0.1.50"

echo "Building frontend..."
cd frontend && npm run build && cd ..

echo "Deploying backend..."
rsync -avz backend/ $SERVER:/opt/platform/backend/

echo "Deploying frontend..."
rsync -avz frontend/dist/ $SERVER:/var/www/platform/

echo "Restarting backend..."
ssh $SERVER "pkill -f server.py; cd /opt/platform/backend && nohup python server.py &"

echo "Done!"
