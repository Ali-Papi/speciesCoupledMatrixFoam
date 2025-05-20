{
    forAll(phases, phasei)
    {
        phaseModel& phase = phases[phasei];
        
        const volScalarField& S = phase.S();              // Saturation
        const volScalarField& rho = phase.rho();          // Density
        const surfaceScalarField& phi = phase.phi();      // Phase flux
        const surfaceScalarField& alphaf = phase.alphaf();      // Alpha at face
        const volScalarField& porosity = fluid.porosity();// Porosity
        Info << "phi " << phase.phi() << endl;
         
        // >>>>>>> I need to declare Yi first!
        // Maybe take it as an input dictionary and declare in createFields?
        //or maybe define it as a class inside the phaseModels (phase.Y). This might need substantial change.
        // Below, we use the first method (take as an input).
        if (phase.name() == "gas")
        {
            fvScalarMatrix YCO2Eqn
            (
                fvm::ddt(porosity * S * rho, YCO2)
                + fvm::div(fvc::interpolate(rho) * alphaf * phi, YCO2)
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
                + fvm::div(fvc::interpolate(rho) * alphaf * phi, XCO2)
                //==
                // event source terms
                //- sourceTerm
            );
            XCO2Eqn.solve();
            XH2O = 1 - XCO2;
        }
    }
}