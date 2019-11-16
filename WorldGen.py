#Created by M.J.S, published on https://github.com/InternalCode/

import random, os, time
from PIL import Image

class World_gen():
	def __init__(self):
		
		print('\n\nCrude 2d map generator\n\n======================================================\noutput will be saved to text and png file\n\n\n')
		try:
			self.size = int(input('Size of map - suggested 30 - 300: '))
		except ValueError:
			self.size = 100
		try:
			self.dense = int(input('Dispersion - suggested 1 to 10: '))
		except ValueError:
			self.dense = 5
		try:	
			self.rivers = int(input('Number of rivers and ponds chance to generate: '))
		except ValueError:
			self.rivers = 1
		self.sea = input('Sea? Y or N: ')
		self.sea = self.sea.lower()
		if self.sea == 'y':
			self.sea = True
		else:
			self.sea = False
		self.interpolation_method = input('Interpolation method of png image, "1" or "2": ')
		if self.interpolation_method != 1 or self.interpolation_method != 2:
			self.interpolation_method = str(1)
		print('\n======================================================\n\n')
		# auto entries
		# ~ self.size = 200
		# ~ self.dense = 1
		# ~ self.rivers = 1
		# ~ self.sea = 'y'
		# ~ self.interpolation_method = '1'

		self.array = []
		self.sea = True
		self.generate_base()
		self.grow_seeds()
		self.add_river(self.rivers)
		# ~ self.display_array(self.array[:])
		if self.interpolation_method == '1':
			self.array = self.interpolation(self.array[:])
		elif self.interpolation_method == '2':
			self.array = self.interpolation2(self.array[:])

		self.save_array_to_file(self.array)

	def generate_base(self):
		print('Generating seeds...')
		for y in range(self.size):
			self.array.append([])
			for x in range(self.size):
				self.array[y].append(' ')
		#add seeds
		for i in range(self.dense):
			if self.sea == True:
				self.array[self.seed()][self.seed()] = '~'
			self.array[self.seed()][self.seed()] = '#'

	def grow_seeds(self):
		print('Growing seeds...')
		i = 0
		start = time.time()
		con = True
		while con:
			y = self.seed()
			x = self.seed()
			if self.array[y][x] == ' ':
				continue
			elif self.array[y][x] != ' ':
				r = random.randint(0, 100)
				if r <= 25 and r > 5:
					dist = 2
				elif r <= 5:
					dist = 3
				else:
					dist = 1
				try:
					direction = random.randint(0,3)
					if direction is 0:
						self.array[y + dist][x] = self.array[y][x]
					if direction is 1:
						self.array[y][x + dist] = self.array[y][x]
					if direction is 2:
						self.array[y - dist][x] = self.array[y][x]
					if direction is 3:
						self.array[y][x - dist] = self.array[y][x]
				except IndexError:
					pass
				i += 1
				# ~ if i > 100:
					# ~ self.display_array(self.array[:])
					# ~ i = 0
				if i == 10000:
					total = self.size * self.size
					for y in range(self.size):
						for x in range(self.size):
							if self.array[y][x] != ' ':
								total -= 1
								if total == 0:
									con = False
					print('Needed Seeds: ' + str(total), '\r', end = '')
					i = 0

		print('\nGenerated in: ', round(time.time() - start, 1), 's')

	def add_river(self, r):
		print('\nAdding rivers...')
		for i in range(r):
			river = []
			start = []
			start.extend([self.seed(), self.seed()])
			a, b = start
					
			for y in range(self.size):
				river.append([])
				for x in range(self.size):
					river[y].append('.')

			while True:
				direction_x = random.randint(-1,1)
				if direction_x != 0:
					break
			while True:
				direction_y = random.randint(-1,1)
				if direction_y != 0:
					break

			while a > 0 and a < self.size - 1 and b > 0 and b < self.size - 1:
				direction_y = random.randint(-1,1)
				direction_x = random.randint(-1,1)

				random_direction = random.randint(-1,1)
				a = a + direction_x
				b = b + direction_y
				self.array[b][a] = '~'

			# ~ self.display_array(river[:])

	def seed(self):
		return(random.randint(0, (self.size - 1)))


	def display_array(self, array):
		os.system('cls')
		for y in range(self.size):
			print()
			for x in range(self.size):
				print(array[y][x], end = '')
				
	def interpolation(self, array):
		print('Interpolation...')
		array2 = []
		array3 = []
		for y in range(len(array)):
			array2.append([])
			for x in range(len(array[y])):
				array2[y].append(array[y][x])
				array2[y].append(array[y][x])
				array2[y].append(array[y][x])
				array2[y].append('*')
		for y in range(len(array2)):
			array2[y].insert(0, '*')

		for y in range(len(array2)):
			array3.append(array2[y])
			array3.append(array2[y])
			array3.append(array2[y])
			array3.append(['*']*len(array2[y]))
		array3.insert(0, ['*'] * len(array3[y]))
		
		del array2

		return array3[:]

	def interpolation2(self, array):
		print('Interpolation...')
		array2 = []
		array3 = []
		for y in range(len(array)):
			array2.append([])
			for x in range(len(array[y])):
				array2[y].append(array[y][x])
				array2[y].append('*')
		for y in range(len(array2)):
			array2[y].insert(0, '*')

		for y in range(len(array2)):
			array3.append(array2[y])
			array3.append(['*']*len(array2[y]))
		array3.insert(0, ['*'] * len(array3[y]))
		
		del array2

		return array3[:]

	def save_array_to_file(self, array):
		print('\nSaving')

		if os.path.isfile('world.txt') == False:
			with open('world.txt', 'w') as file_obj:
				for y in range(len(array)):
					file_obj.write('\n')
					for x in range(len(array)):
						file_obj.write(array[y][x])
				file_obj.close()
				print('World saved as world.txt')
		elif os.path.isfile('world.txt') == True:
			with open ('world.txt', 'a') as file_obj:
				file_obj.write('\n')
				for y in range(len(array)):
					file_obj.write('\n')
					for x in range(len(array)):
						file_obj.write(array[y][x])
				file_obj.close()
				print('\nNew world added to world.txt')
		
		image_obj = Image.new('RGB', (len(array), len(array)), 'white')
		
		for y in range(len(array)):
			for x in range(len(array)):
				if array[y][x] == '~':
					image_obj.putpixel((x,y), (255,255,255))
				elif array[y][x] == '*':
					image_obj.putpixel((x,y), (255,255,255))
				elif array[y][x] == '#':
					image_obj.putpixel((x,y), (0,0,0))
				if self.interpolation_method == '1':
					try:
						if array[y - 1][x] == '~' and array[y + 1][x] == '~' and array[y][x - 1] == '~' and array[y][x + 1] == '~' and array[y][x] == '~':
							image_obj.putpixel((x,y), (60, 60 ,150))
					except IndexError:
						pass

					try:
						if (array[y][x] == '~' and array[y - 1][x] == '~' and array[y + 1][x] == '~' and array[y][x - 1] == '~' and array[y][x + 1] == '~') and (array[y + 3][x] == '#' or array[y +3][x + 3] == '#' or array[y][x + 3] == '#' or array[y - 3][x + 3] == '#' or array[y - 3][x] == '#' or array[y - 3][x - 3] == '#' or array[y][x - 3] == '#' or array[y + 3][x - 3] == '#'):
							image_obj.putpixel((x,y),(30,110,240))
					except IndexError:
						pass

		image_obj.save('%smap.png' %(str(int(time.time()))))
		image_obj.close()
		print('World saved as png')

if __name__ == '__main__':
	word = World_gen()
