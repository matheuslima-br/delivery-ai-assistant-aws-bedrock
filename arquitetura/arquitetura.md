# Arquitetura do Assistente de Delivery

## Visão geral

O projeto utiliza uma arquitetura serverless para realizar a busca de
restaurantes e gerar recomendações utilizando Inteligência Artificial.

```text
                    USUÁRIO
                       |
                       v
              AWS STEP FUNCTIONS
                       |
                       v
                  AWS LAMBDA
                       |
                       v
          OPENSTREETMAP / OVERPASS API
                       |
                       v
             DADOS DE RESTAURANTES
                       |
                       v
                AMAZON BEDROCK
                       |
                       v
              RECOMENDAÇÃO COM IA
                       |
                       v
                    USUÁRIO
