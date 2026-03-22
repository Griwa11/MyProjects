import platform as pl
import speedtest

print('Тип системы: ' + pl.platform(),
      'Установленный процессор ' + pl.processor(),
      'Текущая версия компилятора ' + pl.python_compiler(),
      'Текущая версия python ' + pl.python_version(),
      sep='\n')

s = speedtest.Speedtest()
m_bite_rate = 8388608
print('\nСкорость загрузки:', s.download(threads=1) / m_bite_rate,
      '\nСкорость отдачи:', s.upload(threads=1) / m_bite_rate)
