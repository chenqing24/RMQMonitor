## RabbitMQ拨测脚本

基于Python2.7，存储基于influxdb

1. 告警
    1.1 拨测告警
    拨测心跳Queue, 如果发现发送失败, 会产生3次短信或者微信告警（可以通过配置切换）
    1.2 消费延迟告警
    拨测端会发送一个当前时间的timestamp给到消费端, 消费端校验latency, 如果延迟超过阀值产生3次告警, 3次后间隔一定时间（可配置）再次发送告警
2. 配置
    配置文件目录 ./config
    2.1 RMQHeartBeat.cfg
    针对MQ信息的配置, 包裹告警阀值, 告警等待时间等
    2.2 notifyConfig.cfg
    通知通道配置信息

