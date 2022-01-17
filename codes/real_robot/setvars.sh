# solo vale en los PCs del laboratorio Y con los pendrives de ASUS. Versión 2122
if [ $# -ne 1 ]
  then
    echo "argumentos: numero_turtlebot"
  else
    # hacemos copia del .bashrc, si ya existe la copia copiamos esta en .bashrc
    # para que cada vez que ejecutamos esto no andemos añadiendo más y más líneas
    if [ ! -f ~/.bashrc_zbackup ]
      then
        echo "haciendo copia del .bashrc..."
        cp ~/.bashrc ~/.bashrc_zbackup
    fi
    cp  ~/.bashrc_zbackup ~/.bashrc
    mi_ip=$(ip -o -4 addr list | grep "wlx" | awk '{print $4}' | cut -d/ -f1)
    let offset=$1+4
    ip_turtlebot=192.168.1.$offset
    echo "ROS_MASTER_URI=http://$ip_turtlebot:11311" >> ~/.bashrc
    echo "ROS_HOSTNAME=$mi_ip" >> ~/.bashrc
    echo "source $HOME/ws_rviz_new/devel/setup.bash" >> ~/.bashrc   
    echo "echo tu ip: $mi_ip - ip del robot: $ip_turtlebot" >> ~/.bashrc
fi


