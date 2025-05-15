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
         fvScalarMatrix YiEqn
        (
            fvm::ddt(porosity * S * rho, Yi)
          + fvm::div(rho * phi, Yi)
            //==
            // event source terms
            //- sourceTerm
        );
        YiEqn.solve(); // or YiEqn.solve("Yi")?
    }
   
}