RED='\033[0;31m'
NC='\033[0m'

printf "${RED}>>> pull hashtagcharity container $1:$2${NC}\n"
docker pull hashtagcharity/$1:$2

printf "${RED}>>> stop container $1${NC}\n"
docker stop $1

printf "${RED}>>> remove every container with 'exited' status${NC}\n"
docker ps -f status=exited -q | xargs docker rm || true

printf "${RED}>>> remove untagged images${NC}\n"
docker rmi -f $(docker images | grep "<none>" | awk '{ print $3 }') || true

printf "${RED}>>> fetch envars from consul${NC}\n"
curl --silent http://consul.hashtagcharity.org:8500/v1/kv/lucy/$1/envars | jq ".[0].Value" | python -m base64 -d > $1.env

printf "${RED}>>> start container $1 and publish port 3000 on $3${NC}\n"
docker run -d --name $1 -p $3:3000 --env-file=$1.env hashtagcharity/$1:$2
