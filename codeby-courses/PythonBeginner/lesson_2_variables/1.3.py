area_yura = 7*9
area_alex = 3.14*((9/2)** 2)
area_vladimir = 6*3 + 6*8

area_yura_min = area_yura < area_alex < area_vladimir
area_alex_min = area_alex < area_yura < area_vladimir
area_vladimir_min = area_vladimir < area_yura < area_yura

print("Iura's area", area_yura)
print("alex's area", area_alex)
print("vladimir's area", area_vladimir)

print("\nMinimal area is Iura's area", area_yura_min)
