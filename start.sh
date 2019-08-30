#!/bin/bash
cd /home/web/open_kakao/v2
ps=`pgrep -f main_bob.py`
len=`echo $ps | wc -c`
if [ $len != "1" ];then
   echo kill $ps
   kill $ps
fi
nohup python main_bob.py &
echo `date`
