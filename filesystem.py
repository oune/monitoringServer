import csv
from clock import Time


def getWriterFile(date):
    writerList = []
    fileList = []
    name = filePath + "_" + date + "_" + \
        task.channels.name.replace("/", "_").replace(":", "to") + ".csv"
    fileList.append(open(name, 'a', newline='\n'))
    writerList.append(csv.writer(fileList[-1]))
    print(name, '파일 생성됨')

    return writerList, fileList


def writeOne(csvwriter, data: list, time):
    if type(csvwriter) is list:
        csvwriter = csvwriter[0]

    for raw in data:
        csvwriter.writerow([time, raw])



def writeMultiOne(csvwriter, datas: list, time):
    if type(csvwriter) is list:
        csvwriter = csvwriter[0]

    for i in range(len(datas[0])):
        li = [time]
        li.extend([datas[j][i] for j in range(len(task.channels))])
        csvwriter.writerow(li)


try:
    timer = Time()

    writerList, fileList = getWriterFile(timer.getDate())
    writer = writeMultiOne

    if (timer.isDayChange()):
        writerList, fileList = getWriterFile(timer.getDate())

    now_str = timer.getTime()
    writer(writerList, datas, now_str)

except KeyboardInterrupt:
    for file in fileList:
        file.close()