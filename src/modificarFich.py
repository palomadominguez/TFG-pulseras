f = open("/Users/Paloma/MEGA/4ANO/TFG/TFG-codigo-v2/src/testfile.txt","r")
data = f.readlines()

print(data)

limpio = [l.strip() for l in data]
print(limpio)
limpio = [l.replace(" ", "  ") for l in data]
print(limpio)
limpio = [l.split("  ") for l in limpio]

a = []

for l in limpio:
    a += l

print(a)
