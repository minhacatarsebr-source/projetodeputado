# Revisão Geográfica — Cobertura Estadual SP

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expandir a seção geográfica do dashboard para refletir o universo eleitoral completo do Estado de SP (15 macrorregiões IBGE, 645 municípios, ~34M eleitores).

**Architecture:** Arquivo único `david-soares-dashboard.html` (1513 linhas). Todas as mudanças são nos blocos de dados JS (linhas 977–1038) e nas funções de renderização (linhas 1335–1365), mais pequenas alterações no HTML (linhas 521–535). Nenhuma dependência externa nova.

**Tech Stack:** HTML/CSS/JS vanilla, SVG inline, Meta Marketing API v19.0 (dados já carregados no arquivo)

---

## Mapa de Arquivos

| Arquivo | Ação | Linhas Afetadas |
|---|---|---|
| `david-soares-dashboard.html` | Modificar | 521–535 (HTML), 977–1038 (dados JS), 1335–1365 (funções JS), 1440 (chamada) |

---

## Task 1: Adicionar array `MACRORREGIOES`

**Files:**
- Modify: `david-soares-dashboard.html:976` (inserir após a linha 976, antes de `const UNTAPPED`)

- [ ] **Step 1: Inserir o array `MACRORREGIOES` antes de `const UNTAPPED` (linha 977)**

Localizar a linha `const UNTAPPED = [` (linha 977) e inserir o seguinte bloco imediatamente antes dela:

```js
const MACRORREGIOES = [
  { id: "metro_sp",   nome: "Grande São Paulo",        eleit: 15800000, municipios: 39,  cobertura: 99.7, spend: 8706, prioridade: "ativo"  },
  { id: "campinas",   nome: "Campinas",                eleit: 3200000,  municipios: 74,  cobertura: 0.1,  spend: 0,    prioridade: "alto"   },
  { id: "sorocaba",   nome: "Sorocaba",                eleit: 2100000,  municipios: 79,  cobertura: 0,    spend: 0,    prioridade: "alto"   },
  { id: "sjc",        nome: "S. José dos Campos",      eleit: 1900000,  municipios: 39,  cobertura: 0,    spend: 0,    prioridade: "alto"   },
  { id: "ribeirao",   nome: "Ribeirão Preto",          eleit: 1800000,  municipios: 96,  cobertura: 0,    spend: 0,    prioridade: "medio"  },
  { id: "santos",     nome: "Santos / Baixada",        eleit: 1600000,  municipios: 9,   cobertura: 0,    spend: 0,    prioridade: "medio"  },
  { id: "vale_para",  nome: "Vale do Paraíba",         eleit: 1400000,  municipios: 39,  cobertura: 0.3,  spend: 26,   prioridade: "medio"  },
  { id: "sao_rpreto", nome: "S. José do Rio Preto",   eleit: 1300000,  municipios: 96,  cobertura: 0,    spend: 0,    prioridade: "medio"  },
  { id: "piracicaba", nome: "Piracicaba",              eleit: 850000,   municipios: 26,  cobertura: 0,    spend: 0,    prioridade: "medio"  },
  { id: "bauru",      nome: "Bauru",                   eleit: 1100000,  municipios: 71,  cobertura: 0,    spend: 0,    prioridade: "medio"  },
  { id: "presidente", nome: "Presidente Prudente",     eleit: 950000,   municipios: 102, cobertura: 0,    spend: 0,    prioridade: "baixo"  },
  { id: "marilia",    nome: "Marília",                 eleit: 700000,   municipios: 51,  cobertura: 0,    spend: 0,    prioridade: "baixo"  },
  { id: "aracatuba",  nome: "Araçatuba",               eleit: 650000,   municipios: 42,  cobertura: 0,    spend: 0,    prioridade: "baixo"  },
  { id: "franca",     nome: "Franca",                  eleit: 600000,   municipios: 22,  cobertura: 0,    spend: 0,    prioridade: "baixo"  },
  { id: "registro",   nome: "Registro / Vale Ribeira", eleit: 280000,   municipios: 25,  cobertura: 0,    spend: 0,    prioridade: "baixo"  },
];

```

- [ ] **Step 2: Verificar no browser**

Abrir `david-soares-dashboard.html` no browser. Abrir DevTools (F12) → Console. Digitar `MACRORREGIOES.length`.
Esperado: `15`

- [ ] **Step 3: Commit**

```bash
git add david-soares-dashboard.html
git commit -m "feat: add MACRORREGIOES data array (15 IBGE regions)"
```

---

## Task 2: Expandir `UNTAPPED` para 25 cidades com campo `regiao`

**Files:**
- Modify: `david-soares-dashboard.html:977-1038` (substituir `const UNTAPPED = [...]`)

- [ ] **Step 1: Substituir o bloco `const UNTAPPED` (linhas 977–1038) pelo seguinte**

```js
const UNTAPPED = [
  { city: "Guarulhos",              regiao: "Grande São Paulo",   pop: "1,4M",  eleit: "~900K",  prio: "alto"  },
  { city: "Campinas",               regiao: "Campinas",           pop: "1,2M",  eleit: "~800K",  prio: "alto"  },
  { city: "Sorocaba",               regiao: "Sorocaba",           pop: "700K",  eleit: "~460K",  prio: "alto"  },
  { city: "São José dos Campos",    regiao: "Vale do Paraíba",    pop: "730K",  eleit: "~490K",  prio: "alto"  },
  { city: "Ribeirão Preto",         regiao: "Ribeirão Preto",     pop: "720K",  eleit: "~500K",  prio: "alto"  },
  { city: "Santo André",            regiao: "Grande São Paulo",   pop: "720K",  eleit: "~480K",  prio: "alto"  },
  { city: "São Bernardo do Campo",  regiao: "Grande São Paulo",   pop: "840K",  eleit: "~560K",  prio: "medio" },
  { city: "Osasco",                 regiao: "Grande São Paulo",   pop: "700K",  eleit: "~450K",  prio: "medio" },
  { city: "Santos",                 regiao: "Santos / Baixada",   pop: "440K",  eleit: "~300K",  prio: "medio" },
  { city: "Jundiaí",                regiao: "Campinas",           pop: "430K",  eleit: "~290K",  prio: "medio" },
  { city: "Mogi das Cruzes",        regiao: "Grande São Paulo",   pop: "460K",  eleit: "~310K",  prio: "medio" },
  { city: "Piracicaba",             regiao: "Piracicaba",         pop: "420K",  eleit: "~280K",  prio: "medio" },
  { city: "São José do Rio Preto",  regiao: "S. José do Rio Preto", pop: "470K", eleit: "~320K", prio: "medio" },
  { city: "Taubaté",                regiao: "Vale do Paraíba",    pop: "320K",  eleit: "~210K",  prio: "medio" },
  { city: "Bauru",                  regiao: "Bauru",              pop: "390K",  eleit: "~260K",  prio: "medio" },
  { city: "Mauá",                   regiao: "Grande São Paulo",   pop: "470K",  eleit: "~310K",  prio: "medio" },
  { city: "Franca",                 regiao: "Franca",             pop: "360K",  eleit: "~240K",  prio: "medio" },
  { city: "Limeira",                regiao: "Campinas",           pop: "320K",  eleit: "~210K",  prio: "medio" },
  { city: "Americana",              regiao: "Campinas",           pop: "240K",  eleit: "~160K",  prio: "medio" },
  { city: "São Carlos",             regiao: "Ribeirão Preto",     pop: "260K",  eleit: "~175K",  prio: "medio" },
  { city: "Presidente Prudente",    regiao: "Presidente Prudente",pop: "230K",  eleit: "~155K",  prio: "baixo" },
  { city: "Araçatuba",              regiao: "Araçatuba",          pop: "230K",  eleit: "~155K",  prio: "baixo" },
  { city: "Marília",                regiao: "Marília",            pop: "240K",  eleit: "~160K",  prio: "baixo" },
  { city: "Araraquara",             regiao: "Ribeirão Preto",     pop: "240K",  eleit: "~160K",  prio: "baixo" },
  { city: "Botucatu",               regiao: "Bauru",              pop: "150K",  eleit: "~100K",  prio: "baixo" },
];
```

- [ ] **Step 2: Verificar no browser**

Console DevTools → digitar `UNTAPPED.length`.
Esperado: `25`

Console → digitar `UNTAPPED[0].regiao`.
Esperado: `"Grande São Paulo"`

- [ ] **Step 3: Commit**

```bash
git add david-soares-dashboard.html
git commit -m "feat: expand UNTAPPED to 25 cities with regiao field"
```

---

## Task 3: Atualizar HTML da seção geográfica

**Files:**
- Modify: `david-soares-dashboard.html:521-535`

- [ ] **Step 1: Substituir o bloco HTML da seção geográfica (linhas 521–537)**

Localizar o bloco:
```html
<!-- CITIES -->
<div class="sec">MAPA ESTRATÉGICO SP — REGIÕES COM CAMPANHA + OPORTUNIDADES</div>
<div class="city-grid" style="animation:up .5s ease .25s both">
  <div class="panel">
    <div class="ptitle">REGIÕES ATIVAS — ENGAJAMENTO E RECOMENDAÇÃO</div>
    <table class="city-table"><thead><tr><th>REGIÃO / CIDADE</th><th>GASTO</th><th>ALCANCE</th><th>ENGAJ.</th><th>CPEE</th><th>INVESTIR</th></tr></thead>
    <tbody id="city-tbody"></tbody></table>
  </div>
  <div class="panel pp">
    <div class="ptitle" style="color:var(--p2)">CIDADES SEM CAMPANHA — POTENCIAL NÃO EXPLORADO</div>
    <table class="city-table"><thead><tr><th>CIDADE</th><th>POPULAÇÃO</th><th>ELEITORADO</th><th>PRIORIDADE</th></tr></thead>
    <tbody id="untapped-tbody"></tbody></table>
    <div style="margin-top:10px;padding-top:8px;border-top:1px solid rgba(107,45,139,.12);font-family:var(--fb);font-size:.76rem;color:var(--b2);line-height:1.5">
      💡 <strong style="color:var(--p2)">SP capital concentra 99,7% do alcance atual.</strong>
      Guarulhos, Santo André e Campinas oferecem ~2M de eleitores ainda não alcançados.
    </div>
  </div>
</div>
```

E substituir por:
```html
<!-- CITIES -->
<div class="sec">COBERTURA ELEITORAL — ESTADO DE SÃO PAULO (645 MUNICÍPIOS · ~34M ELEITORES)</div>
<div class="city-grid" style="animation:up .5s ease .25s both">
  <div class="panel">
    <div class="ptitle">COBERTURA POR MACRORREGIÃO — 15 REGIÕES IBGE</div>
    <table class="city-table"><thead><tr><th>MACRORREGIÃO</th><th>MUNICÍPIOS</th><th>ELEITORADO</th><th>COBERTURA ATUAL</th><th>GASTO</th><th>PRIORIDADE</th></tr></thead>
    <tbody id="macro-tbody"></tbody></table>
  </div>
  <div class="panel pp">
    <div class="ptitle" style="color:var(--p2)">TOP 25 CIDADES SEM CAMPANHA — INTERIOR DO ESTADO</div>
    <table class="city-table"><thead><tr><th>CIDADE</th><th>REGIÃO</th><th>POPULAÇÃO</th><th>ELEITORADO</th><th>PRIORIDADE</th></tr></thead>
    <tbody id="untapped-tbody"></tbody></table>
    <div style="margin-top:10px;padding-top:8px;border-top:1px solid rgba(107,45,139,.12);font-family:var(--fb);font-size:.76rem;color:var(--b2);line-height:1.5">
      💡 <strong style="color:var(--p2)">Grande SP concentra 99,7% do alcance atual.</strong>
      As demais 14 macrorregiões somam ~18,2M eleitores — 53% do eleitorado estadual — sem presença de campanha.
    </div>
  </div>
</div>
```

- [ ] **Step 2: Verificar no browser**

Abrir o arquivo. A seção deve mostrar o novo cabeçalho "COBERTURA ELEITORAL — ESTADO DE SÃO PAULO..." e as duas tabelas vazias (ainda sem dados, pois as funções JS ainda não foram atualizadas).

- [ ] **Step 3: Commit**

```bash
git add david-soares-dashboard.html
git commit -m "feat: update geo section HTML — state-wide header and new table structure"
```

---

## Task 4: Substituir funções JS de renderização

**Files:**
- Modify: `david-soares-dashboard.html:1335-1365`

- [ ] **Step 1: Adicionar função utilitária `coverageBar` e substituir `renderCities`**

Localizar o bloco inteiro (linhas 1335–1365):
```js
let _untappedRendered=false;
function renderCities(cities){
  const tb=document.getElementById('city-tbody');tb.innerHTML='';
  [...cities].sort((a,b)=>b.eng-a.eng).forEach(c=>{
    const rc={'alto':'ba','medio':'bm','baixo':'bb'}[c.rec];
    const rl={'alto':'↑ MAIS','medio':'→ MANTER','baixo':'↓ REVISAR'}[c.rec];
    const cc=c.cpee<0.01?'var(--g)':c.cpee<0.05?'#C9A227':'var(--p2)';
    tb.innerHTML+=`<tr>
      <td>${c.city}</td>
      <td style="font-family:var(--fm);font-size:.57rem">${fmtBRL(c.spend)}</td>
      <td style="font-family:var(--fm);font-size:.57rem">${fmtN(c.reach)}</td>
      <td style="font-family:var(--fm);font-size:.57rem">${fmtN(c.eng)}</td>
      <td style="font-family:var(--fm);font-size:.57rem;color:${cc}">R$${c.cpee.toFixed(4)}</td>
      <td><span class="badge ${rc}">${rl}</span></td>
    </tr>`;
  });
  if(!_untappedRendered){
    _untappedRendered=true;
    const tb2=document.getElementById('untapped-tbody');
    UNTAPPED.forEach(c=>{
      const rc={'alto':'ba','medio':'bm','baixo':'bb'}[c.prio];
      const rl={'alto':'⭐ ALTA','medio':'MÉDIA','baixo':'BAIXA'}[c.prio];
      tb2.innerHTML+=`<tr>
        <td>${c.city}</td>
        <td style="font-family:var(--fm);font-size:.57rem">${c.pop}</td>
        <td style="font-family:var(--fm);font-size:.57rem">${c.eleit}</td>
        <td><span class="badge ${rc}">${rl}</span></td>
      </tr>`;
    });
  }
}
```

E substituir por:
```js
function coverageBar(pct){
  const color=pct>=50?'var(--g)':pct>=5?'#C9A227':'var(--p2)';
  const w=Math.min(pct,100)*0.8;
  return `<svg width="80" height="10" style="vertical-align:middle;margin-right:4px"><rect width="80" height="10" rx="3" fill="rgba(255,255,255,.08)"/><rect width="${w}" height="10" rx="3" fill="${color}"/></svg>${pct.toFixed(1)}%`;
}

let _untappedRendered=false;
function renderMacrorregioes(){
  const tb=document.getElementById('macro-tbody');
  if(!tb)return;
  tb.innerHTML='';
  const prioClass={'ativo':'ba','alto':'ba','medio':'bm','baixo':'bb'};
  const prioLabel={'ativo':'✅ ATIVO','alto':'↑ EXPANDIR','medio':'→ PLANEJAR','baixo':'↓ AGUARDAR'};
  MACRORREGIOES.forEach(r=>{
    const isAtivo=r.prioridade==='ativo';
    const rowStyle=isAtivo?'background:rgba(0,166,81,.06)':'';
    tb.innerHTML+=`<tr style="${rowStyle}">
      <td style="${isAtivo?'color:var(--g);font-weight:600':''}">${r.nome}</td>
      <td style="font-family:var(--fm);font-size:.57rem;text-align:center">${r.municipios}</td>
      <td style="font-family:var(--fm);font-size:.57rem">${fmtN(r.eleit)}</td>
      <td style="font-family:var(--fm);font-size:.57rem">${coverageBar(r.cobertura)}</td>
      <td style="font-family:var(--fm);font-size:.57rem">${r.spend>0?fmtBRL(r.spend):'—'}</td>
      <td><span class="badge ${prioClass[r.prioridade]}">${prioLabel[r.prioridade]}</span></td>
    </tr>`;
  });
  if(!_untappedRendered){
    _untappedRendered=true;
    const tb2=document.getElementById('untapped-tbody');
    const prioC={'alto':'ba','medio':'bm','baixo':'bb'};
    const prioL={'alto':'⭐ ALTA','medio':'MÉDIA','baixo':'BAIXA'};
    UNTAPPED.forEach(c=>{
      tb2.innerHTML+=`<tr>
        <td>${c.city}</td>
        <td style="font-family:var(--fm);font-size:.57rem;color:var(--dim)">${c.regiao}</td>
        <td style="font-family:var(--fm);font-size:.57rem">${c.pop}</td>
        <td style="font-family:var(--fm);font-size:.57rem">${c.eleit}</td>
        <td><span class="badge ${prioC[c.prio]}">${prioL[c.prio]}</span></td>
      </tr>`;
    });
  }
}
```

- [ ] **Step 2: Verificar no browser**

Console DevTools → digitar `coverageBar(99.7)`.
Esperado: string HTML com SVG e `"99.7%"`.

- [ ] **Step 3: Commit**

```bash
git add david-soares-dashboard.html
git commit -m "feat: replace renderCities with renderMacrorregioes + coverageBar"
```

---

## Task 5: Atualizar chamada `renderCities` → `renderMacrorregioes`

**Files:**
- Modify: `david-soares-dashboard.html:1440`

- [ ] **Step 1: Substituir a chamada na função `renderBreakdowns`**

Localizar (linha ~1440):
```js
  renderCities(bd.cities);
```

Substituir por:
```js
  renderMacrorregioes();
```

- [ ] **Step 2: Verificar no browser — teste completo**

Abrir `david-soares-dashboard.html`.

Verificar:
1. Cabeçalho da seção mostra "COBERTURA ELEITORAL — ESTADO DE SÃO PAULO (645 MUNICÍPIOS · ~34M ELEITORES)"
2. Tabela da esquerda mostra 15 linhas, uma por macrorregião
3. "Grande São Paulo" aparece com fundo levemente verde e barra de cobertura em ~99,7%
4. Demais regiões mostram barra vermelha/roxa com 0% ou 0,1%/0,3%
5. Tabela da direita mostra 25 cidades com coluna REGIÃO preenchida
6. Nota inferior mostra "Grande SP concentra 99,7%... 53% do eleitorado estadual"
7. Trocar o seletor de período (7/14/28/30/60/90 dias) — as tabelas devem permanecer estáveis (dados estáticos)
8. Nenhum erro no Console

- [ ] **Step 3: Commit final**

```bash
git add david-soares-dashboard.html
git commit -m "feat: wire renderMacrorregioes into renderBreakdowns"
```

---

## Task 6: Publicar no GitHub Pages

**Files:**
- Remote: `origin/main` → branch `main`

- [ ] **Step 1: Push para o repositório**

```bash
git push origin main
```

- [ ] **Step 2: Verificar no GitHub Pages**

Aguardar ~60 segundos e abrir `https://minhacatarsebr-source.github.io/projetodeputado/`.

Verificar que as mesmas 15 macrorregiões e 25 cidades aparecem corretamente no site publicado.
