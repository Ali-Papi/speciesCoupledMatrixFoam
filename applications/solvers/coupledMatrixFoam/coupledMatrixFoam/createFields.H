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

