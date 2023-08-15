 #!/bin/bash


 
 lttng-sessiond --daemonize
 lttng create my-user-space-session
 lttng enable-event --userspace empty_tp:empty_tp_4b
 lttng start


 ./tracebenc world and beyond

 echo "IMPORTANT: do not forget to run lttng destory after you hit enter :)"