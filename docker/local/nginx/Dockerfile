FROM nginx:1.25.3-alpine

# Remove the default configuration file so we can use our own
RUN rm /etc/nginx/conf.d/default.conf

COPY ./nginx.conf /etc/nginx/conf.d/default.conf