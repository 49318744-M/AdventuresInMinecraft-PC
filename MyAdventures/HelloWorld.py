#Programa que realiza instrucciones basicas

import mcpi.minecraft as minecraft
mc = minecraft.Minecraft.create()
mc.postToChat("Hello world")

# printar posicion del jugador en el shell
pos = mc.player.getTilePos()
print(f"Tu posición es: x={pos.x}, y={pos.y}, z={pos.z}")

# colocar un bloque 2 posiciones delante del jugador
mc.setBlock(pos.x, pos.y, pos.z - 2 , 1)

# Crea un cubo de tierra (ID 3) de 3x3x3 en la posición del jugador
for x in range(3):
    for y in range(3):
        for z in range(3):
            mc.setBlock(pos.x + x, pos.y + y, pos.z + z, 3)

# Crea una torre de bloques de oro bajo el jugador
for i in range(10):  # Altura de 10 bloques
    mc.setBlock(pos.x, pos.y + i, pos.z, 41)  # 41 es el ID de oro

#detectar clicks del jugador
events = mc.events.pollBlockHits()
for event in events:
    print(f"¡Has golpeado un bloque en x={event.pos.x}, y={event.pos.y}, z={event.pos.z}!")

