#!/usr/bin/env bash
# 重启服务器
cp /var/www/flask_zhihu/flask_zhihu.nginx /etc/nginx/sites-enabled/flask_zhihu
cp /var/www/flask_zhihu/flask_zhihu.conf /etc/supervisor/conf.d/flask_zhihu.conf
cp /var/www/flask_zhihu/celery_zhihu.conf /etc/supervisor/conf.d/celery_zhihu.conf


service supervisor restart
service nginx restart


echo 'succsss'
echo 'ip'
hostname -I
