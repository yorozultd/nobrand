import requests,sys,time
import time,datetime



class Logger:
 def __init__(self,application_name):
  ts = time.time()
  prefix = "./log/"
  tms = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S')
  self.file_name = prefix+str(application_name)+"_log_"+str(tms)
  self.pointer = open(self.file_name,"w+")
  self.pointer.close()
 def wtmsi(self):
  ts = time.time()
  tms = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
  self.wtil(str(tms))
 def wtil(self,message):
  self.pointer = open(self.file_name,"a")
  self.pointer.write(message+"\n")
  self.pointer.close()
 def wtel(self,message):
  self.pointer = open(self.file_name,"a")
  self.pointer.write("APPLICATION ERROR: "+message+"\n")
  sys.exit(1)
  self.pointer.close()
