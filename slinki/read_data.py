import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams.update({
    "text.usetex": False,
    "font.family": "STIXGeneral",
    "mathtext.fontset": "stix",
    "axes.unicode_minus": False,
})

t_A, x_A, y_A = np.loadtxt('mass_a.txt', unpack=True)
t_B, x_B, y_B = np.loadtxt('mass_b.txt', unpack=True)

sort_idx_A = np.argsort(t_A)
t_A = t_A[sort_idx_A]
x_A = x_A[sort_idx_A]
y_A = y_A[sort_idx_A]

sort_idx_B = np.argsort(t_B)
t_B = t_B[sort_idx_B]
x_B = x_B[sort_idx_B]
y_B = y_B[sort_idx_B]

mask_A = t_A <= 4.1
mask_B = t_B <= 4.1
t_A = t_A[mask_A]
x_A = x_A[mask_A]
y_A = y_A[mask_A]
t_B = t_B[mask_B]
x_B = x_B[mask_B]
y_B = y_B[mask_B]

v_A = np.gradient(x_A, t_A)
v_B = np.gradient(x_B, t_B)

a_A = np.gradient(v_A, t_A)
a_B = np.gradient(v_B, t_B)

color_A = '#00d4ff'
color_B = '#ff6b35'

def style_plot(ax, title, xlabel, ylabel):
    ax.set_facecolor('#0a0a0a')
    ax.set_title(title, fontsize=42, color='white', weight='bold', pad=20)
    ax.set_xlabel(xlabel, fontsize=36, color='white', weight='bold')
    ax.set_ylabel(ylabel, fontsize=36, color='white', weight='bold')
    ax.tick_params(axis='both', which='major', labelsize=28, colors='white', width=3, length=10)
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.spines['left'].set_color('white')
    for spine in ax.spines.values():
        spine.set_linewidth(3)
    ax.grid(True, color='#333333', linestyle='--', linewidth=2, alpha=0.5)

fig = plt.figure(figsize=(32, 18), facecolor='#0a0a0a')
gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.3)

ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(t_A, x_A, '-', color=color_A, linewidth=4, label='$A: x(t)$', alpha=0.9)
ax1.plot(t_B, x_B, '-', color=color_B, linewidth=4, label='$B: x(t)$', alpha=0.9)
style_plot(ax1, 'Position vs Time', 'Time $t$ (s)', 'Position $x$')
legend1 = ax1.legend(fontsize=32, loc='best', facecolor='black', edgecolor='white', framealpha=0.8)
plt.setp(legend1.get_texts(), color='white')

ax2 = fig.add_subplot(gs[0, 1])
ax2.plot(t_A, v_A, '-', color=color_A, linewidth=4, label='$A: v_x(t)$', alpha=0.9)
ax2.plot(t_B, v_B, '-', color=color_B, linewidth=4, label='$B: v_x(t)$', alpha=0.9)
style_plot(ax2, 'Instantaneous Velocity vs Time', 'Time $t$ (s)', 'Velocity $v_x$')
legend2 = ax2.legend(fontsize=32, loc='best', facecolor='black', edgecolor='white', framealpha=0.8)
plt.setp(legend2.get_texts(), color='white')

ax3 = fig.add_subplot(gs[1, :])
ax3.plot(t_A, a_A, '-', color=color_A, linewidth=4, label='$A: a_x(t)$', alpha=0.9)
ax3.plot(t_B, a_B, '-', color=color_B, linewidth=4, label='$B: a_x(t)$', alpha=0.9)
style_plot(ax3, 'Instantaneous Acceleration vs Time', 'Time $t$ (s)', 'Acceleration $a_x$')
legend3 = ax3.legend(fontsize=32, loc='best', facecolor='black', edgecolor='white', framealpha=0.8)
plt.setp(legend3.get_texts(), color='white')

plt.tight_layout()
plt.savefig('experimental_data.png', dpi=150, facecolor='#0a0a0a', bbox_inches='tight', edgecolor='none')
plt.close()
