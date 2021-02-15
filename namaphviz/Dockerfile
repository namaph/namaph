from node:15.8.0-buster-slim

EXPOSE 3000

ENV WORKDIR /app/
WORKDIR ${WORKDIR}

COPY ./package.json ./yarn.lock  ${WORKDIR}

RUN yarn install && \
    yarn install --dev

COPY . $WORKDIR

CMD yarn start
