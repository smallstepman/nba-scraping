# # # base image
# # FROM node:12

# # # set working directory
# # WORKDIR /app

# # # add `/app/node_modules/.bin` to $PATH
# # ENV PATH /app/node_modules/.bin:$PATH

# # # install and cache app dependencies
# # COPY package.json /app/package.json
# # RUN npm install 
# # COPY . .
# # # start app
# # CMD ["npm", "start"]

# # Stage 1
# FROM node:12 as react-build
# ENV NODE_OPTIONS=--max_old_space_size=4096
# WORKDIR /app
# COPY . ./
# RUN npm install
# RUN npm audit fix
# RUN npm run build

# # Stage 2 - the production environment
# FROM nginx:alpine
# COPY nginx.conf /etc/nginx/conf.d/default.conf
# COPY --from=react-build /app/build /usr/share/nginx/html
# EXPOSE 80
# CMD ["nginx", "-g", "daemon off;"]

# Stage 0, "build-stage", based on Node.js, to build and compile the frontend
FROM tiangolo/node-frontend:10 as build-stage
WORKDIR /app
COPY package*.json /app/
RUN npm install
COPY ./ /app/
RUN npm run build
# Stage 1, based on Nginx, to have only the compiled app, ready for production with Nginx
FROM nginx:1.15
COPY --from=build-stage /app/build/ /usr/share/nginx/html
# Copy the default nginx.conf provided by tiangolo/node-frontend
COPY --from=build-stage /nginx.conf /etc/nginx/conf.d/default.conf
CMD ["nginx", "-g", "daemon off;"]
