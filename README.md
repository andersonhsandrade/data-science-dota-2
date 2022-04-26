# Data Science Dota 2

Esse projeto é um espelho de estudo do projeto do [Téo Calvo](https://github.com/TeoCalvo) (Link do repositório: [DotaScience](https://github.com/TeoCalvo/DotaScience)) onde busquei praticar alguns fundamentos para desenvolver meu conhecimento.

Durante o projeto fizemos a coleta de dados diretamente da API da [OpenDota](https://www.opendota.com/) para extrair dados de partidas profissionais, subimos dois bancos de dados MongoDB (os dados extraídos diretamente da api são não relacionais e usamos o mongo para guardar a informação bruta) e MariaDB (selecionamos alguns dados que vamos trabalhar e inputamos num banco relacional para facilitar o trabalho do análise e ML futuramente), com docker (docker-compose).


