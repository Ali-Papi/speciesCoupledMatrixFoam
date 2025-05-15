/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | foam-extend: Open Source CFD
   \\    /   O peration     | Version:     5.0
    \\  /    A nd           | Web:         http://www.foam-extend.org
     \\/     M anipulation  | For copyright notice see file Copyright
-------------------------------------------------------------------------------
License
    This file is part of foam-extend.

    foam-extend is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or (at your
    option) any later version.

    foam-extend is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with foam-extend.  If not, see <http://www.gnu.org/licenses/>.

\*---------------------------------------------------------------------------*/

#include "PurePhaseModel.H"
#include "phaseSystem.H"

// * * * * * * * * * * * * * * * * Constructors  * * * * * * * * * * * * * * //

template<class BasePhaseModel>
Foam::PurePhaseModel<BasePhaseModel>::PurePhaseModel
(
    const phaseSystem& fluid,
    const word& phaseName,
    const bool referencePhase,
    const label index
)
:
    BasePhaseModel(fluid, phaseName, referencePhase, index),
    psi_
    (
        IOobject
        (
            IOobject::groupName("psi", phaseName),
            fluid.mesh().time().timeName(),
            fluid.mesh()
        ),
        fluid.mesh(),
        dimensionedScalar("zero", dimensionSet(0, -2, 2, 0, 0), fluid.subDict(phaseName).lookup("psi"))
    ),
    rho0_
    (
        IOobject
        (
            IOobject::groupName("rho0", phaseName),
            fluid.mesh().time().timeName(),
            fluid.mesh()
        ),
        fluid.mesh(),
        dimensionedScalar("zero", dimensionSet(1, -3, 0, 0, 0), fluid.subDict(phaseName).lookup("rho0"))
    ),
    rho_
    (
        IOobject
        (
            IOobject::groupName("rho", phaseName),
            fluid.mesh().time().timeName(),
            fluid.mesh()
        ),
        (psi_*fluid.p() + rho0_)
    )
{}


// * * * * * * * * * * * * * * * * Destructor  * * * * * * * * * * * * * * * //

template<class BasePhaseModel>
Foam::PurePhaseModel<BasePhaseModel>::~PurePhaseModel()
{}


// * * * * * * * * * * * * * * * Member Functions  * * * * * * * * * * * * * //

template<class BasePhaseModel>
void Foam::PurePhaseModel<BasePhaseModel>::correct()
{
    // update equation of state
    rho_ = psi_*this->fluid().p() + rho0_;

    BasePhaseModel::correct();
}


template<class BasePhaseModel>
Foam::tmp<Foam::volScalarField>
Foam::PurePhaseModel<BasePhaseModel>::rho() const
{
    return rho_;
}


template<class BasePhaseModel>
Foam::tmp<Foam::volScalarField>
Foam::PurePhaseModel<BasePhaseModel>::psi() const
{
    return psi_;
}

// ************************************************************************* //
