# -------------- DEPRECATED --------------

import numpy as np
import kspPorkchop as pork
import time
import astrodynamics as ast
import matplotlib.pyplot as plt

def date2utKSP(y, d, h, m, s):
    return s + m*60 + h*60*60 + d*60*60*6 + y*9203545

# Plot porkchop (KSP Version)
print('*--------------------------*')
print('|   KSP Porkchop Plotter   |')
print('*--------------------------*\n')

depPlanet = pork.Kerbin
depPlanetName = depPlanet.name
arrPlanet = pork.Duna
arrPlanetName = arrPlanet.name

resolution = 300

yStart = 1
dStart = 1
yEnd = 3
dEnd = 1

# days
fltTimeStart = 151
fltTimeEnd = 453

print('Calculating time ranges...')
t0TRange = time.perf_counter()
UTdepRange = (date2utKSP((yStart)-1,(dStart)-1,0,0,0), date2utKSP((yEnd)-1,(dEnd)-1,0,0,0))
flightTimeRange = (date2utKSP(0,fltTimeStart,0,0,0), date2utKSP(0,fltTimeEnd,0,0,0))

UTdeps = np.linspace(UTdepRange[0], UTdepRange[1], resolution)
fltTimes = np.linspace(flightTimeRange[0], flightTimeRange[1], resolution)
UTarrs = np.zeros((resolution,resolution))
for i in range(resolution):
    UTarrs[i,:] = UTdeps + fltTimes[i]
timeTime = time.perf_counter() - t0TRange
if round(timeTime, 5) == 0:
    print('Completed.')
else:
    print(f'Completed in {timeTime:.5f} seconds.')

# Generate r and v vectors for each ut
print('Generating r and v vectors...')
t0RV = time.perf_counter()
rArrayDep = np.zeros((resolution, 3))
vArrayDep = np.zeros((resolution, 3))
rArrayArr = np.zeros((resolution, 3, resolution))
vArrayArr = np.zeros((resolution, 3, resolution))
for i in range(resolution):
    rArrayDep[i,:] = depPlanet.orbit.posAtTrueAnomaly(depPlanet.orbit.trueAnomalyAt(UTdeps[i]))
    vArrayDep[i,:] = depPlanet.orbit.velocityAtTrueAnomaly(depPlanet.orbit.trueAnomalyAt(UTdeps[i]))
    for j in range(resolution):
        rArrayArr[i,:,j] = arrPlanet.orbit.posAtTrueAnomaly(arrPlanet.orbit.trueAnomalyAt(UTarrs[j,i]))
        vArrayArr[i,:,j] = arrPlanet.orbit.velocityAtTrueAnomaly(arrPlanet.orbit.trueAnomalyAt(UTarrs[j,i]))
rvTime = time.perf_counter() - t0RV
if round(rvTime, 5) == 0:
    print('Completed.')
else:
    print(f'Completed in {rvTime:.5f} seconds.')

# Solve Lambert's problem for each time
print('Computing delta Vs...')
t0Lam = time.perf_counter()
dV = np.zeros((resolution,resolution))
for i in range(resolution):
    for j in range(resolution):
        v1, v2 = ast.LambertSolver(rArrayDep[i,:], rArrayArr[i,:,j], fltTimes[j], depPlanet.orbit.refBody.gravParameter)
        
        # Subtract planet velocity then compute delta V
        vInfDep = np.linalg.norm(v1 - vArrayDep[i,:])
        vInfArr = np.linalg.norm(v2 - vArrayArr[i,:,j])
        dV[j,i] = vInfDep + vInfArr
LambertTime = time.perf_counter() - t0Lam
if round(LambertTime, 5) == 0:
    print('Completed.')
else:
    print(f'Completed in {LambertTime:.5f} seconds.')

# Create figure
fig, ax = plt.subplots()
depStart = (yStart - 1)*426 + (dStart - 1)
depEnd = (yEnd - 1)*426 + (dEnd - 1)
porkPlot = ax.imshow(np.flipud(dV), vmin=np.round(np.min(dV)), vmax=np.round(np.percentile(dV,95)), extent=[depStart, depEnd, fltTimeStart, fltTimeEnd], aspect='auto')
ax.set_xlabel('Departure Date (days from epoch)')
ax.set_xticks(np.round(np.linspace(depStart, depEnd, 5)))
ax.set_ylabel('Time of Flight (days)')
ax.set_yticks(np.round(np.linspace(fltTimeStart, fltTimeEnd, 5)))
ax.set_title(f'{depPlanetName} to {arrPlanetName} Delta V Transfer Plot')
cbarTicks = np.round(np.linspace(np.min(dV), np.percentile(dV,95), 5)).astype(int)
cbar = plt.colorbar(porkPlot, ticks=cbarTicks)
cbar.set_ticklabels(cbarTicks)
cbar.set_label('Delta V (m/s)')
plt.show()