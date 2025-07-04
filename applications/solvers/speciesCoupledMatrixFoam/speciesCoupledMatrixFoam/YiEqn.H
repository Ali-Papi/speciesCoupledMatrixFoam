{
    forAll(phases, phasei)
    {
        phaseModel& phase = phases[phasei];
        
        //const volScalarField& S = phase.S();              // Saturation
        //const volScalarField& rho = phase.rho();          // Density
        //volScalarField rho = phase.rho();          // Density
        const surfaceScalarField& phi = phase.phi();      // Phase flux
        //const surfaceScalarField& alphaf = phase.alphaf();      // Alpha at face
        //const volScalarField& porosity = fluid.porosity();// Porosity
         

        if (phase.name() == "gas")
        {
            fvScalarMatrix YCO2Eqn
            (
                fvm::ddt(YCO2)
                + fvm::div(phi, YCO2)
                //==
                // event source terms
                //- sourceTerm
            );
            YCO2Eqn.solve();
            YH2O = phase - YCO2;

        }
        else if (phase.name() == "water")
        {
            fvScalarMatrix XCO2Eqn
            (
                fvm::ddt(XCO2)
                + fvm::div(phi, XCO2)
                //==
                // event source terms
                //- sourceTerm
            );
            XCO2Eqn.solve();
            //XCO2 = min(max(XCO2, scalar(0)), scalar(1));
            XH2O = phase - XCO2;
            
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
