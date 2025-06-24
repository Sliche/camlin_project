# Application Startup
Once you clone the application, do
```
cp .env.sample .env
docker-compose up -d
```
The docker image used is the one on my docker repository and it is public.
The application should work out of the box. It is configured by default to work on port 8000.
So visit http://localhost:8000/docs.

On first run it will do the database migration and create necessary records. As for this application
it is only the default user with credentials:
```
username: camlin12
password: camlin12
```
It will also fetch all currencies supported by NBP api and only those currencies will be permitted
for API operations.

Once the 

### NOTES
1. Storing db and other credentials and keys like this in env.sample publicly on git is not how its done on prod envs but for this use case it works because I wanted everything to work with minimal setup
2. I am using Fastapi's OAuth2PasswordBearer for logging in, fields client_id and client_secret can be ignored while logging in.
3. User managing routes are written to be managed by end-user. Not from admin perspective. This means
that each protected route concerning users will perform operations on the currently logged in user.
4. 
