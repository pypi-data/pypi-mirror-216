# esoteric-sigdigs

# imports
from math import log10, floor
from decimal import Decimal

# INCLUDES
#   sigdigs(*vals) -> int
#   scientific_to_standard(val:str) -> str
#   round_to_sigdigs(val:float, sig:int) -> str
#   standard_to_scientific(val:float) -> str
#   round_to_sigdigs_and_standard_form_given_source




def sigdigs(*vals) -> int:
  """
  Returns the number of significant digits in a calculation involving all of its arguments as an int
  Arguments fed in must be numerical (ie. ints or floats)
  For example, sigdigs(45.6, 0.5, 1234.56) would return 1, as 0.5 has the least amount of significant digits (1)
  Trailing zeroes are considered significant
  Zeros are considered to have 1 significant digit
  """

  # checks
  try:
    [float(v) for v in vals]
  except ValueError:
    raise ValueError("Values fed into sigdigs() must be numerical")
  
  # get the list of values involved in this operation, ie. the source for the sigdig
  # remove any negative signs or dots, and any scientific notation if python has chosen to use it
  # convert to an integer to remove all leading zeros
  # convert back to a string
  # do this to all values in the list
  # find the shortest value in the list by length
  # get the length of that value
  return len(min([str(int(str(v).replace('.', '').replace('-', '').split('e')[0])) for v in vals], key=len))






def scientific_to_standard(val:str) -> str:
  """
  Removes scientific notation and converts a scientific notation number into normal formatting if possible
  Receives a string (ex. "1.23E1") and returns a string (ex. "12.3")
  May return scientific notation if its input cannot be written in normal formatting without breaking significant digits rules
  """

  # checks
  if type(val) != str:
    raise ValueError("Please ensure scientific values fed into scientific_to_standard() are strings and are formatted correctly")
  
  # edge cases
  if val == '0':
    return '0'
    
  # retrieve values
  raw = val.split('E')
  head = raw[0]
  exp = int(raw[1])
  
  # handle polarity
  polarity = ''
  if head[0] == '-':
    head = head.lstrip('-')
    polarity = '-'
    
  # getting sigdigs
  # sigdigs wired to handle polarity already
  sig = sigdigs(head)
  # multiplying it out
  # decimal handles rounding point errors, all thats left is to round to the correct amount of sigdigs
  raw_combined = str(f"{(Decimal(head) * Decimal('10')**Decimal(exp)):,f}")

  # rounding to sigdigs
  # edge cases
  if exp == 0:
    # head*10^0, essentially just the head
    return polarity + head
  elif exp > (sig-1):
    # sig-1 is the amount of digits in the head sans the initial ones-place
    # cannot do it while preserving sigdigs, just return
    return val
  elif exp == (sig-1):
    # raw_combined is completely correct, by multiplying it by 10^exp, its last sigdig is exactly at the ones place
    # should return xyz, actually returns xyz.0 due to float and decimal conventions, trim the rest out
    # decimal should be constructed in such a way so that 10.99999 is not possible, thus splitting it should be ok
    return polarity + raw_combined.split('.')[0]
  elif exp < (sig-1):
    # more complex part
    # need to move the decimal point either to the left or slightly to the right, but not so far right as to have to create new 0s at the end; ie. its doable
    # print('complex activated') #DEBUG
    undotted_raw_combined = raw_combined.replace('.', '')
    combined = None
    if len(undotted_raw_combined) > sig:
      # due to decimal rounding errors, there are too many zeros after the last sigdig
      # round() takes a parameter for digit to round to, the further right of the dot, the higher
      # this branch of the if tree will always have the dot between two digits or before all digits
      # we want it to round to the sig-th digit after the first non-0, non-dot digit
      # since sig includes values before the dot, too, subtract those from sig to get the amount of digits to the right of the dot to round to
      # however, only do this if the leading value is significant: if it is zero, it does not count as a sigdig
      # however, we want it to round from the first non-0 digit, not just the dot, therefore add the distance between the dot and first non-0 digit, ie. the amount of zeros to the right of the dot and before the head
      digit_left_of_dot = raw_combined.split('.')[0]
      digits_left_of_dot = 0
      # if the leading values before the dot are significant, prepare to subtract them, else if its just a zero, ignore it
      if digit_left_of_dot != '0':
        digits_left_of_dot = len(digit_left_of_dot) # there shouldnt be leading zeros like 0123.45 to mix this up due to prior Decimal treatment, which defaults eliminating them
      from_tenths_onward = raw_combined.lstrip('0').lstrip('.') # strip, but only if there are leading 0s
      raw_combined_head = from_tenths_onward.lstrip('0') # strip any remaining leading 0s to the right of the dot, but left of the first sigdig
      # find their difference
      leading_zeros_after_dot = len(from_tenths_onward) - len(raw_combined_head)
      rounding_point = sig - digits_left_of_dot + leading_zeros_after_dot
      combined = str(round(Decimal(raw_combined), rounding_point))
    elif len(undotted_raw_combined) < sig:
      # not enough digits after the last sig dig, fill them in with zeros
      missing_zeros = '0' * (sig - len(undotted_raw_combined))
      combined = raw_combined + missing_zeros
    elif len(undotted_raw_combined) == sig:
      # already ready
      combined = undotted_raw_combined
    return polarity + combined






def round_to_sigdigs(val:float, sig:int) -> str:
  """
  Rounds a specified value to a specified number of significant digits, returning the answer as a string in scientific notation
  The value fed in must be a float and the number of significant digits fed in must be an int
  """

  # checks
  try:
    float(val)
  except ValueError:
    raise ValueError("Values fed into round_to_sigdigs must be floats")
  if type(sig) != int:
    raise ValueError("Sigdig values fed into round_to_sigdigs() must be ints")
  
  # edge cases
  if sig < 1:
    raise ValueError("Cannot have less than 1 sigdig.")
  if val == 0:
    return '0E0'

  # prepare
  raw = str(val)
  was_new_digit_added = 0

  # handle polarity
  polarity = ''
  if raw[0] == '-':
    raw = raw.lstrip('-')
    polarity = '-'

  # grab the number, starting from the first non-0, non-dot character (negative sign handled already)
  raw_head = raw.replace('.', '').lstrip('0').split('e')[0]
  # round the head off to the correct amount of sigdigs
  head = None
  if len(raw_head) > sig:
    # too many digits from the last sig dig onwards, round away the rest
    # raw_head is currently a number 1234, sig might be 2, thus 2-4 is -2 which works for round()
    # then get it to the point sig, because raw_head is currently an int, and rounding it to a negative point, as sig-len(raw_head) does, will leave those 0 digits behind
    # ex 58928, rounded to 4 sigdigs: sig-len(raw_head) becomes -1, creating 5893*0*
    untrimmed_head = str(round(int(raw_head), sig-len(raw_head)))
    if len(raw_head) != len(untrimmed_head):
      # after rounding, it rounded up and added a new digit
      was_new_digit_added = 1 # so that the exponent can also increase by 1
      head = untrimmed_head[:sig+1]
    else:
      head = untrimmed_head[:sig]
  elif len(raw_head) < sig:
    # not enough digits after the last sig dig, fill them in
    missing_zeros = '0' * (sig - len(raw_head))
    head = raw_head + missing_zeros
  elif len(raw_head) == sig:
    # only insertion of decimal needed now
    head = raw_head

  # put it all together, insert the dot at the second position, as in scientific notation
  scientific_1 = head[:1] + '.' + head[1:]
  # make sure the final head does not include a wayward . at the very end
  if scientific_1[-1] == '.':
    scientific_1 = scientific_1.rstrip('.')
  # get the scientific value exponent of the value
  # this little formula removes polarity, grabs the log10 (if xyz was expressed as x.yz, x.yz multiplied by 10 to the what makes it back to its original, ie the distance the dot is from where it should be), floors it to make sure its the normal exponent, then casts it from a float to an int
  scientific_2 = int(floor(log10(abs(val)))) + was_new_digit_added
  # express in scientific notation, with polarity and return
  # to transform into standard notation, use the scientific_to_standard function; as it stands, scientific notation is a much more general, neat way to express numbers
  return polarity + scientific_1 + 'E' + str(scientific_2)






def standard_to_scientific(val:float) -> str:
  """
  Converts floats into scientific form, outputting strings
  """

  # checks
  try:
    float(val)
  except ValueError:
    raise ValueError("Please ensure standard values fed into scientific_to_standard() are floats or ints")
  
  # simply rely on the fact that round_to_sigdigs returns scientifc form, and just instruct it not to modify sigdigs
  return round_to_sigdigs(val, sigdigs(val))






def round_to_sigdigs_and_standard_form_given_source(val:float, sigsource):
  """
  A common routine
  Rounds a float to the permitted number of significant digits according to a list, sigsource
  sigsource must be a list of floats or ints, and will be used to calculate the amount of permitted significant digits
  The value will then be rounded to this amount of significant digits
  """

  # checks
  try:
    float(val)
  except ValueError:
    raise ValueError("Please ensure values are floats or ints")
  if type(sigsource) != list:
      sigsource = [sigsource]

  # this is a quick and easy funcion, often used
  return scientific_to_standard(round_to_sigdigs(val, sigdigs(*sigsource)))





# DRIVER CODE
if __name__ == "__main__":
  import random
  v = round(random.random() * random.randint(-20, 20), random.randint(-1,3))
  w = random.randint(1,6)

  # v = 1234.5678
  # w = 3
  # v = 0.0056

  print(round_to_sigdigs_and_standard_form_given_source(0.000000000000000000000056, [50]))
  print(round_to_sigdigs_and_standard_form_given_source(50.0 * 0.02345 * 10, [50.0, 0.02345, 10]))

  print('value:', v)
  print('sigdigs:', w)
  print('scientific:', round_to_sigdigs(v, w))
  print('standard:', scientific_to_standard(round_to_sigdigs(v, w)))