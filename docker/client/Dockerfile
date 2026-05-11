FROM node:22-alpine

WORKDIR /app

ENV NODE_ENV=development

COPY client/package.json client/yarn.lock ./

RUN yarn install --frozen-lockfile --network-timeout 100000


COPY client/ .

EXPOSE 3000

CMD ["yarn", "dev", "--host", "0.0.0.0"]
