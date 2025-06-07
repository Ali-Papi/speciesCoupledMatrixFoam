// Retrieve solution
Ai = 0;
pAsBlock->retrieveSolution(Ai, p.internalField());

p.correctBoundaryConditions();

forAll(phases, solvePhasei)
{
    phaseModel& phase = phases[solvePhasei];
    if (phase.stationary() || phase.isReference()) continue;

    volScalarField& alpha = phase;

    Ai++;

    pAsBlock->retrieveSolution(Ai, alpha.internalField());
    alpha.correctBoundaryConditions();

    phase.alphafRef() = fvc::interpolate(alpha);
}

// Fill referencePhase
if(refPhaseLabel>-1)
{
    phaseModel* referencePhasePtr = &phases[refPhaseLabel];
    volScalarField& referenceAlpha = *referencePhasePtr;

    referenceAlpha = 1;

    forAll(phases, solvePhasei)
    {
        if (!phases[solvePhasei].isReference())
        {
            referenceAlpha -= phases[solvePhasei];
        }
    }
    // referenceAlpha.correctBoundaryConditions();

    referencePhasePtr->alphafRef() = fvc::interpolate(referenceAlpha);
}

// Report the phase fractions and the phase fraction sum
// Calculate the void fraction
volScalarField alphaVoid
(
    IOobject
    (
        "alphaVoid",
        mesh.time().timeName(),
        mesh
    ),
    mesh,
    dimensionedScalar("one", dimless, 1)
);

// Calculate the porosity fraction
volScalarField porosity
(
    IOobject
    (
        "porosity",
        mesh.time().timeName(),
        mesh
    ),
    mesh,
    dimensionedScalar("one", dimless, 1)
);

forAll(fluid.stationaryPhases(), phasei)
{
    phaseModel& phase = fluid.stationaryPhases()[phasei];
    alphaVoid -= phase;
    if (phase.porous())
    {
        porosity -= phase;
    }

    Info<< phase.name() << " fraction, min, max = "
        << phase.weightedAverage(mesh.V()).value()
        << ' ' << min(phase).value()
        << ' ' << max(phase).value()
        << endl;
}

volScalarField sumAlphaMoving
(
    IOobject
    (
        "sumAlphaMoving",
        mesh.time().timeName(),
        mesh
    ),
    mesh,
    dimensionedScalar("zero", dimless, 0)
);

forAll(fluid.movingPhases(), phasei)
{
    phaseModel& phase = fluid.movingPhases()[phasei];
    volScalarField& alpha = phase;

    Info<< phase.name() << " fraction, min, max = "
        << phase.weightedAverage(mesh.V()).value()
        << ' ' << min(phase).value()
        << ' ' << max(phase).value()
        << endl;

    alpha.max(0);
    sumAlphaMoving += alpha;
}

Info<< "Phase-sum volume fraction, min, max = "
    << (sumAlphaMoving + 1 - alphaVoid)()
      .weightedAverage(mesh.V()).value()
    << ' ' << min(sumAlphaMoving + 1 - alphaVoid).value()
    << ' ' << max(sumAlphaMoving + 1 - alphaVoid).value()
    << endl;

// Correct the sum of the phase fractions to avoid drift
forAll(fluid.movingPhases(), movingPhasei)
{
    fluid.movingPhases()[movingPhasei] *= alphaVoid/sumAlphaMoving;
}

// Update alphaVoid
fluid.alphaVoid() = alphaVoid;

// Update porosity
fluid.porosity() = porosity;

// Update Saturations
forAll(phases, phasei)
{
    phaseModel& phase = phases[phasei];

    if (phase.porous()) continue;

    const volScalarField& alphai = phase;
    phase.SRef() = alphai/fluid.porosity();
}

// snGrad(p_rgh)
fluid.snGradPSf(fvc::snGrad(p)*mesh.magSf());

// Correct fluxes and velocities
{
    surfaceScalarField alphaPhis
    (
        IOobject
        (
            "alphaPhis",
            mesh.time().timeName(),
            mesh
        ),
        mesh,
        dimensionedScalar("zero", dimensionSet(0, 3, -1, 0, 0), 0)
    );

    forAll(fluid.movingPhases(), movingPhasei)
    {
        phaseModel& phase = fluid.movingPhases()[movingPhasei];

        if ( phase.isReference()) continue;

        label Ai = phase.blockIndex()[0];

        phase.alphaPhiRef() =
            eqnBlock[Ai][Ai].flux() + eqnBlock[Ai][0].flux() - fluid.phi0s()[Ai];

        phase.alphaRhoPhiRef() =
            fvc::interpolate(phase.rho())*phase.alphaPhi();

        phase.phiRef() =
            phase.alphaPhi()/max(phase.alphaf(), phase.residualAlpha());

        alphaPhis += phase.alphaPhi();
    }

    if(refPhaseLabel>-1)
    {
        surfaceScalarField phiRef(eqnBlock[0][0].flux());

        forAll(fluid.movingPhases(), movingPhasei)
        {
            phaseModel& phase = fluid.movingPhases()[movingPhasei];

            if ( phase.isReference()) continue;
            label Ai = phase.blockIndex()[0];

            phiRef += eqnBlock[0][Ai].flux() - fluid.phi0s()[0];

            phiRef -= phase.alphaPhiRef();
        }

        phaseModel& phaseRef = fluid.movingPhases()[refPhaseLabel];

        phaseRef.alphaPhiRef() = phiRef;

        alphaPhis += phaseRef.alphaPhi();

        phaseRef.alphaRhoPhiRef() =
            fvc::interpolate(phaseRef.rho())*phaseRef.alphaPhi();

        phaseRef.phiRef() =
            phaseRef.alphaPhi()/max(phaseRef.alphaf(), phaseRef.residualAlpha());
    }

    // forAll(fluid.movingPhases(), movingPhasei)
    // {
    //     phaseModel& phase = fluid.movingPhases()[movingPhasei];
    //     Info <<"alphaPhi "<< phase.name() <<endl;
    //     Info <<phase.alphaPhi()<<endl;
    // }

    phip = - alphaTaus*fluid.snGradPSf();
    phig = phiHbyA;
    phi = alphaPhis;

    forAll(fluid.movingPhases(), movingPhasei)
    {
        phaseModel& phase = fluid.movingPhases()[movingPhasei];

        phase.URef() = fvc::reconstruct(phase.alphaPhi())/max(phase, phase.residualAlpha());

        phase.URef().correctBoundaryConditions();
    }

    // Update fields and models if necessary
    fluid.update();
}

// updated densities
rho = fluid.rho();

