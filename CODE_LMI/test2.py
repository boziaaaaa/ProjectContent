import matplotlib.pyplot as plt
eventNum = []
with open("D:/temp_10.24.189.195/EventFlashNumber_L1B_8_ranges_20180807.txt") as f:
    lines = f.readlines()
    for line in lines:
        temp = line.split()
        if len(temp) != 10 or "LMI" not in line:
            continue
        eventNum.append(int(temp[-1]))
print eventNum
plt.plot(eventNum)
plt.show()