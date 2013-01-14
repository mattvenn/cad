#!/usr/bin/python
import sys
import string
import argparse
import serial

def finish_serial():
  if serial_port:
      serial_port.close()

def setup_serial():
  try:
    serial_port=serial.Serial()
    serial_port.port=args.serialport
    serial_port.timeout=args.timeout
    serial_port.baudrate=args.baud
    serial_port.open()
  except IOError, e:
    print "robot not connected?", e
    exit(1)
  return serial_port

def send_robot_commands(code):
  response = ""
  for line in codes:
    if not line == None:
      #print "-> %s" % line,
      serial_port.write(line)
      response += read_serial_response()
  return response

def read_serial_response():

  response = ""
  all_lines = ""
  while string.find(response,"ok"):
    response = serial_port.readline()
    if response == "":
      print >>sys.stderr, "timeout on serial read"
      finish_serial()
      exit(1)
    if args.verbose:
      print "<- %s" % response,
    all_lines += response
  return all_lines
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="write to arduino")

    parser.add_argument('--command', action='store', dest='command', help="command to send")
    parser.add_argument('--baud',
        action='store', dest='baud', type=int, default='9600',
        help="baud rate")
    parser.add_argument('--serialport',
        action='store', dest='serialport', default='/dev/ttyUSB0',
        help="serial port to listen on")
    parser.add_argument('--verbose',
        action='store_const', const=True, dest='verbose', default=False,
        help="verbose")
    parser.add_argument('--serial-timeout',
        action='store', dest='timeout', type=int, default=1,
        help="timeout on serial read")

    args = parser.parse_args()


    if args.command:
        codes=[args.command+"\n"]

    if not codes:
      print >>sys.stderr, "no codes found"
      exit(1)

    serial_port = setup_serial()

    response = send_robot_commands(codes)
    print response
    finish_serial()

