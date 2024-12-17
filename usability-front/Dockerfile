## Stage 1: Build
FROM node:18-slim AS build
WORKDIR /usr/app

COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

## Stage 2: Serve
FROM nginx:alpine
EXPOSE 5173
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /usr/app/dist /usr/share/nginx/html
