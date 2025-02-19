# Card ML Deployment

## Overview

Este projeto demonstra como treinar e implantar um modelo de machine learning para classificação usando o conjunto de dados de Cards do Gods Unchained. O modelo é treinado com Scikit-learn, e a classificação é servida por meio de uma API criada com FastAPI. Além disso, o projeto inclui um Dockerfile para facilitar a implantação do modelo em contêineres Docker. Também demonstra como testar o desempenho da API com o Locust.

## Tabela de Conteúdo

- [Objetivo](#objetivo)
- [Fluxo de Versionamento](#fluxo-de-versionamento)
- [Ferramentas](#ferramentas)
- [Getting Started](#getting-started)
- [Requisitos](#requisitos)
- [Usage](#usage)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Troubleshooting](#troubleshooting)
- [Contributions](#contribuições)
- [License](#license)
- [Contato](#contato)
- [Acknowledgments](#acknowledgments)

## Objetivo

O objetivo deste projeto é criar uma pipeline de treinamento e implantação de um modelo de machine learning usando Scikit-learn, FastAPI e Docker. O modelo é treinado com base no conjunto de dados de Cards do Gods Unchained e é capaz de fazer classificação de cards `early` e `late` game com base nas características fornecidas e é implantado em um cluster kubernetes servindo uma api http que recebe o `id` de um card e retorna a classificação deste card.

## Fluxo de Versionamento

Este projeto segue um fluxo de versionamento baseado no Git. Cada grande alteração no projeto deve ser acompanhada por um novo commit com uma mensagem descritiva. Versões do modelo treinado e da API devem ser controladas com base em tags no Git.

## Ferramentas

- Scikit-learn: Biblioteca para machine learning em Python.
- FastAPI: Framework para criar APIs web rápidas com Python.
- Docker: Plataforma para criar, implantar e executar aplicativos em contêineres.
- Locust: Ferramenta para teste de carga.

## Getting Started

Siga estas instruções para configurar o ambiente de desenvolvimento e executar o projeto:

1. Clone o repositório:
```
git clone https://github.com/GersonRS/neofin-machine-learning-engineer-challenge.git
cd neofin-machine-learning-engineer-challenge
```


2. Instale as dependências:
```
poetry install
```


3. Treine o modelo:

Execute o pipeline no [notebook](notebooks/Test Case - ML Engineer.ipynb) de treinamento do modelo.


4. Inicie a API:
```
fastapi run
```

5. Acesse a documentação da API em seu navegador em http://localhost:8000/docs para fazer previsões.

## Requisitos

- Python 3.8+
- Scikit-learn
- FastAPI
- Docker (para implantação)
- Locust (opcional, para teste de carga)

## Usage

Após seguir as instruções em **[Getting Started](#getting-started)**, você pode acessar a documentação da API em http://localhost:8000/docs para fazer previsões sobre a espécie das flores de íris com base nas características fornecidas.

## Dockernization

Este projeto pode ser facilmente "dockernizado" para facilitar a implantação em contêineres Docker. A utilização de contêineres Docker ajuda a garantir a portabilidade e a independência das dependências do sistema, tornando a implantação mais fácil e consistente em diferentes ambientes.

Siga estas etapas para criar uma imagem Docker e executar a aplicação em um contêiner:

### 1. Construir uma imagem docker da aplicação

```
docker build -t card-ml:latest .
```

### 2. Executar o container

```
docker run -d -p 8000:8000 --name card-api card-ml:latest
```
O comando acima executa um contêiner Docker a partir da imagem que você construiu. Ele mapeia a porta 8000 do contêiner para a porta 8000 do host local.

### 3. Va para o localhost
```
http://localhost:8000/docs
```
Agora, a aplicação estará em execução dentro do contêiner Docker. Você pode acessá-la em [http://localhost:8000/docs](http://localhost:8000/docs) para fazer previsões por meio da API.


### 4. Experimente o método post/predict
```
curl -X POST "http://localhost:8000/v1/card/predict" -H\
 "accept: application/json"\
 -H "Content-Type: application/json"\
 -d "{\"id\": 205}"
```

> Lembre-se de que você pode personalizar as portas e os nomes dos contêineres conforme necessário. Certifique-se de ter o Docker instalado e em execução em seu sistema antes de prosseguir.

Ao implantar em um ambiente de produção, você pode usar orquestradores de contêineres, como Kubernetes ou Docker Compose, para gerenciar a implantação e escalabilidade de contêineres. Certifique-se de configurar e ajustar seu ambiente de acordo com suas necessidades específicas.

## Testes

Este projeto inclui a capacidade de realizar testes automatizados usando a biblioteca Locust. Os testes de carga fornecidos podem ser usados para avaliar o desempenho da API e medir a capacidade de resposta em diferentes cenários de carga.

Siga estas etapas para executar os testes de carga:

1. Execute os Testes de Carga:

Navegue até o diretório de testes:


```
cd tests
```

2. Execute o Locust com o arquivo de teste específico:


```
locust -f load_test.py
```
Isso iniciará o servidor de teste do Locust em [http://localhost:8089/](http://localhost:8089/). Você pode acessar o painel de controle do Locust em seu navegador.

3. Configure os Parâmetros de Teste:

* Acesse o painel de controle do Locust em [http://localhost:8089/](http://localhost:8089/).
* Defina o número de usuários virtuais (virtual users) que você deseja simular e a taxa de spawn (quantos usuários por segundo serão iniciados).
* Clique no botão `Start` para iniciar os testes.

4. Execute os Testes de Carga:

Os usuários virtuais gerados pelo Locust irão acessar a API automaticamente de acordo com a configuração que você definiu. Eles enviarão solicitações de previsão à API e coletarão métricas de desempenho.

5. Analise os Resultados:

* Você pode monitorar o progresso dos testes e visualizar métricas de desempenho em tempo real no painel de controle do Locust.
* Ao encerrar os testes, você poderá acessar relatórios detalhados e gráficos para avaliar o desempenho da API.

Lembre-se de que os testes de carga com o Locust são uma maneira eficaz de avaliar o desempenho da sua aplicação e identificar possíveis gargalos. Certifique-se de ajustar os parâmetros dos testes de acordo com as necessidades e requisitos da sua aplicação.

## Estrutura do Projeto

O projeto tem a seguinte estrutura de diretórios:

```
.
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── main.py
├── models
│   ├── ml
│   │   ├── challenge_test.csv
│   │   ├── challenge_train.csv
│   │   ├── Classificador de Cards do Gods Unchained com Machine Learning.ipynb
│   │   ├── classifier.py
│   │   ├── modelo_onehotenc.pkl
│   │   ├── modelo_RF.pkl
│   │   └── modelo_rna.pkl
│   └── schemas
│       └── card.py
├── pasta.txt
├── poetry.lock
├── pyproject.toml
├── README.md
├── routes
│   ├── home.py
│   └── v1
│       └── card_predict.py
└── tests
    ├── __init__.py
    ├── load_test.py
    └── test_response.py

6 directories, 23 files

```


## Troubleshooting

Se você encontrar problemas ou tiver dúvidas sobre o projeto, consulte a seção **[Contribuições](#contribuições)** para obter informações sobre como relatar problemas ou fazer perguntas.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para criar uma solicitação pull com melhorias, correções de bugs ou novos recursos. As contribuições são o que tornam a comunidade de código aberto um lugar incrível para aprender, inspirar e criar. Qualquer contribuição que você fizer será muito apreciada.

Para contribuir com o projeto, siga os passos abaixo:

1. Bifurque o projeto.
2. Crie um branch para sua contribuição (git checkout -b feature-mycontribution).
3. Faça as alterações desejadas no código.
4. Confirme suas alterações (git commit -m 'MyContribution: Adicionando novo recurso').
5. Envie o branch para seu repositório Fork (git push origin feature-mycontribution).
6. Abra uma solicitação pull no branch principal do projeto original. Descreva as alterações e aguarde a revisão e discussão da comunidade.

Valorizamos verdadeiramente o seu interesse em contribuir para o projeto. Juntos, podemos torná-lo ainda melhor!

## License

Este projeto está licenciado sob a [MIT License](LICENSE).

## Contato

Para entrar em contato, envie um e-mail para [gersonrodriguessantos8@gmail.com](mailto:gersonrodriguessantos8@gmail.com).

<p align="center">

 <a href="https://twitter.com/gersonrs3" target="_blank" >
     <img alt="Twitter" src="https://img.shields.io/badge/-Twitter-9cf?logo=Twitter&logoColor=white"></a>

  <a href="https://instagram.com/gersonrsantos" target="_blank" >
    <img alt="Instagram" src="https://img.shields.io/badge/-Instagram-ff2b8e?logo=Instagram&logoColor=white"></a>

  <a href="https://www.linkedin.com/in/gersonrsantos/" target="_blank" >
    <img alt="Linkedin" src="https://img.shields.io/badge/-Linkedin-blue?logo=Linkedin&logoColor=white"></a>

  <a href="https://t.me/gersonrsantos" target="_blank" >
    <img alt="Telegram" src="https://img.shields.io/badge/-Telegram-blue?logo=Telegram&logoColor=white"></a>

  <a href="mailto:gersonrodriguessantos8@gmail.com" target="_blank" >
    <img alt="Email" src="https://img.shields.io/badge/-Email-c14438?logo=Gmail&logoColor=white"></a>

</p>

## Acknowledgments

Agradecimentos a todos os desenvolvedores e mantenedores das bibliotecas e ferramentas utilizadas neste projeto, bem como a toda a comunidade de código aberto que torna projetos como este possíveis.
