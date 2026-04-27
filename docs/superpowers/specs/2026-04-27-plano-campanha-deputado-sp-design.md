# Plano de Campanha Digital — Deputado Federal SP 2026

**Data:** 2026-04-27  
**Cliente:** Deputado Federal — Podemos / São Paulo  
**Media Buyer:** Alexsandro  
**Status:** Aprovado para implementação

---

## Contexto

Campanha de reeleição para deputado federal pelo estado de São Paulo. O deputado obteve ~90.000 votos em 2022 e tem como meta 120.000 votos em 2026 (+33%). A estratégia é concentrada em Meta Ads para paid media, com presença orgânica em todas as plataformas e Kommo CRM como hub central de relacionamento com eleitores.

---

## Presença Digital Atual

| Plataforma | Seguidores atuais |
|---|---|
| Facebook | 169.000 |
| Instagram | 77.000 |
| YouTube | 4.000 |
| TikTok | 5.000 |

---

## Fases da Campanha

### Fase 1 — Pré-campanha
- **Período:** Agora → 15 de agosto de 2026 (~110 dias)
- **Orçamento:** R$10.000/mês (~R$40.000 total)
- **Investimento diário Meta Ads:** ~R$330/dia

**Objetivos:**
- Crescer base de seguidores (ver metas abaixo)
- Capturar 15.000+ opt-ins de WhatsApp via landing pages
- Importar base Excel existente para Kommo CRM
- Criar e aquecer a Conta Backup 2 para atingir limite de R$2.700/dia até agosto
- Configurar toda a stack tecnológica

**Metas de crescimento:**

| Plataforma | Hoje | Meta (15/08) |
|---|---|---|
| Instagram | 77k | 150k+ |
| Facebook | 169k | 250k+ |
| YouTube | 4k | 15k+ |
| TikTok | 5k | 30k+ |

---

### Fase 2 — Campanha Oficial
- **Período:** 15 de agosto → 5 de outubro de 2026 (51 dias)
- **Orçamento:** R$750.000
- **Investimento diário Meta Ads:** R$14.700/dia (distribuído entre 3 contas)

**Objetivos:**
- Awareness massivo no estado de SP
- Conversão de eleitores indecisos
- Ativação de apoiadores via WhatsApp (Kommo)
- Meta: 120.000 votos

---

### Fase 3 — Contingência 2º Turno
- **Período:** 5 → 26 de outubro de 2026 (se aplicável)
- **Orçamento:** Reserva de R$20.000 (incluída na verba de campanha)

---

## Arquitetura de Contas Meta

### Estrutura

```
BUSINESS MANAGER (verificado + declaração política ativa)
│
├── CONTA PRINCIPAL — R$8.000/dia
│   Campanhas de awareness, alcance e vídeo
│   Pixel principal instalado aqui
│
├── CONTA BACKUP 1 — R$4.000/dia
│   Campanhas de engajamento e tráfego
│   Mirror das campanhas principais
│
└── CONTA BACKUP 2 — R$2.700/dia
    Campanhas de retargeting e conversão (leads WhatsApp)
    INICIAR AGORA para construir histórico de conta
```

### Regras de Operação
- As 3 contas rodam simultaneamente — divisão por objetivo, não failover
- Conta Backup 2 deve ser criada e aquecida imediatamente (agora com R$100-200/dia)
- Business Manager com declaração de anúncio de interesse social/político ativa antes de agosto
- Cartão de crédito diferente em cada conta
- Limites de gasto crescem com histórico de pagamento — aquecer cedo é obrigatório

---

## Stack Tecnológica

### Kommo CRM (hub central)

**Plano:** Master (~R$400/mês para até 5 usuários)

**Pipelines:**
- Leads frios (capturados via anúncio)
- Apoiadores (engajaram, responderam)
- Mobilizadores (vão indicar outros eleitores)
- VIPs (lideranças e formadores de opinião)

**Integrações:**
- WhatsApp Business API (via BSP homologado)
- Facebook Lead Ads (leads entram automaticamente)
- Instagram DMs
- E-mail

**Automações:**
- Novo lead → mensagem WhatsApp em até 5 minutos
- Sem resposta em 48h → follow-up automático
- Tag "mobilizador" → sequência de ativação

---

### Stack Completa

| Ferramenta | Função | Custo estimado/mês |
|---|---|---|
| Kommo CRM | Hub de relacionamento com eleitores | R$400 |
| WhatsApp Business API | Comunicação em escala (via Kommo) | R$0,25/conversa |
| Landing Page (Systeme.io) | Captura de leads com pixel | R$150 |
| Meta Business Suite | Gestão das 3 contas de anúncio | Gratuito |
| Google Looker Studio | Dashboard de resultados para o cliente | Gratuito |
| Make (ex-Integromat) | Automações entre ferramentas | R$100 |
| **Total tecnologia** | | **~R$650-800/mês** |

**Custo tecnológico total no ciclo:** ~R$8.000

---

### Migração da Base Excel → Kommo

1. Limpeza dos dados (remover duplicatas, padronizar telefones)
2. Enriquecimento: validar WhatsApp ativo via verificação em lote
3. Segmentar por região (capital, RMSP, interior)
4. Importar no Kommo com tags por segmento
5. Subir como Custom Audience no Meta para lookalike imediato

> A base existente é o ativo mais valioso — eleitores anteriores têm 60-70% de taxa de retenção de voto quando nutridos corretamente.

---

## Previsão por Eleitor Alcançado

### Premissas

| Premissa | Valor |
|---|---|
| Universo Meta em SP (adultos 18+) | ~18 milhões |
| CPM pré-campanha | R$11 |
| CPM campanha oficial | R$13 |
| Frequência pré-campanha | 3x |
| Frequência campanha | 8x |

### Projeção de Alcance

| Métrica | Pré-campanha | Campanha | Total |
|---|---|---|---|
| Investimento | R$40.000 | R$750.000 | R$790.000 |
| Impressões geradas | 3,6M | 57,7M | 61,3M |
| Frequência média | 3x | 8x | — |
| Eleitores únicos alcançados | 1,2M | 7,2M | ~7,5M* |
| Custo por eleitor alcançado | R$0,033 | R$0,104 | **R$0,10** |

*Desconta overlap estimado de 30% entre fases

### Funil de Conversão

```
7.500.000  eleitores únicos alcançados       → R$0,10 cada
    ↓ 6% engajamento
  450.000  engajados (vídeo, clique, curtida) → R$1,76 cada
    ↓ 10% dos engajados
   45.000  leads capturados (WhatsApp/form)   → R$17,56 cada
    ↓ 40% dos leads
   18.000  apoiadores ativos                  → R$43,89 cada
    ↓ meta geral
  120.000  votos                              → R$6,58 por voto
```

### Resumo Executivo

| Indicador | Valor |
|---|---|
| Total investido | R$790.000 |
| Eleitores únicos impactados | ~7,5 milhões |
| Custo por eleitor alcançado | **R$0,10** |
| Leads de WhatsApp capturados | ~45.000 |
| Meta de votos | 120.000 |
| Custo por voto | **R$6,58** |

---

## Alocação do Orçamento

### Pré-campanha — R$40.000

| Destino | Valor | % |
|---|---|---|
| Meta Ads (awareness + seguidores) | R$24.000 | 60% |
| Meta Ads (captura de leads) | R$8.000 | 20% |
| Produção de conteúdo | R$6.000 | 15% |
| Tecnologia (Kommo + setup) | R$2.000 | 5% |
| **Total** | **R$40.000** | 100% |

### Campanha Oficial — R$750.000

| Destino | Valor | % |
|---|---|---|
| Meta Ads — Conta Principal | R$408.000 | 54% |
| Meta Ads — Backup 1 | R$204.000 | 27% |
| Meta Ads — Backup 2 | R$138.000 | 18% |
| Produção de conteúdo | R$54.000 | 7% |
| Tecnologia (operação CRM + API) | R$18.000 | 2% |
| Contingência / 2º turno | R$20.000 | 3% |
| **Total** | **R$750.000** | 100% |

### Calendário de Desembolso

```
AGORA → JUL     AGOSTO            SETEMBRO    OUTUBRO
R$10k/mês       R$10k (1-15)      R$220k      R$300k
                R$130k (15-31)
                     ↑
                LARGADA CAMPANHA
                R$14.700/dia
```

> Concentração em setembro/outubro: a decisão de voto se forma nos últimos 30 dias. Gastar pesado antes disso antecipa o gasto sem retorno equivalente.

---

## Visão Consolidada

| Fase | Período | Investimento | % do total |
|---|---|---|---|
| Pré-campanha | Agora → 15/ago | R$40.000 | 5% |
| Campanha | 15/ago → 05/out | R$750.000 | 95% |
| **Total** | | **R$790.000** | 100% |

---

## Próximos Passos Imediatos

1. Criar Conta Backup 2 no Meta Business Manager e iniciar aquecimento
2. Instalar Kommo CRM e configurar pipelines e integrações WhatsApp
3. Limpar e importar base Excel para Kommo + gerar Custom Audience no Meta
4. Criar landing page de captura de leads com pixel instalado
5. Ativar declaração de anúncio político no Business Manager
6. Configurar dashboard Looker Studio para o cliente acompanhar resultados

---

## Ferramentas Existentes no Projeto

O projeto `eleitoral_sp` já conta com:
- **Heatmap eleitoral** por município de SP baseado em dados do TSE 2022/2018
- **API de recomendações** de alocação de orçamento por município
- **Integração Meta Ads** para dados de performance em tempo real

Esses dados devem alimentar a distribuição geográfica do budget durante a campanha — municípios com alto potencial eleitoral e alta eficiência recebem mais verba (lógica INVEST_MORE do sistema de scoring existente).
