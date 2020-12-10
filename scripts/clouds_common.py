"""
Commonly used code.

"""


# Standardize number of digits for frame number suffix with leading zeros
def suffix_creator(index):
    if index < 10:
        suffix = '0000' + str(index) + '.jpg'
    elif index >=10 and index < 100:
        suffix = '000' + str(index) + '.jpg'
    elif index >= 100 and index < 1000:
        suffix = '00' + str(index) + '.jpg'
    elif index >= 1000 and index < 10000:
        suffix = '0' + str(index) + '.jpg'
    else:
        suffix = str(index) + '.jpg'
    return suffix