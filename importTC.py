
import csv
import ctrl

# columns
subsystem, number, name, pid, desc, lparam, nparam = 0,1,2,6,7,14,15
pdesc, pname, ptyp, psize, punit, prng = 16,17,18,19,20,21

a = csv.reader(open('commands.csv'), delimiter='#')

a.next()

n = None
for line in a:
    if line[subsystem] != "":
        if n is not None:
            if n_nparam != len(n['param']):
                print("ERROR: nparam not matching length of param")
            print(n)
            ctrl.cmd.cm.Cm(**n).to_json_file()
        n = {'number': int(line[number]),
                'name': str(line[name]).strip().replace(' ', '_'),
                'pid': str(line[pid]).strip(),
                'desc': str(line[desc]).strip(),
                'lparam': int(0 if line[lparam].strip() == "" else line[lparam])\
                            if line[lparam].strip() != "*" else "*",
                'subsystem': str(line[subsystem]).lower().replace(' ', '_'),
                'param': []}
        n_nparam = int(line[nparam] if line[nparam].strip() != "" else 0)
    if n_nparam == 0:
        n['lparam'] = 0
    else:
        n['param'].append([str(line[pname]).strip().replace(' ', '_'),
                            str(line[pdesc]).strip(),
                            str(line[prng]).strip(),
                            str(line[ptyp]).strip().replace('_t', ''),
                            str(line[psize]).strip(),
                            str(line[punit]).strip().replace(' ', '_')])
print(n)
ctrl.cmd.cm.Cm(**n).to_json_file()
