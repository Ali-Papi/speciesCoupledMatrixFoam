    /// >>>> New changes <<<
    Info << nl << "Reading CO2 field XCO2" << endl;
volScalarField XCO2
(
    IOobject
    (
        "XCO2",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);

Info << nl << "Reading CO2 field YCO2" << endl;
volScalarField YCO2
(
    IOobject
    (
        "YCO2",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);


Info << nl << "Reading H2O field XH2O" << endl;
volScalarField XH2O
(
    IOobject
    (
        "XH2O",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
   //dimensionedScalar("",dimless,1)
);
//XH2O=1-XCO2;

Info << nl << "Reading H2O field YH2O" << endl;

volScalarField YH2O
(
    IOobject
    (
        "YH2O",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
    //dimensionedScalar("",dimless,1)
);
//YH2O=1-YCO2;
    /// >>>> New changes ended <<<
    
    uniformDimensionedVectorField g
    (
        IOobject
        (
            "g",
            runTime.constant(),
            mesh,
            IOobject::MUST_READ,
            IOobject::NO_WRITE
        )
    );

    surfaceScalarField gSf(g & mesh.Sf());

    autoPtr<phaseSystem> fluidPtr
    (
        phaseSystem::New(mesh)
    );

    phaseSystem& fluid = fluidPtr();
    phaseSystem::phaseModelList& phases = fluid.phases();

    volScalarField& p = fluid.p();

    mesh.schemesDict().setFluxRequired(p.name());

    volScalarField rho
    (
        IOobject
        (
            "rho",
            runTime.timeName(),
            mesh
        ),
        fluid.rho()
    );

    // Create fields ref
    surfaceScalarField& phi = fluid.phi();
    surfaceScalarField& phip = fluid.phip();
    surfaceScalarField& phig = fluid.phig();

    dictionary blockSolverDict = mesh.solutionDict().subDict("blockSolver");

    label Ai = 0;
    forAll(phases, phasei)
    {
        phaseModel& phase = phases[phasei];

        if (!phase.stationary() && !phase.isReference())
        {
            Ai++;
            phase.blockIndex().append(Ai);
        }
    }
    const label blockSize = ++Ai;

    // set size of phi0s
    fluid.phi0s().setSize(blockSize);

    // Block vector field for pressure (first entry) and phases fractions
    // (others entries).
    autoPtr<blockSystem> pAsBlock(blockSystem::New(blockSize, pAsDict, mesh));

    //- Phase-fraction field table for multivariate discretisation
    multivariateSurfaceInterpolationScheme<scalar>::fieldTable alphaTable;

    // Initialise p in pAs
    pAsBlock->blockAdd(0, p.internalField());

    // Update fields
    // Face volume fractions
    forAll(phases, phasei)
    {
        phaseModel& phase = phases[phasei];
        const volScalarField& alpha = phase;

        phase.alphafRef() = fvc::interpolate(alpha);

        if (phase.stationary() || phase.isReference()) continue;

        alphaTable.add(alpha);

        // Initialise alpha in pAs
        label Ai = phase.blockIndex()[0];
        pAsBlock->blockAdd(Ai, alpha.internalField());
    }

