import astrodynamics as ast

# Initialize Porkchop Data (KSP version)

Kerbol = ast.CelestialBody('Kerbol', 1.756567e28, 2.616e8, 432000, None)

Moho = ast.CelestialBody('Moho', 2.5263617e21, 250000, 1210000, ast.Orbit(Kerbol, 5263138304, 0.2, 7.0, 70.0, 15.0, 3.14))

Eve = ast.CelestialBody('Eve', 1.2244127e23, 700000, 80500, ast.Orbit(Kerbol, 9832684544, 0.01, 2.1, 15.0, 0, 3.14), 5, 6514.42)
Gilly = ast.CelestialBody('Gilly', 1.2420512e17, 13000, 28255, ast.Orbit(Eve, 31500000, 0.55, 12.0, 80.0, 10.0, 0.9))

Kerbin = ast.CelestialBody('Kerbin', 5.2915793e22, 600000, 21600, ast.Orbit(Kerbol, 13599840256, 0.0, 0, 0, 0, 3.14), 1, 5066.77)
Mun = ast.CelestialBody('Mun', 9.7600236e20, 200000, 138984.38, ast.Orbit(Kerbin, 12000000, 0.0, 0, 0, 0, 1.7))
Minmus = ast.CelestialBody('Minmus', 2.6457897e19, 60000, 40400, ast.Orbit(Kerbin, 47000000, 0.0, 6.0, 78.0, 38.0, 0.9))

Duna = ast.CelestialBody('Duna', 4.5154812e21, 320000, 65517.859, ast.Orbit(Kerbol, 20726155264, 0.051, 0.06, 135.5, 0, 3.14), 0.2, 3619.12)
Ike = ast.CelestialBody('Ike', 2.7821949e20, 130000, 65517.862, ast.Orbit(Duna, 3200000, 0.03, 0.2, 0, 0, 1.7))

Dres = ast.CelestialBody('Dres', 3.2191322e20, 138000, 34800, ast.Orbit(Kerbol, 40839348203, 0.145, 5.0, 280.0, 90.0, 3.14))

Jool = ast.CelestialBody('Jool', 4.2332635e24, 6000000, 36000, ast.Orbit(Kerbol, 68773560320, 0.05, 1.304, 52.0, 0, 0.1), 15, 14476.48)
Laythe = ast.CelestialBody('Laythe', 2.9397663e22, 500000, 52980.879, ast.Orbit(Jool, 27184000, 0, 0, 0, 0, 3.14), 0.8, 3619.12)
Vall = ast.CelestialBody('Vall', 3.1088028e21, 300000, 105962.09, ast.Orbit(Jool, 43152000, 0, 0, 0, 0, 0.9))
Tylo = ast.CelestialBody('Tylo', 4.2332635e22, 600000, 211926.36, ast.Orbit(Jool, 68500000, 0, 0.025, 0, 0, 3.14))
Bop = ast.CelestialBody('Bop', 3.7261536e19, 65000, 544507.4, ast.Orbit(Jool, 128500000, 0.235, 15.0, 10.0, 25.0, 0.9))
Pol = ast.CelestialBody('Pol', 1.0813636e19, 44000, 901902.62, ast.Orbit(Jool, 179890000, 0.17085, 4.25, 2.0, 15.0, 0.9))

Eeloo = ast.CelestialBody('Eeloo', 1.1149358e21, 210000, 19460, ast.Orbit(Kerbol, 90118820000, 0.26, 6.15, 50.0, 260.0, 3.14))