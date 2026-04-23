FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm install --only=production

FROM node:18-alpine

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

COPY --from=builder /app/node_modules ./node_modules
COPY . .

HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
  CMD wget -qO- http://localhost:3000/health || exit 1

USER appuser

EXPOSE 3000

CMD ["node", "app.js"]