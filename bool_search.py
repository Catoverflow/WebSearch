# {A:{b,c,d}}，从倒排表建立的字典
DIC={'the':{0,1,2,3,4,5},'a':{0,1,2,3,4,5},'one':{1},'two':{2},'three':{3}}
reversedchar={"and","or","not","(",")"}
#输入并初步处理，包括去小写，去多余空格，以空格和括号分词，将保留字之外的词直接转换为对应集合
def inputprocess():
    return [DIC[i] if i not in reversedchar else i for i in ' '.join(input("bool_search:input:search source:::").lower().replace('('," ( ").replace(')'," ) ").split()).split(' ')]
#得到全集以处理not
def getmost(inputlist):
    most=set()
    for i in inputlist:
        if isinstance(i,set):
            most=most.union(i)
    return most
#实际计算
def  calculate(list):
    calist=list
    most=getmost(list)
    while len(calist)>1:
        if "not" in calist:
            for j in range(len(calist)):
                if calist[j] == "not":
                    calist[j+1]=most.difference(calist[j+1])
                    del(calist[j])
                    break
        else:
            for j in range(len(calist)):
                if calist[j] == "and":
                    calist[j+1]=calist[j-1].intersection(calist[j+1])
                    del(calist[j-1:j+1])
                    break
                if calist[j] == "or":
                    calist[j+1]=calist[j-1].union(calist[j+1])
                    del(calist[j-1:j+1])
                    break
    return calist

#递归处理括号
def bracketprocess(inputlist):
    if(")" in inputlist):
        r_index=inputlist.index(")")
        inputlist_temp=inputlist[:r_index]
        l_index=0
        for i in range(len(inputlist_temp)):
            if inputlist_temp[i] == "(":
                l_index=i
        inputlist_temp=inputlist[l_index+1:r_index]
        inputlist[l_index:r_index+1]=calculate(inputlist_temp)
        bracketprocess(inputlist)
    return calculate(inputlist)
#主函数。用来说明怎么让它跑起来。得到的结果是[{0,1,2}]这种形式。
def main():
    print(bracketprocess(inputprocess()))

main()