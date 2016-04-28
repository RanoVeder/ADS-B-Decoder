import pygame

####
(width,height) = (1080,720)




###



def render(screen):
	pygame.display.flip()
def update():
	return


pygame.init()

screen = pygame.display.set_mode((width,height))
pygame.display.flip()
pygame.display.set_caption("Project 1")


PastTime  = pygame.time.get_ticks() 
TickTime = 1000/30.
RenderTime = 1000/60.
second = 1000
FPS = 0
FPScounter = 0
Ticks = 0
Frames = 0

while True:

	for event in pygame.event.get():
		if (event.type == pygame.QUIT):
			print("Exiting")
			exit()

	CurrentTime = pygame.time.get_ticks()
	ElapsedTime = CurrentTime - PastTime

	if (ElapsedTime >= TickTime):
		update()
		Ticks+=1
		TickTime+=1000/30.

	if(ElapsedTime >= RenderTime):
		render(screen,Frames)
		Frames+=1
		FPScounter+=1
		RenderTime+=1000/60.

	if(ElapsedTime >= second):
		print "Frames per Second: ",FPScounter," ## Ticks_Per_Second:",Ticks/30.
		FPS = FPScounter
		second+=1000	
		FPScounter = 0



