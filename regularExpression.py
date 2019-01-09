import re

#txt = "123 123 1234"

#x = re.search("\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", txt)

txt = "333-444-1234"

x = re.search("\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", txt)

if (x):
  print("YES! We have a match!")
  print(x)
else:
  print("No match")
