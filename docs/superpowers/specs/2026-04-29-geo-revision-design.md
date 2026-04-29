# Design: Revisão Geográfica — Cobertura Estadual SP

**Data:** 2026-04-29
**Arquivo alvo:** `david-soares-dashboard.html`
**Escopo:** Seção geográfica do dashboard — dados, layout e renderização

---

## Contexto

O dashboard atual foca excessivamente na capital paulista (99,7% do alcance). David Soares concorre a Deputado Estadual, cargo que representa todos os 645 municípios do Estado de São Paulo (~34M eleitores). A seção geográfica precisa refletir o universo eleitoral completo do estado.

---

## Mudanças de Dados

### Novo: `MACRORREGIOES` (substitui a tabela de regiões ativas atual)

Array com as 15 regiões intermediárias do IBGE para SP:

```js
const MACRORREGIOES = [
  { id: "metro_sp",   nome: "Grande São Paulo",        eleit: 15800000, municipios: 39,  cobertura: 99.7, spend: 8706, prioridade: "ativo"  },
  { id: "campinas",   nome: "Campinas",                eleit: 3200000,  municipios: 74,  cobertura: 0.1,  spend: 0,    prioridade: "alto"   },
  { id: "sorocaba",   nome: "Sorocaba",                eleit: 2100000,  municipios: 79,  cobertura: 0,    spend: 0,    prioridade: "alto"   },
  { id: "sjc",        nome: "S. José dos Campos",      eleit: 1900000,  municipios: 39,  cobertura: 0,    spend: 0,    prioridade: "alto"   },
  { id: "ribeirao",   nome: "Ribeirão Preto",          eleit: 1800000,  municipios: 96,  cobertura: 0,    spend: 0,    prioridade: "medio"  },
  { id: "santos",     nome: "Santos / Baixada",        eleit: 1600000,  municipios: 9,   cobertura: 0,    spend: 0,    prioridade: "medio"  },
  { id: "bauru",      nome: "Bauru",                   eleit: 1100000,  municipios: 71,  cobertura: 0,    spend: 0,    prioridade: "medio"  },
  { id: "sao_rpreto", nome: "S. José do Rio Preto",   eleit: 1300000,  municipios: 96,  cobertura: 0,    spend: 0,    prioridade: "medio"  },
  { id: "presidente", nome: "Presidente Prudente",     eleit: 950000,   municipios: 102, cobertura: 0,    spend: 0,    prioridade: "baixo"  },
  { id: "marilia",    nome: "Marília",                 eleit: 700000,   municipios: 51,  cobertura: 0,    spend: 0,    prioridade: "baixo"  },
  { id: "aracatuba",  nome: "Araçatuba",               eleit: 650000,   municipios: 42,  cobertura: 0,    spend: 0,    prioridade: "baixo"  },
  { id: "franca",     nome: "Franca",                  eleit: 600000,   municipios: 22,  cobertura: 0,    spend: 0,    prioridade: "baixo"  },
  { id: "vale_para",  nome: "Vale do Paraíba",         eleit: 1400000,  municipios: 39,  cobertura: 0.3,  spend: 26,   prioridade: "medio"  },
  { id: "piracicaba", nome: "Piracicaba",              eleit: 850000,   municipios: 26,  cobertura: 0,    spend: 0,    prioridade: "medio"  },
  { id: "registro",   nome: "Registro / Vale Ribeira", eleit: 280000,   municipios: 25,  cobertura: 0,    spend: 0,    prioridade: "baixo"  },
];
```

Campos: `id`, `nome`, `eleit` (eleitorado estimado TSE), `municipios`, `cobertura` (% alcance atual Meta API), `spend` (R$ gasto atual), `prioridade`.

### Expandido: `UNTAPPED` (10 → 25 cidades)

Adicionar campo `regiao` a cada entrada. Novas cidades a incluir:
Sorocaba, Jundiaí, Bauru, São José do Rio Preto, Franca, Araçatuba, Presidente Prudente, Marília, Taubaté, Praia Grande, Caçapava, Limeira, Americana, São Carlos, Araraquara, Botucatu.

---

## Layout HTML

### Cabeçalho da seção

**De:**
```
MAPA ESTRATÉGICO SP — REGIÕES COM CAMPANHA + OPORTUNIDADES
```
**Para:**
```
COBERTURA ELEITORAL — ESTADO DE SÃO PAULO (645 MUNICÍPIOS · ~34M ELEITORES)
```

### Painel 1 — COBERTURA POR MACRORREGIÃO

Tabela com colunas:
`MACRORREGIÃO | MUNICÍPIOS | ELEITORADO | COBERTURA ATUAL | GASTO | PRIORIDADE`

- Coluna `COBERTURA ATUAL`: barra SVG inline (80px) + percentual numérico
  - Verde (`var(--g)`) se cobertura ≥ 50%
  - Amarelo (`#C9A227`) se cobertura 5–49%
  - Vermelho/roxo (`var(--p2)`) se cobertura < 5%
- Linha "Grande São Paulo" estilizada com destaque (background levemente diferenciado)
- `id="macro-tbody"` no `<tbody>`

### Painel 2 — TOP 25 CIDADES SEM CAMPANHA

Tabela com colunas:
`CIDADE | REGIÃO | POPULAÇÃO | ELEITORADO | PRIORIDADE`

- Badge colorido na coluna PRIORIDADE (alto = vermelho/roxo, medio = amarelo, baixo = cinza)
- Ordenação: prioridade desc, eleitorado desc
- `id="untapped-tbody"` (mantém id existente)

### Nota estratégica (substitui "SP capital concentra 99,7%")

```
"Grande SP concentra 99,7% do alcance atual. As demais 14 macrorregiões
somam ~18,2M eleitores — 53% do eleitorado estadual — sem presença de campanha."
```

---

## Lógica JS

### Função `coverageBar(pct)`

```js
function coverageBar(pct) {
  const color = pct >= 50 ? 'var(--g)' : pct >= 5 ? '#C9A227' : 'var(--p2)';
  return `<svg width="80" height="10" style="vertical-align:middle;margin-right:4px">
    <rect width="80" height="10" rx="3" fill="rgba(255,255,255,.08)"/>
    <rect width="${Math.min(pct, 100) * 0.8}" height="10" rx="3" fill="${color}"/>
  </svg>${pct.toFixed(1)}%`;
}
```

### Função `renderMacrorregioes()`

Substitui a lógica que popula `#city-tbody`. Itera `MACRORREGIOES`, gera `<tr>` para cada região.

### Função `renderUntapped()`

Substitui a lógica que popula `#untapped-tbody`. Itera `UNTAPPED` expandido (25 cidades), inclui coluna `regiao`.

### Nenhuma alteração em:
- `PERIODS`, `SERIES`, `CAMPAIGNS`, `DEMOS`, `PLATFORMS`
- Seções de KPIs, evolução temporal, criativos, demografia

---

## Escopo

- **Arquivo único:** `david-soares-dashboard.html`
- **Linhas estimadas:** ~150 linhas alteradas/adicionadas (de 1513 total)
- **Sem novas dependências**
- **Compatível com o seletor de período existente** — `cobertura` e `spend` em `MACRORREGIOES` podem ser indexados por período se necessário (v2)
