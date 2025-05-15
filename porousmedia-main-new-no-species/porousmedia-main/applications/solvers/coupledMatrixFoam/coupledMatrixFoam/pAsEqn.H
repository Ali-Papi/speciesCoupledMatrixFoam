// Correct boundaries
forAll(phases, phasei)
{
    phaseModel& phase = phases[phasei];
    volScalarField& alpha = phase;

    alpha.correctBoundaryConditions();

    if (!phase.stationary())
    {
        phase.URef().correctBoundaryConditions();
    }
}

// Correct fixed-flux BCs to be consistent with the velocity BCs
fluid.correctBoundaryFlux();

word phipScheme("div(phip,alpha)");
word phigScheme("div(phig,alpha)");

fluid.mvConvP
(
    fv::convectionScheme<scalar>::New
    (
        mesh,
        alphaTable,
        phip,
        mesh.schemesDict().divScheme(phipScheme)
    )
);

fluid.mvConvG
(
    fv::convectionScheme<scalar>::New
    (
        mesh,
        alphaTable,
        phig,
        mesh.schemesDict().divScheme(phigScheme)
    )
);

tmp<fv::convectionScheme<scalar>> mvConvG(fluid.mvConvG());

// Update phase system models
fluid.correct();

// Create all matrices for equations and cross-coupling terms
autoPtr<phaseSystem::eqnBlockTable> eqnBlockPtr
(
    new phaseSystem::eqnBlockTable()
);

phaseSystem::eqnBlockTable& eqnBlock = eqnBlockPtr();

eqnBlock.setSize(blockSize);

forAll(eqnBlock, blocki)
{
    eqnBlock.set(blocki, new phaseSystem::eqnTable());

    eqnBlock[blocki].setSize(blockSize);
}

// Total predicted gravity flux
surfaceScalarField phiHbyA
(
    IOobject
    (
        "phiHbyA",
        mesh.time().timeName(),
        mesh
    ),
    mesh,
    dimensionedScalar("zero", dimensionSet(0, 3, -1, 0, 0), 0)
);

surfaceScalarField phigibyAR
(
    IOobject
    (
        "phigibyAR",
        mesh.time().timeName(),
        mesh
    ),
    mesh,
    dimensionedScalar("zero", dimensionSet(0, 3, -1, 0, 0), 0)
);


label refPhaseLabel(-1);
forAll(phases, solvePhasei)
{
    phaseModel& phase = phases[solvePhasei];
    if (phase.isReference())
    {
        refPhaseLabel=solvePhasei;

        const word tauName(IOobject::groupName("alphaTaug", phase.name()));

        surfaceScalarField phigiR(fluid.taus(tauName)*fvc::interpolate(phase.rho())*gSf);
        // gravity phase flux by alpha
        phigibyAR =phigiR
            / max(mvConvG->interpolate(phig, phase), phase.residualAlpha());

        break;
    }
}

// Gravity flux
PtrList<surfaceScalarField> phigsp(phases.size());
{
    forAll(phases, phasei)
    {
        phaseModel& phase = phases[phasei];

        if (phase.stationary()) continue;

        const word tauName(IOobject::groupName("alphaTaug", phase.name()));

        surfaceScalarField phigi((fluid.taus(tauName)*fvc::interpolate(phase.rho()))*gSf-
        mvConvG->interpolate(phig, phase)*phigibyAR);

        if (phase.isReference())
        {
            phigi=mvConvG->interpolate(phig,fluid.alphaVoid())*phigibyAR;
        }

        phigsp.set
        (
            phasei,
            phigi
        );

        forAll(phase.URef().boundaryField(), patchi)
        {
            if (phase.URef().boundaryField()[patchi].fixesValue())
            {
                phigsp[phasei].boundaryField()[patchi] == Zero;
            }
        }
    }
}

// Gravity flux
PtrList<surfaceScalarField> phigs(phases.size());
{
    forAll(phases, phasei)
    {
        phaseModel& phase = phases[phasei];

        if (phase.stationary() || phase.isReference()) continue;

        const word tauName(IOobject::groupName("alphaTaug", phase.name()));

        surfaceScalarField phigi(fluid.taus(tauName)*fvc::interpolate(phase.rho())*gSf);

        phigs.set
        (
            phasei,
            phigi
        );

        forAll(phase.URef().boundaryField(), patchi)
        {
            if (phase.URef().boundaryField()[patchi].fixesValue())
            {
                phigs[phasei].boundaryField()[patchi] == Zero;
            }
        }

        phiHbyA += phigs[phasei];
    }
}

const surfaceScalarField& alphaTaus = fluid.taus("alphaTausp");

// Update the fixedFluxPressure BCs to ensure flux consistency
{
    volScalarField::GeometricBoundaryField& pb = p.boundaryField();

    forAll(pb, patchi)
    {
        if (isA<fluxPressureFvPatchScalarField>(pb[patchi]))
        {
            scalarField phib(pb[patchi].size(), 0);

            forAll(phases, phasei)
            {
                phaseModel& phase = phases[phasei];

                if (phase.stationary()) continue;

                phib +=
                    phase.boundaryField()[patchi]*phase.phi()().boundaryField()[patchi];
            }

            scalarField snGrad
            (
                (phiHbyA.boundaryField()[patchi] - phib)
              / (mesh.magSf().boundaryField()[patchi]*alphaTaus.boundaryField()[patchi])
            );

            refCast<fluxPressureFvPatchScalarField>(pb[patchi]).updateCoeffs(snGrad);
        }
    }
}

// Update snGrad(p) in phaseSystem
fluid.snGradPSf(fvc::snGrad(p)*mesh.magSf());

// Construct the transport part of the pressure equation
eqnBlock[0].set
(
    0,
  - fvm::laplacian(alphaTaus, p)
);

fvScalarMatrix& pEqn = eqnBlock[0][0];

pEqn.setReference(pRefCell, pRefValue);

label Ai = 0;
forAll(phases, solvePhasei)
{
    phaseModel& phase = phases[solvePhasei];

    if (phase.stationary() || phase.isReference()) continue;

    volScalarField& alpha = phase;

    // phase flux by gravity
    surfaceScalarField phigi
    (
        phigs[phase.index()]
        / max(mvConvG->interpolate(phig, alpha), phase.residualAlpha())
    );

    Ai = phase.blockIndex()[0];

    const volScalarField& rhoi = phase.rho()();

    fvScalarMatrix divPhiG
    (
        mvConvG->fvmDiv(phigi, alpha)
        + fvm::Sp(((fvc::ddt(rhoi) + (phase.U() & fvc::grad(rhoi)))/rhoi), alpha)
        - fvc::Sp(fvc::ddt(rhoi)/rhoi, alpha)
    );

    // alpha in alphaEqn [Ai, Ai]
    eqnBlock[Ai].set
    (
        Ai,
        fvm::ddt(alpha)
        + divPhiG
    );

    fvScalarMatrix rhoInp
    (
        (alpha/rhoi)*fvm::ddt(phase.psi(), p)
    );

    // [p, p]
    pEqn += rhoInp;

    // [Ai, p]
    eqnBlock[Ai].set(0, rhoInp);

    // phase flux by gravity
    surfaceScalarField phigip
    (
        phigsp[phase.index()]
        / max(mvConvG->interpolate(phig, alpha), phase.residualAlpha())
    );

    fvScalarMatrix divPhiGp
    (
        mvConvG->fvmDiv(phigip, alpha)
        + fvm::Sp(((fvc::ddt(rhoi) + (phase.U() & fvc::grad(rhoi)))/rhoi), alpha)
        - fvc::Sp(fvc::ddt(rhoi)/rhoi, alpha)
    );

    // alpha in pEqn [p, Ai]
    eqnBlock[0].set(Ai, divPhiGp);

}

if(refPhaseLabel>-1)
{
    eqnBlock[0][Ai] += fvc::div(phigsp[refPhaseLabel]);
    fluid.phi0s()[0] -= phigsp[refPhaseLabel];
}

fluid.addTerms(eqnBlock);

forAll(eqnBlock, varI)
{
    if (!eqnBlock.set(varI)) continue;

    forAll(eqnBlock[varI], varJ)
    {
        if (!eqnBlock[varI].set(varJ)) continue;

        if (varI == varJ)
        {
            pAsBlock->insertEquation(varI, eqnBlock[varI][varJ]);
        }
        else
        {
            pAsBlock->insertEquationCoupling(varI, varJ, eqnBlock[varI][varJ]);
        }
    }
}

