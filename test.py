import numpy as np
import matplotlib.pyplot as plt

# Задання вхідної імпульсної відповіді (приклад: дельта-функція)
input_impulse = np.zeros(100)
input_impulse[0] = 1

# Симуляція лінійної системи (приклад: експоненційна функція)
time = np.arange(0, 100)
output_response = np.exp(-0.1 * time)

# Обчислення FFT
fft_input = np.fft.fft(input_impulse)
fft_output = np.fft.fft(output_response)

# Обчислення Частотної Відповіді
frequency_response = fft_output / fft_input

# Зворотне FFT
impulse_response = np.fft.ifft(frequency_response)

# Нормалізація
impulse_response /= np.max(np.abs(impulse_response))

# Виведення результатів
plt.figure(figsize=(10, 6))
plt.subplot(3, 1, 1)
plt.plot(time, input_impulse, label='Input Impulse')
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(time, output_response, label='Output Response')
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(time, np.real(impulse_response), label='Recovered Impulse Response')
plt.legend()

plt.show()
