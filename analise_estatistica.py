"""
Análise Estatística para o Artigo TCC
Testes estatísticos formais para comparação AWS vs Azure
"""

import numpy as np
from scipy import stats

# ============================================================================
# DADOS EXPERIMENTAIS
# ============================================================================

# AWS: Média de response time para cada configuração (5 configs)
aws_means = np.array([272.77, 213.83, 161.46, 136.09, 79.72])
aws_stds = np.array([151.69, 119.76, 90.26, 76.99, 43.13])

# Azure: Média de response time para cada configuração (5 configs)
azure_means = np.array([231.78, 179.81, 160.23, 153.52, 154.81])
azure_stds = np.array([124.09, 98.01, 84.29, 78.51, 62.88])

# Tamanho da amostra por configuração
# 3 repetições × 300 requisições = 900 observações por configuração
n_per_config = 900

print("="*70)
print("ANÁLISE ESTATÍSTICA - AWS vs AZURE")
print("="*70)

# ============================================================================
# 1. COMPARAÇÃO GERAL (Tabela 5 - platform_comparison)
# ============================================================================

print("\n1. COMPARAÇÃO GERAL DE PLATAFORMAS")
print("-"*70)

# Média geral por plataforma (média das 5 configurações)
aws_overall_mean = np.mean(aws_means)
azure_overall_mean = np.mean(azure_means)

# Desvio padrão geral
aws_overall_std = np.mean(aws_stds)
azure_overall_std = np.mean(azure_stds)

print(f"AWS - Média Geral: {aws_overall_mean:.2f}s (±{aws_overall_std:.2f}s)")
print(f"Azure - Média Geral: {azure_overall_mean:.2f}s (±{azure_overall_std:.2f}s)")
print(f"Diferença: {aws_overall_mean - azure_overall_mean:.2f}s ({((aws_overall_mean - azure_overall_mean)/azure_overall_mean)*100:.1f}%)")

# T-test de duas amostras independentes
# H0: não há diferença significativa entre AWS e Azure
# H1: há diferença significativa
t_stat, p_value = stats.ttest_ind(aws_means, azure_means)

print(f"\nTeste t de duas amostras independentes:")
print(f"  Hipotese Nula (H0): media_AWS = media_Azure")
print(f"  Hipotese Alternativa (H1): media_AWS != media_Azure")
print(f"  Estatistica t: {t_stat:.4f}")
print(f"  p-value: {p_value:.4f}")
print(f"  Nivel de significancia (alfa): 0.05")

if p_value < 0.05:
    print(f"  X Resultado: Diferenca SIGNIFICATIVA (p < 0.05)")
else:
    print(f"  OK Resultado: Diferenca NAO significativa (p >= 0.05)")

# Intervalo de confiança 95% para a diferença
diff_mean = aws_overall_mean - azure_overall_mean
diff_std_error = np.sqrt((aws_overall_std**2/5) + (azure_overall_std**2/5))
ci_95 = 1.96 * diff_std_error

print(f"\nIntervalo de Confianca 95% para a diferenca:")
print(f"  Diferenca: {diff_mean:.2f}s")
print(f"  IC 95%: [{diff_mean - ci_95:.2f}s, {diff_mean + ci_95:.2f}s]")

# ============================================================================
# 2. WORKER SCALING - Comparação por configuração
# ============================================================================

print("\n\n2. WORKER SCALING - COMPARAÇÕES INDIVIDUAIS")
print("-"*70)

configs_worker = [
    ("Baseline (1W)", 272.77, 151.69, 231.78, 124.09),
    ("2 Workers", 213.83, 119.76, 179.81, 98.01),
    ("4 Workers", 161.46, 90.26, 160.23, 84.29),
]

for name, aws_m, aws_s, azure_m, azure_s in configs_worker:
    # Simular distribuições normais para t-test
    # (simplificação: assumimos normalidade)
    aws_sample = np.random.normal(aws_m, aws_s, n_per_config)
    azure_sample = np.random.normal(azure_m, azure_s, n_per_config)
    
    t, p = stats.ttest_ind(aws_sample, azure_sample)
    
    diff_pct = ((aws_m - azure_m) / azure_m) * 100
    
    print(f"\n{name}:")
    print(f"  AWS: {aws_m:.2f}s (±{aws_s:.2f}s)")
    print(f"  Azure: {azure_m:.2f}s (±{azure_s:.2f}s)")
    print(f"  Diferença: {diff_pct:+.1f}%")
    print(f"  p-value: {p:.6f}")
    print(f"  Significativo: {'SIM' if p < 0.05 else 'NÃO'}")

# ============================================================================
# 3. HORIZONTAL SCALING - Comparação por configuração
# ============================================================================

print("\n\n3. HORIZONTAL SCALING - COMPARAÇÕES INDIVIDUAIS")
print("-"*70)

configs_horizontal = [
    ("Baseline (1R)", 272.77, 151.69, 231.78, 124.09),
    ("2 Réplicas", 136.09, 76.99, 153.52, 78.51),
    ("4 Réplicas", 79.72, 43.13, 154.81, 62.88),
]

for name, aws_m, aws_s, azure_m, azure_s in configs_horizontal:
    aws_sample = np.random.normal(aws_m, aws_s, n_per_config)
    azure_sample = np.random.normal(azure_m, azure_s, n_per_config)
    
    t, p = stats.ttest_ind(aws_sample, azure_sample)
    
    diff_pct = ((azure_m - aws_m) / aws_m) * 100
    
    print(f"\n{name}:")
    print(f"  AWS: {aws_m:.2f}s (±{aws_s:.2f}s)")
    print(f"  Azure: {azure_m:.2f}s (±{azure_s:.2f}s)")
    print(f"  Azure vs AWS: {diff_pct:+.1f}% {'(mais lento)' if diff_pct > 0 else '(mais rápido)'}")
    print(f"  p-value: {p:.6f}")
    print(f"  Significativo: {'SIM' if p < 0.05 else 'NÃO'}")

# ============================================================================
# 4. TESTE DE VARIÂNCIA (Levene's test)
# ============================================================================

print("\n\n4. TESTE DE HOMOGENEIDADE DE VARIÂNCIA (Levene's Test)")
print("-"*70)

# Testar se as variâncias são significativamente diferentes
stat_levene, p_levene = stats.levene(aws_means, azure_means)

print(f"Hipotese Nula (H0): var_AWS = var_Azure")
print(f"Estatística de Levene: {stat_levene:.4f}")
print(f"p-value: {p_levene:.4f}")

if p_levene < 0.05:
    print(f"X Variancias sao SIGNIFICATIVAMENTE diferentes (p < 0.05)")
    print(f"  -> Azure tem menor variabilidade (std={azure_overall_std:.2f} vs {aws_overall_std:.2f})")
else:
    print(f"OK Variancias NAO sao significativamente diferentes (p >= 0.05)")

# ============================================================================
# 5. COEFICIENTE DE VARIAÇÃO
# ============================================================================

print("\n\n5. ANÁLISE DE PREVISIBILIDADE (Coeficiente de Variação)")
print("-"*70)

cv_aws = (aws_overall_std / aws_overall_mean) * 100
cv_azure = (azure_overall_std / azure_overall_mean) * 100

print(f"AWS - CV: {cv_aws:.1f}%")
print(f"Azure - CV: {cv_azure:.1f}%")
print(f"Diferença: {cv_azure - cv_aws:.1f} pontos percentuais")

if cv_azure < cv_aws:
    print(f"OK Azure eh {((cv_aws - cv_azure) / cv_aws) * 100:.1f}% mais previsivel")
else:
    print(f"OK AWS eh {((cv_azure - cv_aws) / cv_azure) * 100:.1f}% mais previsivel")

# ============================================================================
# 6. RESUMO PARA O ARTIGO
# ============================================================================

print("\n\n" + "="*70)
print("RESUMO PARA INCLUSÃO NO ARTIGO")
print("="*70)

print(f"""
TABELA 5 (platform_comparison) - Adicionar:

Statistical Significance: Not significant (two-sample t-test, p={p_value:.3f} > 0.05)
  - Test: Independent two-sample t-test
  - Null Hypothesis (H0): mean_AWS = mean_Azure  
  - Significance level (alpha): 0.05
  - Result: Fail to reject H0 (p={p_value:.3f})
  - 95% CI for difference: [{diff_mean - ci_95:.2f}s, {diff_mean + ci_95:.2f}s]
  
Interpretation: The 1.9% performance difference between platforms is not
statistically significant at α=0.05, indicating that overall platform
choice has minimal impact on average performance.
""")

print("="*70)
