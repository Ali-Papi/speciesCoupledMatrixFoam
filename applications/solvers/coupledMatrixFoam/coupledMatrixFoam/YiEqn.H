{
    forAll(phases, phasei)
    {
         phaseModel& phase = phases[phasei];
         
         const volScalarField& S = phase.S();              // Saturation
         const volScalarField& rho = phase.rho();          // Density
         const surfaceScalarField& phi = fluid.phi();      // Total flux
         const volScalarField& porosity = fluid.porosity();// Porosity
         
         // >>>>>>> I need to declare Yi first!
         // Maybe take it as an input dictionary and declare in createFields?
         //or maybe define it as a class inside the phaseModels (phase.Y). This might need substantial change.
         // Below, we use the first method (take as an input).

         if (phase.name() == "gas")
            {
                fvScalarMatrix YCO2Eqn
                (
                    fvm::ddt(porosity * S * rho, YCO2)
                    + fvm::div(fvc::interpolate(rho) * phi, YCO2)
                    //==
                    // event source terms
                    //- sourceTerm
                    );
                    YCO2Eqn.solve();
                    YH2O = 1 - YCO2;
            }
            else if (phase.name() == "water")
            {
                fvScalarMatrix XCO2Eqn
                (
                    fvm::ddt(porosity * S * rho, XCO2)
                    + fvm::div(fvc::interpolate(rho) * phi, XCO2)
                    //==
                    // event source terms
                    //- sourceTerm
                    );
                    XCO2Eqn.solve();
                    XH2O = 1 - XCO2;
            }

/* forAll(species, i)
{
    volScalarField& Yi = species[i];

    Info << "Solving for species " << Yi.name() << endl;

    fvScalarMatrix YiEqn
    (
        fvm::ddt(porosity * S * rho, Yi)
      + fvm::div(fvc::interpolate(rho) * phi, Yi)
    );

    YiEqn.solve();
}
*/
    }
   
}