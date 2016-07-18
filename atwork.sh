#!/bin/bash

case $1 in
    on)
        echo "127.0.0.1 www.facebook.com" >> /etc/hosts
        echo "127.0.0.1 index.hu" >> /etc/hosts
        echo "127.0.0.1 www.origo.hu" >> /etc/hosts
        echo "127.0.0.1 444.hu" >> /etc/hosts
        ;;
    off)
        sed -i -e /"127.0.0.1 444.hu"/d /etc/hosts
        sed -i -e /"127.0.0.1 www.origo.hu"/d /etc/hosts
        sed -i -e /"127.0.0.1 index.hu"/d /etc/hosts
        sed -i -e /"127.0.0.1 www.facebook.com"/d /etc/hosts
        ;;
    *)    
        echo "doggy afuera"
esac
