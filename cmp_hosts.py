#!/usr/bin/env python

import argparse
import os
import pprint

#
# variable settings
#
myname      = os.path.basename(__file__)

def sort_uniq_list(inlist):
  """ Takes a list and returns a with unique and sorted items """
  outlist = list(set(inlist))
  outlist.sort()
  return outlist

def process_line(inline):
  """ Process a valid /etc/hosts file
        - converts hostnames fields to lowercase
        - sorts the hostnames section and discards duplicates
        - returns ip and nameslist
  """
  inip, innames = inline.split(None, 1)
  innames = innames.lower()
  nameslist = innames.split()
  nameslist = sort_uniq_list(nameslist)
  return inip, nameslist

def read_file(hfile, indups):
  """ Reads an input hosts file
        - discards empty lines and commented out lines
        - strips lines of extra spaces
        - discards comments at end of lines
        - returns a dictionary, {ip: hostname(s)}
        - if a duplicate ip is found and the '-d' option is on, 
          it will display duplicate entries
        - if a duplicate ip is found it will add host name entries
          from duplicate to existing entry
  """
  inlines = {}
  with open(hfile) as infile:
    for line in infile:
      line = line.strip()
      line = line.partition('#')[0]
      line = ' '.join(line.split())
      if not (line.startswith('#') or line == ""):
        inip, innames = process_line(line)
        if inip in inlines:
          if indups:
            print hfile + ': DUP-L1:', inip, inlines[inip]
            print hfile + ': DUP-L2:', inip, innames
          inlines[inip] = inlines[inip] + innames
          inlines[inip] = sort_uniq_list(inlines[inip])
        else:
          inlines[inip] = innames

  return inlines

def get_options():
  parser = argparse.ArgumentParser(description='Compare two hosts files.')
  parser.add_argument('-d', '--duplicates', action="store_true",
         help="Display duplicate IP's")
  parser.add_argument('file1', type=argparse.FileType('r'),
         help='hosts file 1')
  parser.add_argument('file2', type=argparse.FileType('r'),
         help='hosts file 2')

  args = parser.parse_args()

  if args.file1:
    hfile1 = args.file1.name
    args.file1.close()

  if args.file2:
    hfile2 = args.file2.name
    args.file2.close()

  dups = False
  if args.duplicates:
    dups = True

  return hfile1, hfile2, dups

def cpm_files(ind1,ind2):
  """ Compares two /etc/hosts dictionaries created by read_file()
        - sorts input dict 1 by IP
        - checks if IP's in input dict 1 exist in input dict 2 or not
  """
  for inip in sorted(ind1):
    if inip in ind2:
      if cmp(ind1[inip], ind2[inip]) != 0:
        print 'DIF-F1: ', inip, ind1[inip]
        print 'DIF-F2: ', inip, ind2[inip]
    else:
      print 'MIS-F2: ', inip, ind1[inip]
  return

def main():
  hfile1, hfile2, dups = get_options()
  #print hfile1, hfile2

  pp = pprint.PrettyPrinter(indent=2)

  hlines1 = read_file(hfile1, dups)
  #pp.pprint(hlines1)
  #pp.pprint(hlines1['172.22.86.227'])
  #pp.pprint(len(hlines1))

  hlines2 = read_file(hfile2, dups)
  #pp.pprint(hlines2)
  #pp.pprint(hlines2['172.22.86.227'])
  #pp.pprint(len(hlines2))

  cpm_files(hlines1,hlines2)

if __name__ == '__main__':
  try:
    main()
  except(KeyboardInterrupt):
    print ("\n\nCtrl+C pressed! Exiting ....\n")

