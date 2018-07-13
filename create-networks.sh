networks="user-net shortener-net redirect-net authentication-net static-net auth-data-net short-data-net oauth-net"

for net in $networks; do
    docker network create $net
done
