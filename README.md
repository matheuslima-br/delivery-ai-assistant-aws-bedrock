# Assistente de Delivery com IA

Projeto de um assistente inteligente capaz de encontrar restaurantes
próximos ao usuário e gerar recomendações personalizadas utilizando
Inteligência Artificial.

O projeto foi desenvolvido utilizando serviços serverless da AWS,
Amazon Bedrock, Python e dados do OpenStreetMap.

---

## Objetivo

Criar um assistente conversacional capaz de responder a solicitações como:

> "Acabei de chegar em uma cidade nova. Quero sugestões de restaurantes próximos."

O sistema considera informações como:

- localização do usuário;
- distância;
- tipo de culinária;
- orçamento;
- preferência por delivery;
- histórico da conversa.

---

## Qual problema resolve?

Ele facilita a descoberta de restaurantes para uma pessoa que está em uma cidade nova. Em vez de simplesmente retornar uma lista de estabelecimentos, o sistema considera o contexto e as preferências do usuário e utiliza IA para apresentar as opções mais relevantes.

---

## Arquitetura

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
              OPENSTREETMAP / OVERPASS
                           |
                           v
                  DADOS DOS RESTAURANTES
                           |
                           v
                    AMAZON BEDROCK
                           |
                           v
                 RECOMENDAÇÃO COM IA
                           |
                           v
                        USUÁRIO# delivery-ai-assistant-aws-bedrock
