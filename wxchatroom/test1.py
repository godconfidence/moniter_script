#-*-coding:utf-8-*-

#author: walker
#date: 2016-07-26
#summary: 判断图片的有效性
import io
from PIL import Image

#判断文件是否为有效（完整）的图片
#输入参数为文件路径
def IsValidImage(pathfile):
  bValid = True
  try:
    Image.open(pathfile).verify()
  except Exception as e:
      bValid = False
      print e
  return bValid

#判断文件是否为有效（完整）的图片
#输入参数为bytes，如网络请求返回的二进制数据
def IsValidImage4Bytes(buf):
  bValid = True
  try:
    Image.open(io.BytesIO(buf)).verify()
  except:
    bValid = False

  return bValid

def main():

    print IsValidImage('D:\\Qiniu\\1.jpg')

    pass

if __name__ == '__main__':
    main()
