import re
import os

# tutorials only

header = ("""/*--------------------------------*- C++ -*----------------------------------*\\
  =========                 |
  \\\      /  F ield         | foam-extend: Open Source CFD
   \\\    /   O peration     | Version:     5.0
    \\\  /    A nd           | Coupled-fe: Porous media simulator
     \\\/     M anipulation  | Version:  alpha
\*---------------------------------------------------------------------------*/""")


yourpaths = ['../tests']

for path in yourpaths:
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            if not name.endswith(('.md', '.py', '.sh')):
                print(os.path.join(root, name))
                foamFile = open(os.path.join(root, name), 'r')
                fullText = foamFile.read()
                foamFile.close()
                body = re.split('---\*/', fullText)
                if len(body) > 1:
                    foamFile = open(os.path.join(root, name), 'w')
                    foamFile.write(header)
                    foamFile.write(body[1])
                    foamFile.close()



