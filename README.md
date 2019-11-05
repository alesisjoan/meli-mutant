######TL/DR

```
python3 server_api.py
```

#Instrucciones de ejecucion

Se requiere una instancia de Redis:

```bash
sudo apt-get install redis-server
redis-server
```

Instalar los requerimientos:

```bash
pip3 install -r requirements.txt
```

Para correr el servidor por defecto en el 8081:

```bash
python3 server_api.py
```
para otro puerto:

```bash
export REDIS=[redis_server]
export REDISPWD=[redis_password]
export PORT=[puerto]
python3 server_api.py
```

##Demo

Desde un entorno de pruebas para requests HTTP 

```
POST /mutant HTTP/1.1
Host: https://possessed-spirit-56339.herokuapp.com
Content-Type: text/plain; charset=utf-8
Cache-Control: no-cache

{"dna":["ATGCGA","CAGTGT","TTATGT","AGAAGT","CCCCTT","TCACTG"]}
```

```
GET /stats HTTP/1.1
Host: https://possessed-spirit-56339.herokuapp.com
Content-Type: text/plain; charset=utf-8
Cache-Control: no-cache
```

##Testing

>python3 test.py

##Diagrama de Secuencia

![Secuencia](/docs/sequence_isMutant.png)
![Secuencia](/docs/sequence_stats.png)

##Diagrama de Arquitectura del Sistema

![Secuencia](/docs/architecture.png)

