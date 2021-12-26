# LFSR-and-Autocorrelation-Python-Script
This Python script is part of a larger exercise for my Cryptography course in university. In that exercise I used LFSR to generate a pseudorandom binary sequence and used Python to calculate the autocorrelation of that sequence, in order to validate Golomb's third postulate for randomness. In the end of this file you will find the resources I used.

### LFSR Introduction
Linear Feedback Shift Register is a shift register whose input bit is a linear function of its previous state. It lets us go through all possible combinations of zeros and ones given an array of bits, except for a sequence that consists of all zeros (it is later explained).
Let's look at a simple example to understand how LFSR works; let's choose 1001 as our initial state.

The output of our initial, and current, state is 1 (the output is the last bit). Every time we iterate, we will shift all the bits one spot to the right; thus 1001 is going to become (?)100 and we will have to fill the first spot with a linear combination of some bits. We XOR the last two bits of our initial state (0 and 1) and place the result on the empty spot. XOR(0,1)=1 so now we are left with 1100.

Now 1100 is our current state and the output is 0. Let's repeat the previous steps once again. We shift all the bits one position to the right and we are left with (?)110. We XOR the last two bits of the current state and place the result on the empty spot. XOR(0,0)=0 so now we are left with 0110.

We repeat this process until we return to our initial state. In the tables below you will find the XOR gate table (for help) and a table where we calculate all the states.

| __A__ | __B__ | __XOR__ |
| --- | --- | --- |
| 1 | 1 | 0 |
| 1 | 0 | 1 |
| 0 | 1 | 1 |
| 0 | 0 | 0 |

|  |  |  | __Output__ |
| --- | --- | --- | --- |
| 1 | 0 | 0 | 1 | 1 |
| 1 | 1 | 0 | 0 | __0__ |
| 0 | 1 | 1 | 0 | __0__ |
| 1 | 0 | 1 | 1 | __1__ |
| 0 | 1 | 0 | 1 | __1__ |
| 1 | 0 | 1 | 0 | __0__ |
| 1 | 1 | 0 | 1 | __1__ |
| 1 | 1 | 1 | 0 | __0__ |
| 1 | 1 | 1 | 1 | __1__ |
| 0 | 1 | 1 | 1 | __1__ |
| 0 | 0 | 1 | 1 | __1__ |
| 0 | 0 | 0 | 1 | __1__ |
| 1 | 0 | 0 | 0 | __0__ |
| 0 | 1 | 0 | 0 | __0__ |
| 0 | 0 | 1 | 0 | __0__ |
| 1 | 0 | 0 | 1 | __1__ |


The LFSR output is __*001101011110001*__.

We notice that to calculate all the states, the maximum time was needed. To clarify, since we have 4 bits we have 2<sup>4</sup>=16 possible combinations of 0s and 1s, __*except for the 0000 combination*__. The reason for that is because we wouldn't be able to go to the next state, since XOR(0, 0)=0 and we would be stuck in the state 0000 forever.

To conclude this section, given __*n bits*__, the __*maximum period*__ would be __*2<sup>n</sup>-1*__.

There is more than one way to compute an LFSR; it is done by using different __taps__  (points where you chose to perform the XOR). There are mathematical ... that ..., but they will  not be covered here.


### LFSR Code and Random Number Generator
This is a Python script that implements an LFSR, with 1001 as the initial state:
```python
state = 0b1001
for i in range(15):
  print(“{:04b}”.format(state))
  newBit = (state ^ (state >> 1)) & 1
  state = (state >> 1) | (newBit << 3)
```
This script validates the calculations we did in the previous section. We notice that the 15th time the script is running, we return to the initial state.

Now, we will create a pseudorandom number generator by changing only a few things in the above code; instead of printing all the states we will instead keep the last bit of each iteration and print them side by side:
```python
state = 0b1001
for i in range(15):
  print(state&1, sep='', end='', flush=True)
  newBit = (state ^ (state >> 1)) & 1
  state = (state >> 1) | (newBit << 3)
```
It is important to remember that LFSR generates __*pseudorandom*__ numbers.


### Golomb's Postulates 
Let's generate a number from the initial state 111010. We have 2<sup>6</sup>-1=63 possible combinations of 0s and 1s.
Code to calculate the states:
```python
state = 0b111010
for i in range(63):
  print(“{:06b}”.format(state))
  newBit = (state ^ (state >> 1)) & 1
  state = (state >> 1) | (newBit << 5)
```

Code to generate the number:
```python
state = 0b111010
for i in range(63):
  print(state&1, sep='', end='', flush=True)
  newBit = (state ^ (state >> 1)) & 1
  state = (state >> 1) | (newBit << 5)
```
The pseudorandom binary is: 010111111000001000011000101001111010001110010010110111011001101

We will now examine whether Golomb's postulates are true.
__Postulate #1__: the number of 1s and 0s must be equal, or differ at most by 1. This means that if we have an even amount of bits, the number of 1s and 0s must be the same, and if we have an odd number of bits, the number of 1s should differ from the number of 0s by one.
Our binary sequence has 31 0s and 32 1s. Thus, the first postulate is true.

__Postulate #2__: 1/2 of the *runs (consecutive 1s and 0s)* must be of length 1, 1/4 of the runs must be of length 2 and 1/8 of the runs must be of length 3. We calculate 32 runs, of wich:
- 16 runs are of length 1 (16/32=1/2)
- 8 runs are of length 2 (8/32=1/4)
- 4 runs are of length 3 (4/32=1/8)
Thus, the second postulate is true.

__Postulate #3__: for period=1, the autocorrelation must be stable
In order to go forth with the Python script implementtion, we must first understand what autocorrelation and what an autocorrelation function are.

__Autocorrelation:__ given a binary sequence A of length n we get its autocorrelation if we XOR the sequence with itself shifetd i times: 
*Given A=(a<sub>0</sub>, a<sub>1</sub>, ..., a<sub>n-1</sub>), c(i)=XOR(A, A<<<i)*

__Autocorrelation Function:__ it measures the similarity between the sequence and its phase shift by τ. This is its mathematical formula:
...insert picture...


The Python script that calculates the autocorrelatio is the following:
```python
import difflib # library that helps us calculate the difference between two strings

# function that shifts the bits to the right, once, every time it is called
def shift(num_str):
    li = [char for char in num_str]
    first = li[0]
    li = li[1:]
    li.append(first)
    return "".join(li)
# function that calculates the XOR of two binary sequences (in string format) 
def xor(a, b, n):
    ans = ""
    for i in range(n):
        if (a[i] == b[i]):
            ans += "0"
        else:
            ans += "1"
    return ans

# main 
s = "010111111000001000011000101001111010001110010010110111011001101"
length = len(s)

# the following two prints are for aesthetic purposes only, feel free to skip them if you're not interested
print("  τ                               s                                                              s<<<τ                                                      s XOR s<<<τ                                     c(τ)")
print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

# loop to iterate
for i in range(63):
  # the following conditions are for aesthetic purposes only, feel free to skip them if you're not interested
  if (i==0):
    print("  0", s, s, "000000000000000000000000000000000000000000000000000000000000000", "  0.0")
  elif(i<=9):
    xor_result = xor(s, shift(s), length) # calculate XOR
    print(" ", i, s, shift(s), xor_result, " ", difflib.SequenceMatcher(None, s, xor_result).ratio()) # print τ, s, s<<<τ, XOR(s, s<<<τ), similarity between s and XOR
    s = shift(s)
  else:
    xor_result = xor(s, shift(s), length)
    print("", i, s, shift(s), xor_result, " ", difflib.SequenceMatcher(None, s, xor_result).ratio()) # print τ, s, s<<<τ, XOR(s, s<<<τ), similarity between s and XOR
    s = shift(s)
```

The output of the program is the following (part of it):
... insert picture of result...





