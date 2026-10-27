# Imagen de DESARROLLO del frontend: simple a propósito (sin multi-stage ni optimizaciones).
FROM node:22-alpine

# pnpm con la versión fijada en el TRD §1
RUN npm install -g pnpm@12.15.0

WORKDIR /app

# 1) Dependencias exactas del pnpm-lock.yaml
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

# 2) Código (se copia explícito para no arrastrar un node_modules local al contenedor)
COPY index.html vite.config.js ./
COPY public ./public
COPY src ./src

EXPOSE 5173
CMD ["pnpm", "dev"]
