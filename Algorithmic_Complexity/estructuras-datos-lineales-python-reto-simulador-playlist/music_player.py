from random import randint
from node_based_queue import Queue
from time import sleep

class Track:
    def __init__(self, title=None): #Metodo constructor
        self.title = title
        self.length = randint(5, 6) #duracion de la cancion

class MediaPlayerQueue(Queue): #Va a heredar de la clase nodos
    def __init__(self):
        super(MediaPlayerQueue, self).__init__()

    def add_track(self, track): #Metodo para agregar una cancion
        self.enqueue(track) 

    def play(self): #Metodo para reproducir las canciones
        print(f"count: {self.count}") #cuantas cnaciones hay
        while self.count > 0 and self.head is not None: #como estamos usando nodos, que son las canciones, el nodo actual sera el head
            current_track_node = self.dequeue()
            print(f"Now playing {current_track_node.data.title}.")

            sleep(current_track_node.data.length) #Simulamos el tiempo que dura la cancion


track1 = Track("white whistle")
track2 = Track("t/shirt")
track3 = Track("friends")
track4 = Track("to born to die")
track5 = Track("Don't let me down")

print(track1.length)
print(track2.length)
print(track3.length) #Imprimimos la duracion de las canciones

media_player = MediaPlayerQueue()

media_player.add_track(track1)
media_player.add_track(track2)
media_player.add_track(track3)
media_player.add_track(track4)
media_player.add_track(track5)
media_player.play()