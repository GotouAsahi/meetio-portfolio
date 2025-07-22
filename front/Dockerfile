# pull official base image
FROM node:16-alpine

# Install global packages
RUN npm install --global @vue/cli
RUN npm install --global axios
RUN npm install --global vue-router
RUN npm install --global tailwindcss@latest
RUN npm install --global postcss@latest
RUN npm install --global autoprefixer@latest

# Set the working directory
WORKDIR /usr/src/frontend

# Install project dependencies
RUN yarn install

# Install specific npm packages
RUN npm install --save @fortawesome/fontawesome-svg-core \
  @fortawesome/free-solid-svg-icons \
  @fortawesome/vue-fontawesome \
  @fortawesome/free-brands-svg-icons \
  @fortawesome/free-regular-svg-icons \
  vue-session \
  vue-cookies \
  moment \
  vue3-simple-typeahead \
  vue3-google-login \
  file-saver \
  monaco-editor \
  monaco-editor-webpack-plugin \
  terser-webpack-plugin \
  vue-star-rating@next \
  vue-chartjs \
  chart.js \
  moment

# Set environment variables
ENV HOST 0.0.0.0
EXPOSE 8080
