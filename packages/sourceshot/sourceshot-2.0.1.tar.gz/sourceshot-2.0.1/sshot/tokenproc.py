def split_line(token_list):
    result=[]
    temp=[]
    for i,j in token_list:
        if '\n' not in j:
            temp.append((i,j))
        else:
            if j=='\n':
                result.append(temp)
                temp=[]
                continue
            jsplit=j.split('\n')
            for k in jsplit:
                temp.append((i,k))
                result.append(temp)
                temp=[]
    return result
