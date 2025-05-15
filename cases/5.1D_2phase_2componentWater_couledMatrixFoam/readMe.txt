This case is intended to simulate the injection of a liquid with two components (CO2 and H2O) in a 1D model with the liquid injection velocity of 0.005. It is assumed that the porous medium is initially saturated with gas (alpha gas = 0.2) and the rest of it is alpha rock (0.8). alpha water (liquid) is assumed 0.2 at the inlet (injection).

The expected answer: it is expected that as liquid is injected in the porous medium, alpha.water is increased and alpha.gas is decreased from 0.2. Also, because the components exist in the liquid phase, we expect that the CO2.water and H2O.water also increase in the system, just together with alpha.water.

I have made a similar case where Gas is injected into a liquid (instead of liquid injected into a gas), and this was working fine. But in this case, it gives an error:

--> FOAM FATAL ERROR:
incompatible fields for operation
    [CO2.water] += [alpha.water].