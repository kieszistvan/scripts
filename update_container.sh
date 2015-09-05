RED='\033[0;31m'
NC='\033[0m'

printf "${RED}>>> pull container $1:$2${NC}\n"
docker pull $1:$2

printf "${RED}>>> stop container $1${NC}\n"
docker stop $1

printf "${RED}>>> remove every container with 'exited' status${NC}\n"
docker ps -f status=exited -q | xargs docker rm || true

printf "${RED}>>> remove untagged images${NC}\n"
docker rmi -f $(docker images | grep "<none>" | awk '{ print $3 }') || true

printf "${RED}>>> fetch envars from consul${NC}\n"
MACHINE_ENV=$(curl --silent http://consul.org:8500/v1/kv/machines/$HOSTNAME/env | jq ".[0].Value" | python -m base64 -d)
curl --silent http://consul.org:8500/v1/kv/$MACHINE_ENV/$1/envars | jq ".[0].Value" | python -m base64 -d > $1.env

printf "${RED}>>> start container $1 and publish port 3000 on $3${NC}\n"
docker run -d --name $1 -p $3:3000 --env-file=$1.env $1:$2
