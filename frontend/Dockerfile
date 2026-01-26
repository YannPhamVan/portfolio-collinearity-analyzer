FROM node:20-alpine

WORKDIR /app

# Copy package.json and package-lock.json
COPY frontend/package*.json ./

RUN npm install

# Copy the rest of the frontend code
COPY frontend/ .

EXPOSE 3000

CMD ["npm", "start"]
