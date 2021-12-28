import difflib

#function that shifts the characters of a given string
def shift(num_str):
    li = [char for char in num_str]
    first = li[0]
    li = li[1:]
    li.append(first)
    return "".join(li)

#function that calculates the XOR of two binary numbers (given as strings)
def xor(a, b, n):
    ans = ""
    for i in range(n):
        if (a[i] == b[i]):
            ans += "0"
        else:
            ans += "1"
    return ans

s = "010111111000001000011000101001111010001110010010110111011001101" # the resultt of the lfsr script
length = len(s)

# the following prints serve aesthetic purposes (feel free to skip them if you don't need them)
print("  ô                               s                                                              s<<<ô                                                      s XOR s<<<ô                                     c(ô)")
print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
for i in range(63):
# the following if statements serve aesthetic purposes (feel free to skip them if you don't need them)
  if (i==0):
    print("  0", s, s, "000000000000000000000000000000000000000000000000000000000000000", "  0.0")
  elif(i<=9):
    xor_result = xor(s, shift(s), length)
    print(" ", i, s, shift(s), xor_result, " ", difflib.SequenceMatcher(None, s, xor_result).ratio())
    s = shift(s)
  else:
    xor_result = xor(s, shift(s), length)
    print("", i, s, shift(s), xor_result, " ", difflib.SequenceMatcher(None, s, xor_result).ratio())
    s = shift(s)