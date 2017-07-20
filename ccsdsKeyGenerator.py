#!/usr/bin/env python
# -*- coding: utf-8 -*-


# TAGS CONSTRAINTS:
# unit: a-z A-Z 0-9 / . NOSPACE
# disp: a-z A-Z 0-9 - _ NOSPACE
# form: 0-9 . x - + * / ( ) WITHSPACE, starting {, finishing }
# type: float, double OR hex


# TEST CASES:
"""
//EXPORT_PICSAT_DATA_STRUCTURE_PARSE_START=StructTest
    
    //unsigned short txTrxvuHkCurrent; //[!]SKIP <form>={0.0897*x+89/1.2} <unit>=kg.m2/s /// Tx Telemetry transmitter current [kg.m2/s]

    //unsigned char txTrxvuHkCurrent; //[!]SKIP <unit>=mA <disp>=haha /// Tx Telemetry transmitter current [mA]

    //short txTrxvuHkCurrent; //[!]SKIP <disp>=haha <form>={0.0897*x+89/1.2} ///Tx Telemetry

    //uint8_t txTrxvuHkCurrent; //[!]// <type>=float[!] ///Tx Telemetry transmitter current [mA]

    //uint8_t padding:3; //[!]

    //uint8_t flagStuff:1; //[!] ///flag of some stuff



//EXPORT_PICSAT_DATA_STRUCTURE_PARSE_END
"""


import sys
import os
import re


cwd = os.getcwd()
# ----------------------------------------------------------------
# parameters

cFileNames = [['l0app', 'tools', 'L0AppCommonAcr.hpp'],
               ['l0app', 'tools', 'L0AppCommon.hpp'],
               ['l0app', 'tools', 'L0AppFramLogAndEventReportLib.hpp']]
              
#cFileNames = [['l0app', 'tools', 'L0AppFramLogAndEventReportLib.hpp']]
              
#cFileNames = [['StructTest.hpp']]

START = "EXPORT_PICSAT_DATA_STRUCTURE_PARSE_START"
END = "EXPORT_PICSAT_DATA_STRUCTURE_PARSE_END"
# 'type': (signed, bitSize)
stdType = [['uint8_t', (False, 8)], ['int8_t',   (True, 8)],
           ['uint16_t', (False, 16)], ['int16_t', (True, 16)],
           ['uint32_t', (False, 32)], ['int32_t', (True, 32)],
           ['uint64_t', (False, 64)], ['int64_t', (True, 64)],
           ['unsigned int', (False, 32)], ['int', (True, 32)],
           ['unsigned short', (False, 16)], ['short', (True, 16)],
           ['unsigned char', (False, 8)]]
# have the list from longest to shortest type name
stdType = sorted(stdType, key=lambda x: len(x[0]), reverse=True)

RESULT = ""

#functions
def addit(txt):
    global RESULT
    RESULT += txt

def printf(format, *args):
    sys.stdout.write(format % args)


def camelToSnake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


for cFileName in cFileNames:
    cFile = open(os.path.join(*cFileName), mode='r')
    full_content = cFile.read()
    cFile.close()
    next_struct_index = 0
    # check if structure in file, and for each of them
    while full_content.find(START, next_struct_index) != -1:
        # start bit in the structure
        start = 0
        next_struct_index = full_content.find(START, next_struct_index) + len(START)
        content = full_content[next_struct_index:full_content.find(END, next_struct_index)].splitlines()
        # first line is structure name
        structureName = re.search(".*= *([a-zA-Z_0-9\-]+)", content[0]).group(1)
        printf("structure name: %s\r\n", structureName)
        
        pyFile = open(os.path.join(cwd, structureName.lower() + ".py"), mode='w')

        pyFileFormulae = ''
        
        pyFile.write("#!/usr/bin/env python\n# -*- coding: utf-8 -*-\n\n\n")
        pyFile.write("from ctrl.utils import bincore\nfrom ctrl.utils import b\nfrom ctrl.utils import O\n\n\n")
        addit("{}_KEYS = [\n".format(structureName.upper()))

        # scan and parse each line
        for line in list(content[1:][::-1]):
            if line.find('//[!]') == -1:
                # skip this line
                continue
            line = line.strip('\r\n\t /').replace('//[!]', '')
            # check for type
            for idx, (typeKey, _) in enumerate(stdType):
                if line.startswith(typeKey):
                    dataType = typeKey
                    break
            else:  # no type found
                dataType = '???'

            # remove type, grab name until first ;, and comment afterwards
            fieldName, comment = line.replace(dataType, '').split(';', 1)

            # clean and parse name
            fieldName = fieldName.strip()
            if fieldName.rfind(':') == -1:  # no bitfield
                signed, typeLen = stdType[idx][1]
            else:  # bitfield
                # override number of bits
                temp = fieldName.split(':', 1)
                typeLen, fieldName = int(temp[1]), temp[0]
                dataType = 'bitfield'
                signed = False

            if fieldName.lower() == 'padding':
                printf("fieldName: %s on %d bits\r\n", fieldName, typeLen)
                printf("------------------------------\r\n")
                start += typeLen
                continue

            printf("fieldName: %s\r\n", fieldName)
            printf("dataType: %s\r\n", dataType)

            snake_name = camelToSnake(fieldName)

            printf("typeLen: %d\r\n", typeLen)

            # get comment going
            comment = comment.strip('\r\n\t /')
            
            res = comment.split('///', 1)
            if len(res) == 2:
                commentFields, docString = res
                docString = docString.strip('\r\n\t /')
                printf("docString: %s\r\n", docString)
            else:
                commentFields = res[0]
                docString = ''
                printf("no docString\r\n")
            
            # checks optional disp name
            dispName = re.search("<disp>=([a-zA-Z_0-9\-]+)", commentFields)
            if dispName is None:
                dispName = fieldName
            else:
                dispName = dispName.group(1)
                printf("dispName: %s\r\n", dispName)

            # checks optional unit
            unit = re.search("<unit>=([a-zA-Z0-9\/\.]+)", commentFields)
            if unit is not None:
                unit = unit.group(1)
                printf("unit: %s\r\n", unit)
            
            # checks optional formula
            formula = re.search("<form>=\{([\.x0-9\-\+\*\/ \(\)]+)\}", commentFields)
            if formula is not None:
                formula = formula.group(1)
                printf("formula: %s\r\n", formula)
                #rev_formula = inverse(formula)
                rev_formula = formula
                printf("reverse formula: %s\r\n", rev_formula)
            
            typ = "sint" if signed else "uint"

            # checks optional override of type
            typ = re.search("<type>=([a-zA-Z_0-9\-]+)", commentFields)
            if typ is not None:
                typ = typ.group(1).lower()
                if typ == 'float':
                    typeLen = 32
                elif typ == 'double':
                    typeLen = 64
                elif typ == 'hex':
                    pass
                else:
                    raise Exception("unknown <type>={}".format(typ))
            else:
                typ = 'sint' if signed else 'uint'
            
            #force ovverride of type if bool (length is 1 bit)
            if typeLen == 1:
                typ = 'bool'
            printf("-------------- type: %s\r\n", typ)

            printf("------------------------------\r\n")

            fs = \x20\x20\x20\x20'
            tq = '\x22\x22\x22'
            addit("{fs:}dict(name = '{}',\n".format(snake_name, fs=fs))
            addit("{fs:}{fs:}start = {:d}*b,\n".format(start, fs=fs))
            addit("{fs:}{fs:}l = {:d}*b,\n".format(typeLen, fs=fs))
            addit("{fs:}{fs:}typ = '{}',\n".format(typ, fs=fs))
            if len(docString) == 0:
                addit("{fs:}{fs:}verbose = '[NO DOC STRING]',\n", fs=fs)
            else:
                addit("{fs:}{fs:}verbose = '{}',\n".format(docString, fs=fs))
            if unit is not None:
                addit("{fs:}{fs:}unit = '{}',\n".format(unit, fs=fs))
            if formula is not None:
                formula = formula.replace('x', 'float(x)')
                unramName = 'unram_{}'.format(snake_name).replace(" ", "")
                pyFileFormulae += 'def {}(x, **kwargs):\n{fs:}{tq:}\n{fs:}verbose = {fm}\n{fs:}{tq:}\n{fs:}return {fm}\n\n'\
                                    .format(unramName, fm=formula, fs=fs, tq=tq)
                addit("{fs:}{fs:}fctunram = {},\n".format(unramName, fs=fs))
            addit("{fs:}{fs:}disp = '{}'),\n\n".format(dispName, fs=fs))

            # finally, increase start counter for next round
            start += typeLen
            # end foreach line loop
        addit("]\n\n")
        pyFile.write(pyFileFormulae)
        pyFile.write('\n\n\n')
        pyFile.write(RESULT)
        pyFile.close()
        # end while loop
    # end foreach file loop
