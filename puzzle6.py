packet = input("Provide input: ")

for i in range(4, len(packet)):
    marker = packet[i-4:i]
    if len(marker) == len(set(marker)):
        break

print(i)

for i in range(14, len(packet)):
    marker = packet[i-14:i]
    if len(marker) == len(set(marker)):
        break

print(i)
