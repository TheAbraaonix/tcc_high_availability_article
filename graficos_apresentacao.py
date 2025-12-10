"""
Script para gerar gráficos da apresentação TCC
Comparação AWS vs Azure - Configurações lado a lado
"""

import matplotlib.pyplot as plt
import numpy as np

# Configuração global de estilo
plt.style.use('seaborn-v0_8-darkgrid')
COLORS = {'AWS': '#FF9900', 'Azure': '#0078D4'}  # Cores oficiais
FIGSIZE = (12, 6)

# ============================================================================
# GRÁFICO 1: BASELINE - AWS vs Azure (1 Worker, 1 Replica)
# ============================================================================

def grafico_baseline():
    """Slide 1: Baseline Performance - AWS vs Azure"""
    
    platforms = ['AWS\nBaseline\n(B1)', 'Azure\nBaseline\n(B2)']
    avg_response = [272.77, 231.78]
    std_dev = [151.69, 124.09]
    colors = [COLORS['AWS'], COLORS['Azure']]
    
    fig, ax = plt.subplots(figsize=FIGSIZE)
    
    bars = ax.bar(platforms, avg_response, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax.errorbar(platforms, avg_response, yerr=std_dev, fmt='none', 
                ecolor='black', capsize=10, linewidth=2, capthick=2)
    
    # Adicionar valores nas barras
    for i, (bar, val, std) in enumerate(zip(bars, avg_response, std_dev)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + std + 10,
                f'{val:.1f}s\n(±{std:.1f}s)',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax.set_ylabel('Tempo de Resposta Médio (s)', fontsize=14, fontweight='bold')
    ax.set_title('Baseline Performance - AWS vs Azure\n(4 vCPU, 8GB RAM, 1 Worker, 1 Réplica)', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_ylim(0, max(avg_response) + max(std_dev) + 50)
    ax.grid(axis='y', alpha=0.3)
    
    # Rodapé com interpretação
    footer_text = ('Azure é 15% mais rápido no baseline (231.78s vs 272.77s) e 19% mais consistente (menor desvio padrão). '
                   'AWS apresenta menor tempo mínimo (2.72s vs 10.30s), provavelmente devido a otimizações de primeira requisição.')
    
    plt.figtext(0.5, -0.05, footer_text, ha='center', fontsize=10, 
                style='italic', wrap=True, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    plt.tight_layout()
    plt.savefig('slide_1_baseline.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfico 1 salvo: slide_1_baseline.png")
    plt.close()


# ============================================================================
# GRÁFICO 2: WORKER SCALING - 2 Workers
# ============================================================================

def grafico_2_workers():
    """Slide 2: Worker Scaling - 2 Workers AWS vs Azure"""
    
    platforms = ['AWS\n2 Workers\n(WS1)', 'Azure\n2 Workers\n(WS3)']
    avg_response = [213.83, 179.81]
    std_dev = [119.76, 98.01]
    speedup = [1.28, 1.29]
    colors = [COLORS['AWS'], COLORS['Azure']]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Subplot 1: Tempo de resposta
    bars1 = ax1.bar(platforms, avg_response, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax1.errorbar(platforms, avg_response, yerr=std_dev, fmt='none', 
                 ecolor='black', capsize=10, linewidth=2, capthick=2)
    
    for bar, val, std in zip(bars1, avg_response, std_dev):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + std + 5,
                 f'{val:.1f}s\n(±{std:.1f}s)',
                 ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax1.set_ylabel('Tempo de Resposta Médio (s)', fontsize=13, fontweight='bold')
    ax1.set_title('Tempo de Resposta - 2 Workers', fontsize=14, fontweight='bold')
    ax1.set_ylim(0, max(avg_response) + max(std_dev) + 30)
    ax1.grid(axis='y', alpha=0.3)
    
    # Subplot 2: Speedup
    bars2 = ax2.bar(platforms, speedup, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    for bar, val in zip(bars2, speedup):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                 f'{val:.2f}×',
                 ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax2.axhline(y=2.0, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Linear (2×)')
    ax2.set_ylabel('Speedup', fontsize=13, fontweight='bold')
    ax2.set_title('Speedup vs Baseline', fontsize=14, fontweight='bold')
    ax2.set_ylim(0, 2.5)
    ax2.legend(fontsize=11)
    ax2.grid(axis='y', alpha=0.3)
    
    plt.suptitle('Worker Scaling - 2 Workers (AWS vs Azure)', fontsize=16, fontweight='bold', y=1.02)
    
    # Rodapé com interpretação
    footer_text = ('Azure mantém vantagem de desempenho com 2 workers (179.81s vs 213.83s = 16% mais rápido). '
                   'Ambas plataformas apresentam speedup similar (~1.28×), indicando eficiência equivalente no worker scaling inicial.')
    
    plt.figtext(0.5, -0.05, footer_text, ha='center', fontsize=10, 
                style='italic', wrap=True, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    plt.tight_layout()
    plt.savefig('slide_2_workers_2.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfico 2 salvo: slide_2_workers_2.png")
    plt.close()


# ============================================================================
# GRÁFICO 3: WORKER SCALING - 4 Workers
# ============================================================================

def grafico_4_workers():
    """Slide 3: Worker Scaling - 4 Workers AWS vs Azure"""
    
    platforms = ['AWS\n4 Workers\n(WS2)', 'Azure\n4 Workers\n(WS4)']
    avg_response = [161.46, 160.23]
    std_dev = [90.26, 84.29]
    speedup = [1.69, 1.45]
    colors = [COLORS['AWS'], COLORS['Azure']]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Subplot 1: Tempo de resposta
    bars1 = ax1.bar(platforms, avg_response, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax1.errorbar(platforms, avg_response, yerr=std_dev, fmt='none', 
                 ecolor='black', capsize=10, linewidth=2, capthick=2)
    
    for bar, val, std in zip(bars1, avg_response, std_dev):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + std + 5,
                 f'{val:.1f}s\n(±{std:.1f}s)',
                 ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax1.set_ylabel('Tempo de Resposta Médio (s)', fontsize=13, fontweight='bold')
    ax1.set_title('Tempo de Resposta - 4 Workers', fontsize=14, fontweight='bold')
    ax1.set_ylim(0, max(avg_response) + max(std_dev) + 30)
    ax1.grid(axis='y', alpha=0.3)
    
    # Subplot 2: Speedup
    bars2 = ax2.bar(platforms, speedup, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    for bar, val in zip(bars2, speedup):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                 f'{val:.2f}×',
                 ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax2.axhline(y=4.0, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Linear (4×)')
    ax2.set_ylabel('Speedup', fontsize=13, fontweight='bold')
    ax2.set_title('Speedup vs Baseline', fontsize=14, fontweight='bold')
    ax2.set_ylim(0, 4.5)
    ax2.legend(fontsize=11)
    ax2.grid(axis='y', alpha=0.3)
    
    plt.suptitle('Worker Scaling - 4 Workers (AWS vs Azure)', fontsize=16, fontweight='bold', y=1.02)
    
    # Rodapé com interpretação
    footer_text = ('Convergência de desempenho: apenas 0.8% de diferença (161.46s vs 160.23s). '
                   'AWS apresenta 16.6% maior eficiência no speedup (1.69× vs 1.45×), mas desempenho absoluto é praticamente idêntico.')
    
    plt.figtext(0.5, -0.05, footer_text, ha='center', fontsize=10, 
                style='italic', wrap=True, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    plt.tight_layout()
    plt.savefig('slide_3_workers_4.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfico 3 salvo: slide_3_workers_4.png")
    plt.close()


# ============================================================================
# GRÁFICO 4: HORIZONTAL SCALING - 2 Réplicas
# ============================================================================

def grafico_2_replicas():
    """Slide 4: Horizontal Scaling - 2 Réplicas AWS vs Azure"""
    
    platforms = ['AWS\n2 Réplicas\n(HS1)', 'Azure\n2 Réplicas\n(HS3)']
    avg_response = [136.09, 153.52]
    std_dev = [76.99, 78.51]
    speedup = [2.00, 1.51]
    colors = [COLORS['AWS'], COLORS['Azure']]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Subplot 1: Tempo de resposta
    bars1 = ax1.bar(platforms, avg_response, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax1.errorbar(platforms, avg_response, yerr=std_dev, fmt='none', 
                 ecolor='black', capsize=10, linewidth=2, capthick=2)
    
    for bar, val, std in zip(bars1, avg_response, std_dev):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + std + 5,
                 f'{val:.1f}s\n(±{std:.1f}s)',
                 ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax1.set_ylabel('Tempo de Resposta Médio (s)', fontsize=13, fontweight='bold')
    ax1.set_title('Tempo de Resposta - 2 Réplicas', fontsize=14, fontweight='bold')
    ax1.set_ylim(0, max(avg_response) + max(std_dev) + 30)
    ax1.grid(axis='y', alpha=0.3)
    
    # Subplot 2: Speedup
    bars2 = ax2.bar(platforms, speedup, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    for bar, val in zip(bars2, speedup):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                 f'{val:.2f}×',
                 ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax2.axhline(y=2.0, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Linear (2×)')
    ax2.set_ylabel('Speedup', fontsize=13, fontweight='bold')
    ax2.set_title('Speedup vs Baseline', fontsize=14, fontweight='bold')
    ax2.set_ylim(0, 2.5)
    ax2.legend(fontsize=11)
    ax2.grid(axis='y', alpha=0.3)
    
    plt.suptitle('Horizontal Scaling - 2 Réplicas (AWS vs Azure)', fontsize=16, fontweight='bold', y=1.02)
    
    # Rodapé com interpretação
    footer_text = ('AWS atinge escalonamento linear perfeito (2.00× speedup) com 2 réplicas. '
                   'Azure alcança 1.51× speedup. AWS 11% mais rápido (136.09s vs 153.52s).')
    
    plt.figtext(0.5, -0.05, footer_text, ha='center', fontsize=10, 
                style='italic', wrap=True, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    plt.tight_layout()
    plt.savefig('slide_4_horizontal_2.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfico 4 salvo: slide_4_horizontal_2.png")
    plt.close()


# ============================================================================
# GRÁFICO 5: HORIZONTAL SCALING - 4 Réplicas (PRINCIPAL ACHADO!)
# ============================================================================

def grafico_4_replicas():
    """Slide 5: Horizontal Scaling - 4 Réplicas AWS vs Azure (ACHADO PRINCIPAL)"""
    
    platforms = ['AWS\n4 Réplicas\n(HS2)', 'Azure\n4 Réplicas\n(HS4)']
    avg_response = [79.72, 154.81]
    std_dev = [43.13, 62.88]
    speedup = [3.42, 1.50]
    colors = [COLORS['AWS'], COLORS['Azure']]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Subplot 1: Tempo de resposta
    bars1 = ax1.bar(platforms, avg_response, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax1.errorbar(platforms, avg_response, yerr=std_dev, fmt='none', 
                 ecolor='black', capsize=10, linewidth=2, capthick=2)
    
    for bar, val, std in zip(bars1, avg_response, std_dev):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + std + 5,
                 f'{val:.1f}s\n(±{std:.1f}s)',
                 ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax1.set_ylabel('Tempo de Resposta Médio (s)', fontsize=13, fontweight='bold')
    ax1.set_title('Tempo de Resposta - 4 Réplicas', fontsize=14, fontweight='bold')
    ax1.set_ylim(0, max(avg_response) + max(std_dev) + 30)
    ax1.grid(axis='y', alpha=0.3)
    
    # Subplot 2: Speedup
    bars2 = ax2.bar(platforms, speedup, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    for bar, val in zip(bars2, speedup):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                 f'{val:.2f}×',
                 ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax2.axhline(y=4.0, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Linear (4×)')
    ax2.set_ylabel('Speedup', fontsize=13, fontweight='bold')
    ax2.set_title('Speedup vs Baseline', fontsize=14, fontweight='bold')
    ax2.set_ylim(0, 4.5)
    ax2.legend(fontsize=11)
    ax2.grid(axis='y', alpha=0.3)
    
    plt.suptitle('Horizontal Scaling - 4 Réplicas (AWS vs Azure) - ACHADO PRINCIPAL', 
                 fontsize=16, fontweight='bold', y=1.02, color='red')
    
    # Rodapé com interpretação
    footer_text = ('⚡ ACHADO PRINCIPAL: AWS 94% mais rápido (79.72s vs 154.81s) com 3.42× speedup. '
                   'Azure apresenta plateau em 2 réplicas (1.50× vs 1.51×) - sem ganho adicional. '
                   'Diferença de 128% na eficiência de escalonamento.')
    
    plt.figtext(0.5, -0.05, footer_text, ha='center', fontsize=10, fontweight='bold',
                wrap=True, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('slide_5_horizontal_4.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfico 5 salvo: slide_5_horizontal_4.png (ACHADO PRINCIPAL)")
    plt.close()


# ============================================================================
# GRÁFICO 6: COMPARAÇÃO GERAL - Worker vs Horizontal (AWS)
# ============================================================================

def grafico_comparacao_aws():
    """Slide 6: Comparação Worker vs Horizontal Scaling - AWS"""
    
    configs = ['Baseline\n(1W, 1R)', '2 Workers\n(WS1)', '4 Workers\n(WS2)', 
               '2 Réplicas\n(HS1)', '4 Réplicas\n(HS2)']
    avg_response = [272.77, 213.83, 161.46, 136.09, 79.72]
    speedup = [1.00, 1.28, 1.69, 2.00, 3.42]
    colors_bars = ['gray', 'lightblue', 'lightblue', 'lightcoral', 'lightcoral']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Subplot 1: Tempo de resposta
    bars1 = ax1.bar(configs, avg_response, color=colors_bars, alpha=0.8, 
                    edgecolor='black', linewidth=1.5)
    
    for bar, val in zip(bars1, avg_response):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 5,
                 f'{val:.1f}s',
                 ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax1.set_ylabel('Tempo de Resposta Médio (s)', fontsize=13, fontweight='bold')
    ax1.set_title('Tempo de Resposta - Todas Configurações AWS', fontsize=14, fontweight='bold')
    ax1.set_ylim(0, max(avg_response) + 30)
    ax1.grid(axis='y', alpha=0.3)
    ax1.tick_params(axis='x', rotation=15)
    
    # Subplot 2: Speedup
    bars2 = ax2.bar(configs, speedup, color=colors_bars, alpha=0.8, 
                    edgecolor='black', linewidth=1.5)
    
    for bar, val in zip(bars2, speedup):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                 f'{val:.2f}×',
                 ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax2.axhline(y=4.0, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Linear (4×)')
    ax2.set_ylabel('Speedup', fontsize=13, fontweight='bold')
    ax2.set_title('Speedup - Todas Configurações AWS', fontsize=14, fontweight='bold')
    ax2.set_ylim(0, 4.5)
    ax2.legend(fontsize=11)
    ax2.grid(axis='y', alpha=0.3)
    ax2.tick_params(axis='x', rotation=15)
    
    # Adicionar legenda de cores
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='gray', label='Baseline'),
                      Patch(facecolor='lightblue', label='Worker Scaling'),
                      Patch(facecolor='lightcoral', label='Horizontal Scaling')]
    ax2.legend(handles=legend_elements, loc='upper right', fontsize=10)
    
    plt.suptitle('AWS: Worker vs Horizontal Scaling', fontsize=16, fontweight='bold', y=1.02)
    
    # Rodapé com interpretação
    footer_text = ('Horizontal scaling é claramente superior no AWS: 3.42× vs 1.69× (102% mais eficiente). '
                   'Redução de 272.77s para 79.72s (71% de melhoria). '
                   'Recomendação: priorizar horizontal scaling com ALB no AWS.')
    
    plt.figtext(0.5, -0.05, footer_text, ha='center', fontsize=10, 
                style='italic', wrap=True, bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.4))
    
    plt.tight_layout()
    plt.savefig('slide_6_comparacao_aws.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfico 6 salvo: slide_6_comparacao_aws.png")
    plt.close()


# ============================================================================
# GRÁFICO 7: COMPARAÇÃO GERAL - Worker vs Horizontal (Azure)
# ============================================================================

def grafico_comparacao_azure():
    """Slide 7: Comparação Worker vs Horizontal Scaling - Azure"""
    
    configs = ['Baseline\n(1W, 1R)', '2 Workers\n(WS3)', '4 Workers\n(WS4)', 
               '2 Réplicas\n(HS3)', '4 Réplicas\n(HS4)']
    avg_response = [231.78, 179.81, 160.23, 153.52, 154.81]
    speedup = [1.00, 1.29, 1.45, 1.51, 1.50]
    colors_bars = ['gray', 'lightblue', 'lightblue', 'lightcoral', 'lightcoral']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Subplot 1: Tempo de resposta
    bars1 = ax1.bar(configs, avg_response, color=colors_bars, alpha=0.8, 
                    edgecolor='black', linewidth=1.5)
    
    for bar, val in zip(bars1, avg_response):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 5,
                 f'{val:.1f}s',
                 ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax1.set_ylabel('Tempo de Resposta Médio (s)', fontsize=13, fontweight='bold')
    ax1.set_title('Tempo de Resposta - Todas Configurações Azure', fontsize=14, fontweight='bold')
    ax1.set_ylim(0, max(avg_response) + 30)
    ax1.grid(axis='y', alpha=0.3)
    ax1.tick_params(axis='x', rotation=15)
    
    # Subplot 2: Speedup
    bars2 = ax2.bar(configs, speedup, color=colors_bars, alpha=0.8, 
                    edgecolor='black', linewidth=1.5)
    
    for bar, val in zip(bars2, speedup):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.03,
                 f'{val:.2f}×',
                 ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax2.axhline(y=4.0, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Linear (4×)')
    ax2.set_ylabel('Speedup', fontsize=13, fontweight='bold')
    ax2.set_title('Speedup - Todas Configurações Azure', fontsize=14, fontweight='bold')
    ax2.set_ylim(0, 4.5)
    ax2.grid(axis='y', alpha=0.3)
    ax2.tick_params(axis='x', rotation=15)
    
    plt.suptitle('Azure: Worker vs Horizontal Scaling', fontsize=16, fontweight='bold', y=1.02)
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='gray', label='Baseline'),
                      Patch(facecolor='lightblue', label='Worker Scaling'),
                      Patch(facecolor='lightcoral', label='Horizontal Scaling')]
    ax2.legend(handles=legend_elements, loc='upper right', fontsize=10)
    
    plt.suptitle('Azure: Worker vs Horizontal Scaling', fontsize=16, fontweight='bold', y=1.02)
    
    # Rodapé com interpretação
    footer_text = ('Azure: worker scaling e horizontal scaling apresentam desempenho equivalente (1.45× vs 1.50×). '
                   'Plateau em 2 réplicas indica limitação do load balancer. '
                   'Recomendação: preferir worker scaling (menor custo, sem ALB) no Azure.')
    
    plt.figtext(0.5, -0.05, footer_text, ha='center', fontsize=10, 
                style='italic', wrap=True, bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.4))
    
    plt.tight_layout()
    plt.savefig('slide_7_comparacao_azure.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfico 7 salvo: slide_7_comparacao_azure.png")
    plt.close()


# ============================================================================
# GRÁFICO 8: CONSISTÊNCIA - Coeficiente de Variação (CV)
# ============================================================================

def grafico_consistencia():
    """Slide 8: Análise de Consistência - Coeficiente de Variação"""
    
    # Coeficiente de Variação (CV) = (Desvio Padrão / Média) × 100
    configs = ['Baseline', '2 Workers', '4 Workers', '2 Réplicas', '4 Réplicas']
    
    # AWS: [B1, WS1, WS2, HS1, HS2]
    aws_mean = [272.77, 213.83, 161.46, 136.09, 79.72]
    aws_std = [151.69, 119.76, 90.26, 76.99, 43.13]
    aws_cv = [(std/mean)*100 for mean, std in zip(aws_mean, aws_std)]
    
    # Azure: [B2, WS3, WS4, HS3, HS4]
    azure_mean = [231.78, 179.81, 160.23, 153.52, 154.81]
    azure_std = [124.09, 98.01, 84.29, 78.51, 62.88]
    azure_cv = [(std/mean)*100 for mean, std in zip(azure_mean, azure_std)]
    
    x = np.arange(len(configs))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    bars1 = ax.bar(x - width/2, aws_cv, width, label='AWS', 
                   color=COLORS['AWS'], alpha=0.8, edgecolor='black', linewidth=1.5)
    bars2 = ax.bar(x + width/2, azure_cv, width, label='Azure', 
                   color=COLORS['Azure'], alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Adicionar valores nas barras
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{height:.1f}%',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax.set_xlabel('Configuração', fontsize=14, fontweight='bold')
    ax.set_ylabel('Coeficiente de Variação (CV) - %', fontsize=14, fontweight='bold')
    ax.set_title('Análise de Consistência - Coeficiente de Variação\n(Menor é melhor - mais previsível)', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(configs, fontsize=11)
    ax.legend(fontsize=13, loc='upper right')
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim(0, max(max(aws_cv), max(azure_cv)) + 10)
    
    # Linha de referência para CV baixo (30%)
    ax.axhline(y=30, color='green', linestyle='--', linewidth=2, alpha=0.5, 
               label='CV baixo (<30%)')
    
    # Rodapé com interpretação
    footer_text = ('Interpretação: CV < 30% = alta consistência; 30-50% = moderada; > 50% = alta variabilidade\n'
                   'AWS melhora consistência em horizontal scaling (55.6% → 54.1%); '
                   'Azure mantém consistência similar em todas configurações (51.1% → 40.6%)')
    
    plt.figtext(0.5, -0.05, footer_text, ha='center', fontsize=10, 
                style='italic', wrap=True, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    plt.tight_layout()
    plt.savefig('slide_8_consistencia.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfico 8 salvo: slide_8_consistencia.png")
    plt.close()


# ============================================================================
# GRÁFICO 9: CUSTO-BENEFÍCIO - Scatter Plot
# ============================================================================

def grafico_custo_beneficio():
    """Slide 9: Análise de Custo-Benefício - Custo vs Desempenho"""
    
    # Dados: (custo/hora USD, tempo médio resposta s, label, plataforma)
    configs = [
        # AWS
        (0.081, 272.77, 'AWS Baseline (B1)', 'AWS'),
        (0.081, 213.83, 'AWS 2W (WS1)', 'AWS'),
        (0.081, 161.46, 'AWS 4W (WS2)', 'AWS'),
        (0.213, 136.09, 'AWS 2R (HS1)', 'AWS'),
        (0.345, 79.72, 'AWS 4R (HS2)', 'AWS'),
        # Azure
        (0.439, 231.78, 'Azure Baseline (B2)', 'Azure'),
        (0.439, 179.81, 'Azure 2W (WS3)', 'Azure'),
        (0.439, 160.23, 'Azure 4W (WS4)', 'Azure'),
        (0.868, 153.52, 'Azure 2R (HS3)', 'Azure'),
        (1.735, 154.81, 'Azure 4R (HS4)', 'Azure'),
    ]
    
    # Separar por plataforma
    aws_data = [c for c in configs if c[3] == 'AWS']
    azure_data = [c for c in configs if c[3] == 'Azure']
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Plot AWS
    aws_costs = [c[0] for c in aws_data]
    aws_times = [c[1] for c in aws_data]
    aws_labels = [c[2] for c in aws_data]
    
    ax.scatter(aws_costs, aws_times, s=300, c=COLORS['AWS'], 
               alpha=0.7, edgecolors='black', linewidth=2, 
               marker='o', label='AWS', zorder=3)
    
    # Plot Azure
    azure_costs = [c[0] for c in azure_data]
    azure_times = [c[1] for c in azure_data]
    azure_labels = [c[2] for c in azure_data]
    
    ax.scatter(azure_costs, azure_times, s=300, c=COLORS['Azure'], 
               alpha=0.7, edgecolors='black', linewidth=2, 
               marker='s', label='Azure', zorder=3)
    
    # Anotações para cada ponto
    for cost, time, label, platform in configs:
        # Ajustar posição da label para não sobrepor
        offset_x = 0.02 if platform == 'AWS' else -0.02
        offset_y = 5 if platform == 'AWS' else -8
        ha = 'left' if platform == 'AWS' else 'right'
        
        # Simplificar labels
        short_label = label.replace('AWS ', '').replace('Azure ', '')
        
        ax.annotate(short_label, 
                   xy=(cost, time), 
                   xytext=(offset_x, offset_y),
                   textcoords='offset points',
                   ha=ha, va='center',
                   fontsize=9,
                   bbox=dict(boxstyle='round,pad=0.3', 
                            facecolor='white', 
                            edgecolor='gray', 
                            alpha=0.8))
    
    # Destacar AWS HS2 (melhor custo-benefício)
    ax.scatter([0.345], [79.72], s=500, facecolors='none', 
               edgecolors='green', linewidth=3, marker='o', 
               zorder=4, label='Melhor custo-benefício')
    
    # Destacar Azure HS4 (pior custo-benefício)
    ax.scatter([1.735], [154.81], s=500, facecolors='none', 
               edgecolors='red', linewidth=3, marker='s', 
               zorder=4, label='Pior custo-benefício')
    
    # Adicionar linha de tendência ideal (diagonal)
    ax.plot([0, 2], [300, 0], 'g--', alpha=0.3, linewidth=2, 
            label='Direção ideal')
    
    # Área de melhor custo-benefício (sombreada)
    ax.axvspan(0, 0.5, alpha=0.1, color='green', zorder=1)
    ax.axhspan(0, 100, alpha=0.1, color='green', zorder=1)
    ax.text(0.25, 50, 'REGIÃO IDEAL\n(baixo custo + alto desempenho)', 
            ha='center', va='center', fontsize=11, fontweight='bold',
            color='darkgreen', alpha=0.6)
    
    # Configurações do gráfico
    ax.set_xlabel('Custo por Hora (USD)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Tempo de Resposta Médio (s)\n(menor é melhor)', 
                  fontsize=14, fontweight='bold')
    ax.set_title('Análise de Custo-Benefício: Custo × Desempenho\n(Ideal: canto inferior esquerdo)', 
                 fontsize=16, fontweight='bold', pad=20)
    
    # Inverter eixo Y para "menor = melhor" ficar em cima visualmente
    ax.invert_yaxis()
    
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper right', fontsize=11, framealpha=0.9)
    
    # Limites dos eixos
    ax.set_xlim(-0.05, 1.9)
    ax.set_ylim(300, 60)
    
    # Rodapé com interpretação
    footer_text = ('AWS HS2 oferece MELHOR custo-benefício: 94% mais rápido (79.72s vs 154.81s) custando 80% MENOS ($0.345 vs $1.735/hora). '
                   'Azure HS4 é 5.0× mais caro que AWS HS2 com desempenho 94% inferior. '
                   'Configurações AWS (círculos laranja) dominam região de melhor custo-benefício.')
    
    plt.figtext(0.5, -0.05, footer_text, ha='center', fontsize=10, fontweight='bold',
                wrap=True, bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.4))
    
    plt.tight_layout()
    plt.savefig('slide_9_custo_beneficio.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfico 9 salvo: slide_9_custo_beneficio.png")
    plt.close()


# ============================================================================
# EXECUTAR TODOS OS GRÁFICOS
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("GERANDO GRÁFICOS PARA APRESENTAÇÃO TCC")
    print("="*60 + "\n")
    
    grafico_baseline()
    grafico_2_workers()
    grafico_4_workers()
    grafico_2_replicas()
    grafico_4_replicas()
    grafico_comparacao_aws()
    grafico_comparacao_azure()
    grafico_consistencia()
    grafico_custo_beneficio()
    
    print("\n" + "="*60)
    print("✓ TODOS OS 9 GRÁFICOS GERADOS COM SUCESSO!")
    print("="*60)
    print("\nArquivos gerados:")
    print("  • slide_1_baseline.png")
    print("  • slide_2_workers_2.png")
    print("  • slide_3_workers_4.png")
    print("  • slide_4_horizontal_2.png")
    print("  • slide_5_horizontal_4.png (ACHADO PRINCIPAL)")
    print("  • slide_6_comparacao_aws.png")
    print("  • slide_7_comparacao_azure.png")
    print("  • slide_8_consistencia.png")
    print("  • slide_9_custo_beneficio.png (RQ4 - CUSTO-BENEFÍCIO)")
    print("\nPróximos passos:")
    print("  1. Revisar os gráficos gerados")
    print("  2. Inserir nos slides do PowerPoint/Google Slides")
    print("  3. Adicionar 'Fonte: Autoria própria' em cada slide")
    print("="*60 + "\n")
