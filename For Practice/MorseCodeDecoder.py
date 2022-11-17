# Decode the Morse code, advanced
# Kata link: https://www.codewars.com/kata/54b72c16cd7f5154e9000457/train/python?

def decode_bits(bits):
    # first we have to determine how long is "one unit"
    # find the shortest sequence of 1, that is a unit
    bits = str(bits)
    counts = []

    # finding the unit
    def find_unit(bits):
        break_count = 0 # counting the time the detecter meets 0
        count = 0
        for num in bits:
            if break_count > 3:
                print(min(counts))
                break
            if num == "1": # counting the length of sequence 1
                count += 1
            if num == "0":
                counts.append(count)
                break_count += 1
    
    # loop to ensure finding the basic unit
    #for i in range(len(bits)):
    find_unit(bits)
    print(min(counts))
    unit_0 = "0" * (min(counts))
    unit_1 = "1" * min(counts)

    return bits.replace( unit_0 * 7,'   ').replace( unit_1 * 3, '-').replace( unit_1 * 1, '.').replace( unit_0 * 3, ' ').replace(unit_0 * 1, '')

def decodeMorse(morse_sequence):
    words = []
    for morse_word in morse_sequence.split('   '):
        word = ''.join(MORSE_CODE.get(morse_char, '') for morse_char in morse_word.split(' '))
        if word:
            words.append(word)
    return ' '.join(words)

# TF is the error message, i just F*ing printed out the min(list) sht

#  STDERR
# Traceback (most recent call last):
#   File "main.py", line 19, in <module>
#     testAndPrint(decodeMorse(decodeBits('1')), 'E')
#   File "/home/codewarrior/solution.py", line 26, in decode_bits
#     unit_0 = "0" * int(min(counts))
# ValueError: min() arg is an empty sequence


print(decode_bits(1100110011001100000011000000111111001100111111001111110000000000000011001111110011111100111111000000110011001111110000001111110011001100000011))