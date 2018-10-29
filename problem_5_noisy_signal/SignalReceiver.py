import argparse

parser = argparse.ArgumentParser(description='Test number')
parser.add_argument('test_no', metavar='N', type=int, help='Test number.')


class SignalReceiver:
	def __init__(self, test_no):
		assert 1 <= test_no <= 5, "Invalid test number."
		f_real = open('Tests/Test' + str(test_no) + '_real')
		f_noisy = open('Tests/Test' + str(test_no))

		self.__noisy_values = [float(i) for i in f_noisy.readlines()]
		self.__real_values = [float(i) for i in f_real.readlines()]
		self.__c_index = 0
		self.__total_error = 0

	def get_value(self):
		'''
		Gets next noisy value from device. This must be called before push_value.
		:return: (float) device value, None if the device is closed.
		'''
		if self.__c_index >= len(self.__noisy_values):
			return None

		val = self.__noisy_values[self.__c_index]
		self.__c_index = self.__c_index + 1
		return val

	def push_value(self, c_val):
		'''
		Computes the error between the real signal and the corrected value.
		:param c_val: corrected value.
		:return: (float) error value, None if the device is closed.
		'''

		if self.__c_index - 1 >= len(self.__real_values):
			return None

		error = abs(self.__real_values[self.__c_index - 1] - c_val)
		self.__total_error += error
		return error

	def get_error(self):
		return self.__total_error


import numpy as np
from solve import smooth, gaussian_filter, flat_filter
import matplotlib.pyplot as plt
import time

def ff(x, y):
	k = len(y) // 2
	x = np.r_[x[:k][::-1], x, x[-k:][::-1]]
	out = np.zeros((len(x) - 2*k, ))
	for i in range(len(x) - len(y)):
		out[i] = np.sum(x[i:i+len(y)] * y)

	return out

if __name__ == "__main__":
	args = parser.parse_args()
	sr = SignalReceiver(args.test_no)

	# i_val = sr.get_value()
	# while i_val:
	# 	print(sr.push_value(i_val))
	# 	i_val = sr.get_value()
	# print('Total error: ' + str(sr.get_error()))

	bufsize = 1000
	wsize = 31

	buf = np.zeros((bufsize,))
	for i in range(bufsize):
		x = sr.get_value()
		buf[i] = x
		sr.push_value(x)



	s = 0

	while True:
		x = sr.get_value()
		if x is None:
			break

		buf = np.r_[buf[1:], [x]]

		# out = smooth(buf, wsize, window='flat')
		# out = out[wsize//2:]
		# out = out[:-wsize//2+1]``
		# print(out.size, buf.size)

		# out = ff(buf, flat_filter(size=wsize))
		out = np.convolve(buf, flat_filter(size=wsize), mode='same')

		if True and s % 20 == 0:
			plt.plot(out, 'g');
			# plt.plot(buf, 'r');
			plt.grid()
			plt.show()

		# plt.draw()
		# plt.pause(0.0001)
		# plt.clf()
		o = out[-1]
		sr.push_value(o)

		s += 1


	print(sr.get_error())
