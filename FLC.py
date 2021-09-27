import skfuzzy as fuzzy
import skfuzzy.control as ctrl
import numpy as np

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
# h = hot, c = cold, w = warm, A = acted, nA = not acted, d = dark, c = comfort, b = too bright
# l = low, ml = medium low, m = medium, mh = medium high, h = high, nc = no change
outdoorTemp_input['h'] = fuzzy.trapmf(outdoorTemp_range, [-10, -10, 12, 18])
outdoorTemp_input['c'] = fuzzy.trapmf(outdoorTemp_range, [12, 18, 60, 60])

indoorTemp_input['c'] = fuzzy.trapmf(indoorTemp_range, [-10, -10, 18, 22])
indoorTemp_input['w'] = fuzzy.trapmf(indoorTemp_range, [18, 22, 24, 26])
indoorTemp_input['h'] = fuzzy.trapmf(indoorTemp_range, [24, 26, 45, 45])

userInteraction_input['A'] = fuzzy.trapmf(userInteraction_range, [0, 0, 20, 40])
userInteraction_input['nA'] = fuzzy.trapmf(userInteraction_range, [20, 40, 60, 60])

Lux_input['d'] = fuzzy.trapmf(Lux_range, [0, 0, 130, 200])
Lux_input['c'] = fuzzy.trapmf(Lux_range, [160, 200, 300, 340])
Lux_input['b'] = fuzzy.trapmf(Lux_range, [300, 400, 1500, 1500])

Tv_output['l'] = fuzzy.trimf(Tv_range, [0.05, 0.05, 0.15])
Tv_output['ml'] = fuzzy.trimf(Tv_range, [0.05, 0.15, 0.3])
Tv_output['m'] = fuzzy.trimf(Tv_range, [0.15, 0.3, 0.45])
Tv_output['mh'] = fuzzy.trimf(Tv_range, [0.3, 0.45, 0.6])
Tv_output['h'] = fuzzy.trimf(Tv_range, [0.45, 0.6, 0.6])
Tv_output['nc'] = fuzzy.trimf(Tv_range, [0.05, 0.05, 0.05])

# set up the method of defuzzifying
Tv_output.defuzzify_method = 'centroid'

# make the fuzzy rules
rule0 = ctrl.Rule(antecedent=(userInteraction_input['nA'] & outdoorTemp_input['h'] & indoorTemp_input['h'] & Lux_input['b'])|(userInteraction_input['nA'] & outdoorTemp_input['h'] & indoorTemp_input['w'] & Lux_input['b']), consequent=Tv_output['l'], label='rule l')
rule1 = ctrl.Rule(antecedent=(userInteraction_input['nA'] & outdoorTemp_input['c'] & indoorTemp_input['h'] & Lux_input['b'])|(userInteraction_input['nA'] & outdoorTemp_input['c'] & indoorTemp_input['w'] & Lux_input['b'])|(userInteraction_input['nA'] & outdoorTemp_input['h'] & indoorTemp_input['c'] & Lux_input['b']), consequent=Tv_output['ml'], label='rule ml')
rule2 = ctrl.Rule(antecedent=(userInteraction_input['nA'] & outdoorTemp_input['c'] & indoorTemp_input['c'] & Lux_input['b']), consequent=Tv_output['m'], label='rule m')
rule3 = ctrl.Rule(antecedent=(userInteraction_input['nA'] & outdoorTemp_input['h'] & indoorTemp_input['w'] & Lux_input['d'])|(userInteraction_input['nA'] & outdoorTemp_input['h'] & indoorTemp_input['c'] & Lux_input['d'])|(userInteraction_input['nA'] & indoorTemp_input['h'] & Lux_input['d']), consequent=Tv_output['mh'], label='rule mh')
rule4 = ctrl.Rule(antecedent=(userInteraction_input['nA'] & outdoorTemp_input['c'] & indoorTemp_input['c'] & Lux_input['d'])|(userInteraction_input['nA'] & outdoorTemp_input['c'] & indoorTemp_input['w'] & Lux_input['d']), consequent=Tv_output['h'], label='rule h')
rule5 = ctrl.Rule(antecedent=(userInteraction_input['A'])|(userInteraction_input['nA'] & Lux_input['c']), consequent=Tv_output['nc'], label='rule nc')
# initialize the system and operating environment
system = ctrl.ControlSystem(rules=[rule0, rule1, rule2, rule3, rule4, rule5])
sim = ctrl.ControlSystemSimulation(system)

# simulation
x = eval(input('input(userInteraction,outdoorTemp,indoorTemp,Lux):'))
listx = list(x)
sim.input['userInteraction_input'] = listx[0]
sim.input['outdoorTemp_input'] = listx[1]
sim.input['indoorTemp_input'] = listx[2]
sim.input['Lux_input'] = listx[3]
sim.compute()
output_Tv = sim.output['Tv_output']
if output_Tv < 0.06:
    result = "light transmission level unchanged"
else:
    result = output_Tv
print(result)

