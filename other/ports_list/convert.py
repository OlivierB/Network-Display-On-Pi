#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

MAX=999999

# SOURCE : https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.txt


def main():
    f = open("ports.txt", "r")
    tcp = open("list_tcp.py", "w")
    udp = open("list_udp.py", "w")
    sctp = open("list_sctp.py", "w")
    dccp = open("list_dccp.py", "w")
    res = open("res.txt", "w")
    res.write("Double entry ports (delete them in list files):\n")
    with f:
        var = "#!/usr/bin/env python\n# -*- coding: utf-8 -*-\n"
        tcp.write(var+"dListTCP = {\n")
        udp.write(var+"dListUDP = {\n")
        sctp.write(var+"dListSCTP = {\n")
        dccp.write(var+"dListDCTP = {\n")

        nb = 0
        listP = list()
        for line in f:
            toWrite = ""

            if line.find("Unassigned") == -1 and line.find("IANA assigned this") == -1:

                if line[0] != " ":
                    name, pos = get_name(line)
                else:
                    name, pos = None, 1

                number, pos = get_number(line, pos)

                desc = get_desc(line, pos)
                
                
                if number is not None and name is not None:
                    if number.find("-") == -1:
                        toWrite = "\t"+ number + ": {'callback': None, 'protocol': '" + str.upper(name) + "', 'description': '" + desc + "'},\n"
                    else:
                        num = number.split("-")
                        nums = int(num[0])
                        nume = int(num[1]) + 1
                        for nn in range(nums, nume):
                            toWrite += "\t"+ str(nn) + ": {'callback': None, 'protocol': '" + str.upper(name) + "', 'description': '" + desc + "'},\n"


                    if line.find("  tcp") != -1:
                        # tcp.write(toWrite)
                        if number in listP:
                            print "double", number
                            res.write(number+"\n")
                        else:
                            listP.append(number)
                            tcp.write(toWrite)
                    # elif line.find("  udp") != -1:
                    #     udp.write(toWrite)
                    # elif line.find("  sctp") != -1:
                    #     sctp.write(toWrite)
                    # elif line.find("  dccp") != -1:
                    #     dccp.write(toWrite)
                    




            # For loop INC
            if nb > MAX:
                break
            nb += 1

        tcp.write("}\n")
        udp.write("}\n")
        sctp.write("}\n")
        dccp.write("}\n")


def get_number(line, pos=1):
    if pos < 1:
        pos = 1

    llen = len(line)
    ok = False

    # Get the first number
    while pos < llen and not ok:
        try:
            int(line[pos])
            if line[pos-1] == " ":
                ok = True
            break
        except ValueError:
            pass
        pos +=1

    # Get port number or range
    number = ""
    while pos < llen:
        try:
            if line[pos] == "-":
                number += line[pos]
            else:
                int(line[pos])
                number += line[pos]
        except ValueError:
            if line[pos] != " ":
                ok = False
            break
        pos +=1

    if ok:
        return number, pos
    else:
        return None, pos


def get_name(line):
    llen = len(line)
    pos = 0
    name = ""
    while pos < llen:
        if llen-pos > 2 and line[pos:pos+2] == "  ":
            break
        name += line[pos]

        pos +=1

    name = name.replace("\'", "-").replace("\"", "-").replace("\\", "-")

    return name, pos

def get_desc(line, pos):
    nline = line[pos:]
    llen = len(nline)
    pos = nline.find("p")
    if pos == -1:
        return ""
    else:
        pos += 1

    while pos < llen and nline[pos] == " ":
        pos += 1

    desc = ""
    while pos < llen:
        if nline[pos] == "\n" or (llen-pos > 2 and nline[pos:pos+2] == "  "):
            break
        desc += nline[pos]

        pos +=1

    desc = desc.replace("\'", "-").replace("\"", "-").replace("\\", "-")

    return desc



if __name__ == "__main__":
    sys.exit(main())
