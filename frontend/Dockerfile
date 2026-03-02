FROM node:20-alpine AS base

WORKDIR /app

# Install dependencies
FROM base AS deps
COPY package*.json ./
RUN npm ci

# Build
FROM deps AS build
COPY . .
ENV NUXT_PUBLIC_API_BASE=http://localhost:8000/api/v1
RUN npm run build

# Production
FROM base AS production
COPY --from=build /app/.output /app/.output

ENV NODE_ENV=production
ENV HOST=0.0.0.0
ENV PORT=3000

EXPOSE 3000

CMD ["node", ".output/server/index.mjs"]
