n = int(input(""))
arr = [int(x) for x in input().split(" ")]

s = sum(arr)
x = 0

if s % 3 == 0:
	d1 = s / 3
	d2 = 2 * d1
	z = t = 0
	for i in range(n-1):
		z += arr[i]
		if z == d2:
			x += t
		if z == d1:
			t += 1
print(x)