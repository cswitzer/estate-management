# Don't need docker.io in the FROM statement, but it adds clarity.
FROM docker.io/node:20.11-alpine3.18 as base

FROM base as node-build-stage

# recommended by official docs: https://github.com/nodejs/docker-node/blob/58c3b39e5948f82c594395857193cd97d01c690e/README.md#nodealpine
RUN apk add --no-cache libc6-compat

# Copy dependencies, accounting for pnpm, yarn, and npm
COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* ./

RUN \
    if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
    elif [ -f package-lock.json ]; then npm ci; \
    elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm i; \
    else echo "Lockfile not found." && exit 1; \
    fi

# RUN STAGE
FROM base as node-run-stage

ARG APP_HOME=/app
WORKDIR ${APP_HOME}

COPY --from=node-build-stage /node_modules ./node_modules

COPY . ${APP_HOME}

# add group with id 1001 and the name nodejs
# add system user with id 1001 and the name nextjs. add them to nodejs group
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001 -G nodejs

# change ownership of the app directory to nextjs user and nodejs group
# change permissions of the app directory to 777
RUN chown -R nextjs:nodejs ${APP_HOME}
RUN chmod -R 777 ${APP_HOME}

USER nextjs

CMD [ "npm", "run", "dev" ]
