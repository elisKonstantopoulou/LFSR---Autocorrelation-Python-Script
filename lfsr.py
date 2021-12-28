state = 0b111010 # we give an initial state 
for i in range(63):
  print(state&1, sep='', end='', flush=True)
  newBit = (state ^ (state >> 1)) & 1
  state = (state >> 1) | (newBit << 5)