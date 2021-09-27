import skfuzzy as fuzzy
import skfuzzy.control as ctrl
import numpy as np
import matplotlib.pyplot as plt

# Generate universe variables
outdoorTemp_range = np.arange(-10, 61, 1, np.float32)
indoorTemp_range = np.arange(-10, 35, 1, np.float32)
userInteraction_range = np.arange(0, 61, 1, np.float32)
Lux_range = np.arange(0, 1500, 1, np.float32)
Tv_range = np.arange(0.05, 0.60, 0.01, np.float32)

# Create the three fuzzy variables - two inputs, one output
outdoorTemp_input = ctrl.Antecedent(outdoorTemp_range, 'outdoorTemp_input')
indoorTemp_input = ctrl.Antecedent(indoorTemp_range, 'indoorTemp_input')
userInteraction_input = ctrl.Antecedent(userInteraction_range, 'userInteraction_input')
Lux_input = ctrl.Antecedent(Lux_range, 'Lux_input')
Tv_output = ctrl.Consequent(Tv_range, 'Tv_output')

# Generate fuzzy membership functions
outdoorTemp_input_h = fuzzy.trapmf(outdoorTemp_range, [-10, -10, 12, 18])
outdoorTemp_input_c = fuzzy.trapmf(outdoorTemp_range, [12, 18, 60, 60])

indoorTemp_input_c = fuzzy.trapmf(indoorTemp_range, [-10, -10, 18, 22])
indoorTemp_input_w = fuzzy.trapmf(indoorTemp_range, [18, 22, 24, 26])
indoorTemp_input_h = fuzzy.trapmf(indoorTemp_range, [24, 26, 45, 45])

userInteraction_input_A = fuzzy.trapmf(userInteraction_range, [0, 0, 20, 40])
userInteraction_input_A = fuzzy.trapmf(userInteraction_range, [0, 0, 20, 40])
userInteraction_input_nA = fuzzy.trapmf(userInteraction_range, [20, 40, 60, 60])

Lux_input_d = fuzzy.trapmf(Lux_range, [0, 0, 130, 200])
Lux_input_c = fuzzy.trapmf(Lux_range, [160, 200, 300, 340])
Lux_input_b = fuzzy.trapmf(Lux_range, [300, 400, 1500, 1500])

Tv_output_l = fuzzy.trimf(Tv_range, [0.05, 0.05, 0.15])
Tv_output_ml = fuzzy.trimf(Tv_range, [0.05, 0.15, 0.3])
Tv_output_m = fuzzy.trimf(Tv_range, [0.15, 0.3, 0.45])
Tv_output_mh = fuzzy.trimf(Tv_range, [0.3, 0.45, 0.6])
Tv_output_h = fuzzy.trimf(Tv_range, [0.45, 0.6, 0.6])
Tv_output_nc = fuzzy.trimf(Tv_range, [0.05, 0.05, 0.05])



# Visualize these universes and membership functions

fig, (ax0, ax1, ax2, ax3, ax4) = plt.subplots(nrows=5, figsize=(8, 9))

ax0.plot(userInteraction_range, userInteraction_input_A, 'b', linewidth=1.5, label='Acted')
ax0.plot(userInteraction_range, userInteraction_input_nA, 'g', linewidth=1.5, label='Not Acted')
ax0.set_title('User Interaction with EC Windows')
ax0.legend()

ax1.plot(outdoorTemp_range, outdoorTemp_input_h, 'b', linewidth=1.5, label='Hot')
ax1.plot(outdoorTemp_range, outdoorTemp_input_c, 'g', linewidth=1.5, label='Cold')
ax1.set_title('Outdoor Temperature')
ax1.legend()

ax2.plot(indoorTemp_range, indoorTemp_input_c, 'b', linewidth=1.5, label='Cold')
ax2.plot(indoorTemp_range, indoorTemp_input_w, 'g', linewidth=1.5, label='Warm')
ax2.plot(indoorTemp_range, indoorTemp_input_h, 'r', linewidth=1.5, label='Hot')
ax2.set_title('Indoor Temperature')
ax2.legend()

ax3.plot(Lux_range, Lux_input_d, 'b', linewidth=1.5, label='Dark')
ax3.plot(Lux_range, Lux_input_c, 'g', linewidth=1.5, label='Comfort')
ax3.plot(Lux_range, Lux_input_b, 'r', linewidth=1.5, label='Too-Bright')
ax3.set_title('illuminance')
ax3.legend()

ax4.plot(Tv_range, Tv_output_l, 'b', linewidth=1.5, label='Low')
ax4.plot(Tv_range, Tv_output_ml, 'g', linewidth=1.5, label='Medium Low')
ax4.plot(Tv_range, Tv_output_m, 'r', linewidth=1.5, label='Medium')
ax4.plot(Tv_range, Tv_output_mh, 'm', linewidth=1.5, label='Medium High')
ax4.plot(Tv_range, Tv_output_h, 'k', linewidth=1.5, label='High')
ax4.set_title('EC Windows Visible Light Transmission')
ax4.legend()

# Turn off top/right axes   , ax1, ax2
for ax in (ax0, ax1, ax2, ax3, ax4):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

plt.tight_layout()
plt.show()