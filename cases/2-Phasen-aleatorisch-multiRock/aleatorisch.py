import random

nCells = 1000

rock = range(15, 25, 1)
comp = range(0, 100, 1)
invK = range(100000, 250000, 5000)

### invK
#invKfile0 = open("0/invK.rock", 'r')
#invKlines = invKfile0.readlines()
#invKfile = open("0/invK.rock", 'w')

# alphas
rockfile0 = open("0/alpha.rock", 'r')
co3file0 = open("0/CO3.rock", 'r')
sio3file0 = open("0/SiO3.rock", 'r')
oilfile0 = open("0/alpha.oil", 'r')
rocklines = rockfile0.readlines()
co3lines = co3file0.readlines()
sio3lines = sio3file0.readlines()
oillines = oilfile0.readlines()


rockfile = open("0/alpha.rock", 'w')
sio3file = open("0/SiO3.rock", 'w')
co3file = open("0/CO3.rock", 'w')
oilfile = open("0/alpha.oil", 'w')

"""
for line in invKlines:
    if line.startswith("internalField"):
        invKfile.write("internalField   nonuniform List<diagTensor>\n%s\n(\n" % nCells)
        for i in range(nCells):
            invki = random.choice(invK)
            invKfile.write("(%s %s %s)\n" % (invki, invki, invki))
        invKfile.write(")\n;\n")
    else:
        invKfile.write(line)
"""
for lineR in rocklines:
    if lineR.startswith("internalField"):
        for lineO in oillines:
            if lineO.startswith("internalField"):
                rockfile.write("internalField   nonuniform List<scalar>\n%s\n(\n" % nCells)
                sio3file.write("internalField   nonuniform List<scalar>\n%s\n(\n" % nCells)
                co3file.write("internalField   nonuniform List<scalar>\n%s\n(\n" % nCells)
                oilfile.write("internalField   nonuniform List<scalar>\n%s\n(\n" % nCells)
                for i in range(nCells):
                    poroi = random.choice(rock)/100.
                    compi = random.choice(comp)/100.
                    rockfile.write("%.2f\n" % (1-poroi))
                    sio3file.write("%.2f\n" % ((1-poroi)*compi))
                    co3file.write("%.2f\n" % ((1-poroi)*(1-compi)))
                    oilfile.write("%s\n" % poroi)
                rockfile.write(")\n;\n")
                co3file.write(")\n;\n")
                sio3file.write(")\n;\n")
                oilfile.write(")\n;\n")
            else:
                oilfile.write(lineO)
    else:
        rockfile.write(lineR)
        co3file.write(lineR)
        sio3file.write(lineR)

#invKfile.close()
rockfile.close()
co3file.close()
sio3file.close()
oilfile.close()


