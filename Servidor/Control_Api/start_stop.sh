#!/bin/bash

#Script Realizado por Alejandro Rodríguez González

# Colores de Texto
NEGRO='\e[30m'
ROJO='\e[31m'
VERDE='\e[32m'
AMARILLO='\e[33m'
AZUL='\e[34m'
MAGENTA='\e[35m'
CYAN='\e[36m'
BLANCO='\e[37m'
RESET='\e[0m'

PORT=5000


PORT_RESULT=$(netstat -lpn | grep :$PORT )

startup(){    
    #Funcion para inicializar la Api

    nohup python3 api.py &
    echo -e "Iniciando la Api"
    if [ -z "$PORT_RESULT" ]; then

        echo -e "Api START[${ROJO}FAILED${RESET}]"  
    else

        echo -e "Api START[${VERDE}GOOD${RESET}]"
    fi
}

stop(){
    #Funcion para parar la Api
    if [ -z "$PORT_RESULT" ]; then

        echo -e "Api ya caida"

    else

        kill $PORT_RESULT

        sleep 2

        if [ -z "$PORT_RESULT" ]; then

            echo -e "Api STOP[${ROJO}FAILED${RESET}]"  
        else

            echo -e "Api STOP[${VERDE}GOOD${RESET}]"
        fi 
        
    fi
    
}

if [ $# -eq 0 ]; then 

    echo -e "---------------------------------------------------------\n"
    echo -e "Script para parar (${VERDE}-p${RESET}) o para iniciar (${VERDE}-i${RESET}) o ambas (${VERDE}-a${RESET}) la api \n"
    echo -e "---------------------------------------------------------\n"

elif [ $1 == "-i" ]; then

    startup

elif [ $1 == "-p" ]; then

    stop
    



elif [ $1 == "-a" ];then

    stop
    sleep 2 
    startup

fi




