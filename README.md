# webscraping_python

Este é um projeto criado de acordo com meu avanço no aprendizado de Python e WebScraping
O script busca no site da CBF a tabela do campeonato brasileiro séria a, transforma em dataframe, trata alguns detalhes e informações como, exclusão de colunas e caracteres indesejados.

Caso a página alvo tenha mais de uma tabela, é possível identifica-las através do bloco "for", tornando mais fácil escolher qual tabela deseja trabalhar.

Por fim o script salva o dataframe em .xlsx, .csv e json
