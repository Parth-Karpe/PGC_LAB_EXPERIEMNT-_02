import matplotlib.pyplot as plt
import numpy as np
import os

plt.style.use('dark_background')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

threads = np.array([1, 2, 4, 6, 16])
seq_time = 1.845448

pthread_times = np.array([1.812432, 3.604127, 4.572821, 5.266353, 10.175397])
omp_times = np.array([1.828267, 0.940907, 0.483794, 0.356250, 0.209669])

pthread_speedups = seq_time / pthread_times
omp_speedups = seq_time / omp_times
ideal_speedups = threads

pthread_eff = (pthread_speedups / threads) * 100
omp_eff = (omp_speedups / threads) * 100

out_dir = r'c:\Users\parth\Downloads\semhy5\PGC_LAB_EXPERIMENT_02\graphs'
os.makedirs(out_dir, exist_ok=True)

# 1. Execution Time Comparison Plot
fig, ax = plt.subplots(figsize=(10, 6), facecolor='#1e1e2e')
ax.set_facecolor('#181825')
bar_width = 0.35
x = np.arange(len(threads))

rects1 = ax.bar(x - bar_width/2, pthread_times, bar_width, label='Pthreads (Manual Multi-Threading)', color='#f38ba8', edgecolor='#cdd6f4', linewidth=1.2)
rects2 = ax.bar(x + bar_width/2, omp_times, bar_width, label='OpenMP (Work Sharing)', color='#a6e3a1', edgecolor='#cdd6f4', linewidth=1.2)
ax.axhline(y=seq_time, color='#fab387', linestyle='--', linewidth=2, label=f'Sequential Baseline ({seq_time:.2f}s)')

ax.set_xlabel('Number of Threads', fontsize=12, color='#cdd6f4', fontweight='bold', labelpad=10)
ax.set_ylabel('Execution Time (seconds)', fontsize=12, color='#cdd6f4', fontweight='bold', labelpad=10)
ax.set_title('Execution Time vs Number of Threads (Lower is Better)\nWorkload: N = 1,000,000,000 Arithmetic Reductions', fontsize=14, color='#cdd6f4', fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels([f'{t} Threads' for t in threads], color='#cdd6f4', fontsize=10)
ax.tick_params(colors='#cdd6f4')
ax.grid(axis='y', linestyle='--', alpha=0.3, color='#cdd6f4')
ax.legend(facecolor='#1e1e2e', edgecolor='#cdd6f4', fontsize=10)

for rect in rects1:
    h = rect.get_height()
    ax.annotate(f'{h:.2f}s', xy=(rect.get_x() + rect.get_width() / 2, h),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom',
                color='#f38ba8', fontweight='bold', fontsize=9)

for rect in rects2:
    h = rect.get_height()
    ax.annotate(f'{h:.2f}s', xy=(rect.get_x() + rect.get_width() / 2, h),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom',
                color='#a6e3a1', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'execution_time_comparison.png'), dpi=300)
plt.close()

# 2. Speedup Comparison Plot
fig, ax = plt.subplots(figsize=(10, 6), facecolor='#1e1e2e')
ax.set_facecolor('#181825')
ax.plot(threads, ideal_speedups, 'o--', color='#89b4fa', linewidth=2, label='Ideal Linear Speedup ($S_p = p$)')
ax.plot(threads, omp_speedups, 's-', color='#a6e3a1', linewidth=2.5, markersize=8, label=f'OpenMP Scaling (Max {omp_speedups[-1]:.2f}x @ 16T)')
ax.plot(threads, pthread_speedups, '^-', color='#f38ba8', linewidth=2.5, markersize=8, label=f'Pthreads Scaling ({pthread_speedups[-1]:.2f}x @ 16T)')

ax.set_xlabel('Thread Count (p)', fontsize=12, color='#cdd6f4', fontweight='bold', labelpad=10)
ax.set_ylabel('Speedup Factor ($S_p = T_1 / T_p$)', fontsize=12, color='#cdd6f4', fontweight='bold', labelpad=10)
ax.set_title('Speedup Analysis Across Thread Configurations (Higher is Better)\nOpenMP vs Pthreads vs Ideal Scaling', fontsize=14, color='#cdd6f4', fontweight='bold', pad=15)
ax.set_xticks(threads)
ax.set_xticklabels([f'{t}' for t in threads], color='#cdd6f4', fontsize=10)
ax.tick_params(colors='#cdd6f4')
ax.grid(True, linestyle='--', alpha=0.3, color='#cdd6f4')
ax.legend(facecolor='#1e1e2e', edgecolor='#cdd6f4', fontsize=10)

for t, s in zip(threads, omp_speedups):
    ax.annotate(f'{s:.2f}x', xy=(t, s), xytext=(5, 5), textcoords="offset points",
                color='#a6e3a1', fontweight='bold', fontsize=9)

for t, s in zip(threads, pthread_speedups):
    ax.annotate(f'{s:.2f}x', xy=(t, s), xytext=(5, -12), textcoords="offset points",
                color='#f38ba8', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'speedup_comparison.png'), dpi=300)
plt.close()

# 3. Parallel Efficiency Plot
fig, ax = plt.subplots(figsize=(10, 6), facecolor='#1e1e2e')
ax.set_facecolor('#181825')
ax.axhline(y=100, color='#89b4fa', linestyle='--', linewidth=1.5, label='100% Ideal Efficiency')
ax.plot(threads, omp_eff, 's-', color='#a6e3a1', linewidth=2.5, markersize=8, label='OpenMP Parallel Efficiency (%)')
ax.plot(threads, pthread_eff, '^-', color='#f38ba8', linewidth=2.5, markersize=8, label='Pthreads Parallel Efficiency (%)')

ax.set_xlabel('Thread Count (p)', fontsize=12, color='#cdd6f4', fontweight='bold', labelpad=10)
ax.set_ylabel('Parallel Efficiency (%) [$E_p = S_p / p \\times 100$]', fontsize=12, color='#cdd6f4', fontweight='bold', labelpad=10)
ax.set_title('Parallel Efficiency vs Core Count\nOpenMP Thread Pool vs Unsynchronized Pthread Worker Overhead', fontsize=14, color='#cdd6f4', fontweight='bold', pad=15)
ax.set_xticks(threads)
ax.set_xticklabels([f'{t}' for t in threads], color='#cdd6f4', fontsize=10)
ax.set_ylim(0, 115)
ax.tick_params(colors='#cdd6f4')
ax.grid(True, linestyle='--', alpha=0.3, color='#cdd6f4')
ax.legend(facecolor='#1e1e2e', edgecolor='#cdd6f4', fontsize=10)

for t, e in zip(threads, omp_eff):
    ax.annotate(f'{e:.1f}%', xy=(t, e), xytext=(5, 5), textcoords="offset points",
                color='#a6e3a1', fontweight='bold', fontsize=9)

for t, e in zip(threads, pthread_eff):
    ax.annotate(f'{e:.1f}%', xy=(t, e), xytext=(5, 5), textcoords="offset points",
                color='#f38ba8', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'parallel_efficiency.png'), dpi=300)
plt.close()

# 4. Multi-Panel Combined Summary Dashboard
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12), facecolor='#1e1e2e')

# Panel 1: Exec Time
ax1.set_facecolor('#181825')
ax1.plot(threads, pthread_times, '^-', color='#f38ba8', linewidth=2, markersize=6, label='Pthreads')
ax1.plot(threads, omp_times, 's-', color='#a6e3a1', linewidth=2, markersize=6, label='OpenMP')
ax1.axhline(y=seq_time, color='#fab387', linestyle='--', label=f'Sequential ({seq_time:.2f}s)')
ax1.set_title('(A) Execution Time (s) [Lower is Better]', color='#cdd6f4', fontweight='bold', fontsize=12)
ax1.set_xlabel('Threads', color='#cdd6f4')
ax1.set_ylabel('Seconds', color='#cdd6f4')
ax1.grid(True, linestyle='--', alpha=0.3, color='#cdd6f4')
ax1.tick_params(colors='#cdd6f4')
ax1.legend(facecolor='#1e1e2e', edgecolor='#cdd6f4')

# Panel 2: Speedup
ax2.set_facecolor('#181825')
ax2.plot(threads, ideal_speedups, 'o--', color='#89b4fa', label='Ideal')
ax2.plot(threads, omp_speedups, 's-', color='#a6e3a1', linewidth=2, markersize=6, label='OpenMP')
ax2.plot(threads, pthread_speedups, '^-', color='#f38ba8', linewidth=2, markersize=6, label='Pthreads')
ax2.set_title('(B) Speedup Factor ($S_p$) [Higher is Better]', color='#cdd6f4', fontweight='bold', fontsize=12)
ax2.set_xlabel('Threads', color='#cdd6f4')
ax2.set_ylabel('Speedup (X)', color='#cdd6f4')
ax2.grid(True, linestyle='--', alpha=0.3, color='#cdd6f4')
ax2.tick_params(colors='#cdd6f4')
ax2.legend(facecolor='#1e1e2e', edgecolor='#cdd6f4')

# Panel 3: Efficiency
ax3.set_facecolor('#181825')
ax3.plot(threads, omp_eff, 's-', color='#a6e3a1', linewidth=2, markersize=6, label='OpenMP')
ax3.plot(threads, pthread_eff, '^-', color='#f38ba8', linewidth=2, markersize=6, label='Pthreads')
ax3.axhline(y=100, color='#89b4fa', linestyle='--', label='100% Ideal')
ax3.set_title('(C) Parallel Efficiency ($E_p$ %)', color='#cdd6f4', fontweight='bold', fontsize=12)
ax3.set_xlabel('Threads', color='#cdd6f4')
ax3.set_ylabel('Efficiency (%)', color='#cdd6f4')
ax3.grid(True, linestyle='--', alpha=0.3, color='#cdd6f4')
ax3.tick_params(colors='#cdd6f4')
ax3.legend(facecolor='#1e1e2e', edgecolor='#cdd6f4')

# Panel 4: Synchronization Comparison (Race vs Mutex/Critical)
ax4.set_facecolor('#181825')
categories = ['Pthreads\nUnprotected\n(race.c)', 'Pthreads\nMutex\n(mutex.c)', 'OpenMP\nUnprotected\n(omp_race.c)', 'OpenMP\nCritical\n(omp_critical.c)']
actual_counts = [150011, 400000, 100112, 400000]
bar_c = ['#f38ba8', '#a6e3a1', '#f38ba8', '#a6e3a1']

bars = ax4.bar(categories, actual_counts, color=bar_c, edgecolor='#cdd6f4', linewidth=1.2, width=0.5)
ax4.axhline(y=400000, color='#fab387', linestyle='--', label='Target (400,000)')
ax4.set_title('(D) Race Condition vs Synchronization Verification', color='#cdd6f4', fontweight='bold', fontsize=12)
ax4.set_ylabel('Counter Value', color='#cdd6f4')
ax4.grid(axis='y', linestyle='--', alpha=0.3, color='#cdd6f4')
ax4.tick_params(colors='#cdd6f4')
ax4.set_ylim(0, 480000)
for bar in bars:
    y = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2.0, y + 10000, f'{y:,}', ha='center', va='bottom', color='#cdd6f4', fontweight='bold', fontsize=9)
ax4.legend(facecolor='#1e1e2e', edgecolor='#cdd6f4')

plt.suptitle('PGC Experiment 02: Multithreaded Pthreads & OpenMP Comprehensive Dashboard', color='#cdd6f4', fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(os.path.join(out_dir, 'scaling_summary_chart.png'), dpi=300)
plt.close()

# Also copy the script into graphs directory
with open(__file__, 'r', encoding='utf-8') as f:
    script_content = f.read()
with open(os.path.join(out_dir, 'generate_plots.py'), 'w', encoding='utf-8') as f:
    f.write(script_content)

print('All 4 graphs generated and generate_plots.py saved in graphs/ successfully!')
