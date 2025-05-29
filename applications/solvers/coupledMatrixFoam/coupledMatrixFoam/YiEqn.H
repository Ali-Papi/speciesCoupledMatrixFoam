{
    forAll(phases, phasei)
    {
        phaseModel& phase = phases[phasei];
        
        const volScalarField& S = phase.S();              // Saturation
        //const volScalarField& rho = phase.rho();          // Density
        //volScalarField rho = phase.rho();          // Density
        const surfaceScalarField& phi = phase.phi();      // Phase flux
        const surfaceScalarField& alphaf = phase.alphaf();      // Alpha at face
        const volScalarField& porosity = fluid.porosity();// Porosity
         
        // >>>>>>> I need to declare Yi first!
        // Maybe take it as an input dictionary and declare in createFields?
        //or maybe define it as a class inside the phaseModels (phase.Y). This might need substantial change.
        // Below, we use the first method (take as an input).

        if (phase.name() == "gas")
        {
            //continue;
            //fvScalarMatrix YCO2Eqn
            //(
            //    fvm::ddt(porosity * S * rho, YCO2)
            //    + fvm::div(fvc::interpolate(rho) * alphaf * phi, YCO2)
                //==
                // event source terms
                //- sourceTerm
            //);
            //YCO2Eqn.solve();
            //YH2O = 1 - YCO2;

        }
        else if (phase.name() == "water")
        {
            fvScalarMatrix XCO2Eqn
            (
                porosity * fvm::ddt(S, XCO2)
                + fvm::div(alphaf * phi, XCO2)
                //==
                // event source terms
                //- sourceTerm
            );
            XCO2Eqn.solve();
            //XCO2 = min(max(XCO2, scalar(0)), scalar(1));
            XH2O = 1 - XCO2;
            
            //fvScalarMatrix XH2OEqn
            //(
            //    porosity * fvm::ddt(S, XH2O)
            //    + fvm::div(alphaf * phi, XH2O)
                //==
                // event source terms
                //- sourceTerm
            //);
            //XH2OEqn.solve();
            //XH2O = min(max(XH2O, scalar(0)), scalar(1));
            //XCO2 = 1 - XH2O;
        }
    }
}