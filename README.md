TL/DR

python3 server_api.py

Instrucciones de ejecucion

Se requiere una instancia de Redis:

sudo apt-get install redis-server
redis-server

Instalar los requerimientos:

pip3 install -r requirements.txt

Para correr el servidor por defecto en el 8081:

python3 server_api.py

para otro puerto:

export PORT=[puerto]
python3 server_api.py

Demo

POST https://possessed-spirit-56339.herokuapp.com/isMutant
https://possessed-spirit-56339.herokuapp.com/stats

Diagrama de Secuencia

![Secuencia](/docs/sequence_isMutant.png)
![Secuencia](/docs/sequence_stats.png)

Diagrama de Arquitectura del Sistema
