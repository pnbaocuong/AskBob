FROM node:20-bullseye-slim AS build
WORKDIR /app
ENV npm_config_loglevel=warn \
    npm_config_fund=false \
    npm_config_audit=false \
    npm_config_update_notifier=false \
    NPM_CONFIG_FETCH_TIMEOUT=120000 \
    NPM_CONFIG_FETCH_RETRIES=5
COPY frontend/package.json frontend/package-lock.json* /app/
RUN npm install --legacy-peer-deps || npm install
COPY frontend /app
RUN npm run build

FROM nginx:alpine AS runtime
COPY --from=build /app/dist /usr/share/nginx/html
COPY frontend/nginx.conf /etc/nginx/nginx.conf
EXPOSE 12173
CMD ["nginx", "-g", "daemon off;"]
