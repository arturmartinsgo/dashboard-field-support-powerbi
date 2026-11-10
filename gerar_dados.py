"""Gera dados SINTÉTICOS de um service desk fictício (nenhum dado real)."""
import numpy as np, pandas as pd
rng = np.random.default_rng(42)

tecnicos = pd.DataFrame({
    "tecnico_id": [f"T{i:02d}" for i in range(1, 13)],
    "tecnico": [f"Técnico {i:02d}" for i in range(1, 13)],
    "equipe": ["Equipe A"]*4 + ["Equipe B"]*4 + ["Equipe C"]*4,
})

categorias = {  # categoria: (peso, prioridade_sla_horas)
    "Hardware - Notebook": (0.22, 8), "Hardware - Periféricos": (0.10, 16),
    "Software - Instalação": (0.18, 16), "Software - Erro/Falha": (0.12, 8),
    "Acesso e Senhas": (0.14, 4), "Rede/Conectividade": (0.08, 8),
    "Impressoras": (0.06, 16), "Gestão de Ativos": (0.06, 24),
    "Dispositivos Móveis": (0.04, 8),
}
cats = list(categorias)
inicio = pd.Timestamp("2026-01-05")
n = 1200
dias = rng.integers(0, 300, n)
abertura = inicio + pd.to_timedelta(dias, "D") + pd.to_timedelta(rng.integers(8*60, 17*60, n), "m")
abertura = abertura[abertura.dayofweek < 5] if False else abertura
df = pd.DataFrame({
    "chamado_id": [f"INC{100000+i}" for i in range(n)],
    "abertura": abertura,
    "categoria": rng.choice(cats, n, p=[categorias[c][0] for c in cats]),
    "tecnico_id": rng.choice(tecnicos.tecnico_id, n),
    "usuario_vip": rng.random(n) < 0.08,
})
df["sla_horas"] = df.categoria.map(lambda c: categorias[c][1])
df.loc[df.usuario_vip, "sla_horas"] = (df.sla_horas / 2).clip(lower=2)
# tempo de resolução ~ lognormal, relativo ao SLA
fator = rng.lognormal(mean=-0.7, sigma=0.55, size=n)
df["horas_resolucao"] = (df.sla_horas * fator).round(2)
df["resolucao"] = df.abertura + pd.to_timedelta(df.horas_resolucao, "h")
df["status"] = np.where(rng.random(n) < 0.04, "Em andamento", "Resolvido")
df.loc[df.status == "Em andamento", ["resolucao", "horas_resolucao"]] = [pd.NaT, np.nan]
df["dentro_sla"] = np.where(df.status == "Resolvido", df.horas_resolucao <= df.sla_horas, pd.NA)
df["dias_sem_atualizacao"] = np.where(df.status == "Em andamento", rng.integers(0, 9, n), 0)
df = df.sort_values("abertura")
df.to_csv("dados/chamados.csv", index=False, encoding="utf-8-sig")
tecnicos.to_csv("dados/tecnicos.csv", index=False, encoding="utf-8-sig")
cal = pd.DataFrame({"data": pd.date_range("2026-01-01", "2026-12-31")})
cal["ano"]=cal.data.dt.year; cal["mes"]=cal.data.dt.month; cal["mes_nome"]=cal.data.dt.strftime("%b")
cal["dia_semana"]=cal.data.dt.dayofweek+1
cal.to_csv("dados/calendario.csv", index=False)
print(df.shape, df.status.value_counts().to_dict(), "SLA:", round(df.dentro_sla.dropna().astype(bool).mean(),3))
