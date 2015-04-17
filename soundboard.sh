#!/bin/sh
#
# /etc/init.d/soundboard
# Subsystem file for "soundboard" server
#
# chkconfig: 2345 95 05	(1)
# description: soundboard server daemon
#
# processname: python
# config: /root/robotSoundBoard/run.cfg
# pidfile: /var/run/soundboard.pid


RETVAL=0
prog="RobotSoundBoard"

start() {
	echo -n $"Starting $prog:"
	cd /root/robotSoundBoard
	/usr/bin/python game.py &
        PID=$!
	RETVAL=$?
	echo $PID >  /var/run/soundboard.pid
	echo
}

stop() {
	echo -n $"Stopping $prog:"
	if [ -f /var/run/soundboard.pid ] ; then
	kill -9 `cat /var/run/soundboard.pid`
	rm /var/run/soundboard.pid
        fi
	echo
}

case "$1" in
	start)
		start
		;;
	stop)
		stop
		;;
	restart)
		stop
		start
		;;
	*)
		echo $"Usage: $0 {start|stop|restart}"
		RETVAL=1
esac
exit $RETVAL
