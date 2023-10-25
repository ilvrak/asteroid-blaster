import pygame

pygame.mixer.init()
sound = pygame.mixer.Sound()

# Задаем частоту дискретизации (число сэмплов в секунду)
sample_rate = 44100

# Задаем длительность звука в секундах
duration = 1

# Задаем частоту звука (число колебаний в секунду)
frequency = 440

# Генерируем звук
samples = []
for i in range(int(duration * sample_rate)):
    # Генерируем сэмпл (значение амплитуды звука на текущем моменте времени)
    sample = 32767 * float(i % frequency) / frequency
    samples.append(sample)

# Преобразуем список сэмплов в байтовую строку
sound_data = pygame.sndarray.make_sound(samples).get_raw()

# Загружаем звук в память
sound.set_buffer(sound_data)

# Воспроизводим звук
sound.play()
