# Ikea_ilo_patcher



-"ls /config" in repo server for list of ilo servers 																						#done
-pattern  for RE ...\d\d\d and list all mathes																								#done
-then take server listed there connets to his IP and runs  *show /map1/firmware1															#done
- function to determine if ilo 4 or 5																										#done
-if ilo 4 then firmware 4 and if ilo 5 then firmware 5																						#done
-command "load -source http://dsdsd.bin " to load and install new ilo firmware # differnt firmware if 4 or 5







//////////////////////////////////////////////////
show /map1/firmware1   #output is this

status=0
status_tag=COMMAND COMPLETED
Wed Sep 9 ....


/map1/firmware1
Targets
Properties
	version=2.70
	date=May 07 2019
	name=iLO 4
Verbs
	cd version exit show load

//////////////////////////////////////////////////