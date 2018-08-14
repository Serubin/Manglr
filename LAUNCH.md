# Starting Manglr

The current version of Manglr is still "In-Dev" and is non functional. The current docker architecture is functional, however not all of the individual services are complete.

The architecture is split into two sections: Authentication and Shortener.

## Starting
To start the authentication service set
`docker-compose -f docker-auth.yml build`
`docker-compose -f docker-auth.yml up`

To start the authentication service set
`docker-compose -f docker-shortener.yml build`
`docker-compose -f docker-shortener.yml up`


