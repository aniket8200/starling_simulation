from pyglet.gl import *
from pyglet.window import key
import math, random, vector
from boid import Boid
import sys


class Model:
	"""This class is model of the display. This contain all the elements displayed on display and updates the location of the boids."""
	def create_boid(self,length, width, height):
		return Boid(position=[random.uniform(-length, length),random.uniform(-width, width),random.uniform(-height-10, 0)],
					velocity=[random.uniform(-25000,25000),random.uniform(-2500,2500),random.uniform(-25000,25000)],
					color=[0,0,0])

	def __init__(self, n):
		"""This constructor makes complete view of the display. It makes all the boids and give them shape."""
		self.batch = pyglet.graphics.Batch()
		self.objs = []
		self.boids = []
		for n in range(int(n)):
			self.boids.append(self.create_boid(200,50,200))

		for boid in self.boids:
			x, y, z = boid.position
			c1, c2, c3 = boid.color
			color = ('c3f', (c1, c2, c3)*3)
			vel = boid.velocity
			# x1, y1, z1, x2, y2, z2, x3, y3, z3 = x/10+0.5,y/10,z/10, x/10-0.5,y/10,z/10, x/10, y/10,z/10-2

			p = vector.bird_orient(boid.fly, boid.velocity, boid.position, [20, 10, 3])



			self.objs.append(self.batch.add(3, GL_TRIANGLES, None, ('v3f', (p[1][0]/30,p[1][1]/30,p[1][2]/30,p[2][0]/30,p[2][1]/30,p[2][2]/30,p[0][0]/30,p[0][1]/30,p[0][2]/30,)), color))
			self.objs.append(self.batch.add(3, GL_TRIANGLES, None, ('v3f', (p[0][0]/30,p[0][1]/30,p[0][2]/30,p[1][0]/30,p[1][1]/30,p[1][2]/30,p[4][0]/30,p[4][1]/30,p[4][2]/30,)), color))
			self.objs.append(self.batch.add(3, GL_TRIANGLES, None, ('v3f', (p[0][0]/30,p[0][1]/30,p[0][2]/30,p[1][0]/30,p[1][1]/30,p[1][2]/30,p[3][0]/30,p[3][1]/30,p[3][2]/30,)), color))			

		# boid = Boid()
		# pos = boid.position
		# x, y, z = 0, 0, -1
		# c1, c2, c3 = boid.color
		# color = ('c3f', (c1, c2, c3)*3)
		# self.faces = []
		# self.faces.append(self.batch.add(3, GL_TRIANGLES, None, ('v3f', (x,y,z, x+1,y,z, x+0.5, y+1,z, )), color))
	def update_boid(self, start, stop):
		for ind in range(start, stop):
			self.boids[ind].update(0.0003, self.boids, [],[])
	def draw(self):
		"""This function is displaying all the elements constructor has made so far. It also changes the location of the boids with time making it look like motion."""
		# for n in range(0, len(self.boids), 100):
		# 	stop = n+100 if n +100 <= len(self.boids) else len(self.boids)
		# 	p = multiprocessing.Process(target = self.update_boid, args = (n, stop))
		# 	p.start()
		force = 0
		ang_mom = 0
		energy = 0
		for boid in self.boids:
			boid.update(0.0003, self.boids, [],[])
		for num in range(len(self.boids)):
			obj = self.objs[num*3]
			obj1 = self.objs[num*3+1]
			obj2 = self.objs[num*3+2]
			boid = self.boids[num]
			force =force + self.boids[num].force
			ang_mom = ang_mom + self.boids[num].ang_mom
			energy = energy + self.boids[num].energy
			
			x, y, z = boid.position
			p = vector.bird_orient(boid.fly, boid.velocity, boid.position, [20, 10, 3])
			boid.fly = -1*boid.fly

			obj.vertices = [p[1][0]/30,p[1][1]/30,p[1][2]/30,p[2][0]/30,p[2][1]/30,p[2][2]/30,p[0][0]/30,p[0][1]/30,p[0][2]/30]
			obj1.vertices = [p[0][0]/30,p[0][1]/30,p[0][2]/30,p[1][0]/30,p[1][1]/30,p[1][2]/30,p[4][0]/30,p[4][1]/30,p[4][2]/30]
			obj2.vertices = [p[0][0]/30,p[0][1]/30,p[0][2]/30,p[1][0]/30,p[1][1]/30,p[1][2]/30,p[3][0]/30,p[3][1]/30,p[3][2]/30]

		print (force/200, ang_mom/200, energy/200)
		self.batch.draw()

class Player:
	"""This is the player of the display. In other view, point of view. It is responsible for interactive working of the display. Player moves or change point of refernce to make it look like translation."""
	def __init__(self):
		self.pos = [0,0,50]
		self.rot = [0,0]

	def mouse_motion(self, dx, dy):
		"""This function map mouse with rotating environment. Whenever we move mouse in its mode, it it move the environment and make it look like player has rotated."""
		dx/=8
		dy/=8
		self.rot[0]+=dy
		self.rot[1]-=dx
		# if self.rot[0]>90 : self.rot[0] = 90
		# if self.rot[0]<-90 : self.rot[0] = -90
		# if self.rot[1]>90 : self.rot[1] = 90
		# if self.rot[1]<-90 : self.rot[1] = -90

	def update(self, dt, keys):
		"""This function use keyboard key to move the player from one place to another."""
		s = dt*10
		rotY = -self.rot[1]/180*math.pi
		dx, dz = math.sin(rotY), math.cos(rotY)
		if keys[key.W]: self.pos[0]+=dx; self.pos[2]-=dz
		if keys[key.S]: self.pos[0]-=dx; self.pos[2]+=dz
		if keys[key.A]: self.pos[0]-=dz; self.pos[2]-=dx
		if keys[key.D]: self.pos[0]+=dz; self.pos[2]+=dx
		if keys[key.SPACE]: self.pos[1]+=s
		if keys[key.LSHIFT]: self.pos[1]-=s

class Window(pyglet.window.Window):
	"""Main display object which organize player and boids in it."""
	def Projection(self): glMatrixMode(GL_PROJECTION); glLoadIdentity()
	def Model(self): glMatrixMode(GL_MODELVIEW); glLoadIdentity()



	def set3d(self):
		self.Projection()
		gluPerspective(50, self.width/self.height, 0.05, 5000)
		self.Model()


	def setLock(self, state): self.lock = state; self.set_exclusive_mouse(state)
	lock = False
	mouse_lock = property(lambda self:self.lock, setLock)

	def on_mouse_motion(self, x, y, dx, dy):
		if self.mouse_lock: self.player.mouse_motion(dx, dy)


	def on_key_press(self, KEY, MOD):
		if (KEY == key.ESCAPE): self.close()
		if KEY == key.E : self.mouse_lock = not self.mouse_lock

	def update(self, dt):
		self.player.update(dt, self.keys)

	def push(self, pos, rot):
		glPushMatrix();
		glRotatef(-rot[0], 1, 0, 0);
		glRotatef(-rot[1], 0, 1, 0);
		glTranslatef(-pos[0], -pos[1], -pos[2])


	
	def __init__(self, *args, **kwargs):
		"""Constructor of the main display. It takes all the necessary arguments and create the display. It adds model and player into display."""
		super().__init__(*args, **kwargs)
		self.set_minimum_size(200, 200)
		self.keys = key.KeyStateHandler()
		self.push_handlers(self.keys)
		pyglet.clock.schedule(self.update)
		# self.boids = []
		# # for n in range(3000):
		# # 	self.boids.append(self.create_boid(5,5,5))
		self.model = Model(sys.argv[1])
		self.player = Player()
	def on_draw(self):
		"""This function determines all the drawing which occurs in the display. It uses Model draw funtion to display all the boids onto the screen."""
		self.set3d()
		self.clear()
		self.push(self.player.pos, self.player.rot)	
		x,y,z = self.player.pos
		# for boid in self.boids:
		# 	boid.update(1, self.boids, [], [])
		# upd = [x.position for x in self.boids]
		self.model.draw()
		glPopMatrix()

def run():
	window = Window( width=1900, height=1000, caption = "Flocking Simulation", resizable=True)
	glClearColor(0.5,0.7,1,1)
	glEnable(GL_DEPTH_TEST)
	# ps = []
	# for x in range

	# pyglet.graphics.draw(50000, pyglet.gl.GL_LINE_LOOP, ('v3f', ps, 'c3f', (0,0,0)*50000) )
	pyglet.app.run()


if __name__ == '__main__':
	window = Window( width=1900, height=1000, caption = "Flocking Simulation", resizable=True)
	glClearColor(0.5,0.7,1,1)
	glEnable(GL_DEPTH_TEST)
	# ps = []
	# for x in range

	# pyglet.graphics.draw(50000, pyglet.gl.GL_LINE_LOOP, ('v3f', ps, 'c3f', (0,0,0)*50000) )
	pyglet.app.run()