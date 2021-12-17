def parse_logs(filename):
    with open(filename) as file:
        data = file.read()

    blocks = data.split('\n')
    blocks[:] = [line for line in blocks if line]

    res = []
    i = 0
    while i < len(blocks):
        is_sequence = (len(blocks[i].split('-')) == 2)
        
        if is_sequence:
            split = blocks[i].split('-')
            frame_period = int(split[0].split(':')[1].strip())

            cadence_ips = int(split[1].split(':')[1].strip())
            i += 1

            progressive = int(blocks[i].split(':')[1].strip())
            i += 1
            
            res.append((is_sequence, progressive, frame_period, cadence_ips))

        else:
            progressive = int(blocks[i].split(':')[1].strip())
            i += 1
            
            tff = int(blocks[i].split(':')[1].strip())
            i +=1
            
            rff = int(blocks[i].split(':')[1].strip())
            i += 1
            
            res.append((is_sequence, progressive, tff, rff))

    return res

if __name__ == '__main__':
    res = parse_logs("./output")
    print("Print first three elements:")
    print(res[:3])
