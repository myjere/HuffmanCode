"""
LZ77编码与Huffman编码结合压缩
"""
import PIL.Image
import struct
picturewidth = 0
pictureheight = 0
frequency = {}
nodelist = []
codeformat = {}

class huffnode:
    def __init__(self,left = None,right = None,father = None,weight = None,code = None):
        self.left = left
        self.right = right
        self.father = father
        self.weight = weight  #代表值，如第一个读取值为244
        self.code = code  #代表权值

def freq(list):
    global frequency
    for i in list:
        if i not in frequency.keys():
            frequency[i] = 1
        else:
            frequency[i] +=1

def leafnode(valuelist):
    for i in range(len(valuelist)):
        nodelist.append(huffnode(weight = valuelist[i][1],code = str(valuelist[i][0])))
    return nodelist

def buildtree(listnode):
    listnode = sorted(listnode,key=lambda x:x.weight)
    while len(listnode) != 1:
        temp1 = listnode[0]
        temp2 = listnode[1]
        newnode = huffnode()
        newnode.weight = temp1.weight + temp2.weight
        newnode.left = temp1
        newnode.right = temp2
        temp1.father = newnode
        temp2.father = newnode
        listnode.remove(temp1)
        listnode.remove(temp2)
        listnode.append(newnode)
        listnode = sorted(listnode,key=lambda x:x.weight)
    return listnode

def encode(inputfile):
    picture = PIL.Image.open(inputfile)
    picture = picture.convert('L') 
    width = picture.size[0]
    height = picture.size[1]
    global pictureheight
    pictureheight = height
    print(pictureheight)
    global picturewidth
    picturewidth = width
    print(picturewidth)
    img = picture.load()
    list = []
    for i in range(0,width):
        for j in range(0,height):
            list.append(img[i,j])
    freq(list)
    global frequency
    frequency_list = frequency
    frequency_list = sorted(frequency_list.items(),key=lambda x:x[1])
    node_leaf = leafnode(frequency_list)
    head = buildtree(node_leaf)[0]
    global codeformat
    for n in node_leaf:
        node_new = n
        codeformat.setdefault(n.code,"")
        while node_new != head:
            if node_new.father.left == node_new:
                codeformat[n.code] = '1'+codeformat[n.code]
            else:
                codeformat[n.code] = '0'+codeformat[n.code]
            node_new = node_new.father
    for k in codeformat.keys():
        print("Key:"+k+"HuffmanCode:"+codeformat[k])
    result = ''
    for i in range(0,width):
        for j in range(0,height):
            for key,values in codeformat.items():
                if str(img[i,j]) == key:
                    result = result+values
    print(result)
    file = open('C:\\Users\\Jeremy\\Desktop\\软件技术基础大作业\\HuffmanCode\\testpicture\\resultoutput','w')
    file.write(result)

def compress(outputfile):
    temp = open('C:\\Users\\Jeremy\\Desktop\\软件技术基础大作业\\HuffmanCode\\testpicture\\resultoutput','r')
    temp = temp.readlines()[0].strip('\n')
    str = temp
    remainder = 8-temp.__len__()%8
    file = open(outputfile,'wb')
    for i in range(0,str.__len__(),8):
        #处理结尾数据，余数补0
        if i+8 > str.__len__():
            char = 00000000
            binary = str[i:]
            b = ''
            for i in range(remainder):
                b = b+'0'
            binary = b+binary
            for j in range(8):
                if binary[j] == '1':
                    if j == 7:
                        char += 1
                    else:
                        char += 1
                        char = char << 1
                if binary[j] == '0':
                    if j == 7:
                        pass
                    else:
                        char = char << 1
            file.write(struct.pack("B",char))
            break
        binary = str[i:i+8]
        char = 00000000
        for j in range(8):
            if binary[j] == '1':
                if j == 7:
                    char += 1
                else:
                    char += 1
                    char = char << 1
            if binary[j] == '0':
                if j == 7:
                    pass
                else:
                    char == char << 1
        file.write(struct.pack("B",char))
    file.write(struct.pack("B",remainder))
    print("Compress Finished")

def decode(inputfile):
    f = open('C:\\Users\\Jeremy\\Desktop\\软件技术基础大作业\\HuffmanCode\\testpicture\\decodeoutput','w')
    tp = open('C:\\Users\\Jeremy\\Desktop\\软件技术基础大作业\\HuffmanCode\\testpicture\\resultoutput','r')
    tp = tp.readlines()[0].strip('\n')
    l = int((tp.__len__() - tp.__len__()%8)/8)
    list = []
    for i in range(l):
        file = open(inputfile,'rb')
        file.seek(i)
        (a,) = struct.unpack("B",file.read(1))
        print("这是第"+str(i)+"个a，值为"+str(a))
        print(l)
        list.append(a)
    file.close()
    result = ''
    for i in range(len(list)-2):
        b = ''
        #bin:返回一个整数的二进制形式
        for j in range(8-len(bin(list[i])[2:])):
            b = b + '0'
        binary = b + bin(list[i])[2:]
        result = result + binary
    remainder = 8-list[-1]
    last = bin(list[-2])[2:]
    if last.__len__() != remainder:
        b = ''
        for j in range(8-remainder-last.__len__()):
            b = b + '0'
        binary = b+bin(list[-2])[2:]
        result = result + binary
    if last.__len__() == remainder:
        result = result + bin(list[-2])[2:]
    f.write(result)

def decompress(outputfile,picturewidth,pictureheight):
    file = open('C:\\Users\\Jeremy\\Desktop\\软件技术基础大作业\\HuffmanCode\\testpicture\\decodeoutput','r')
    strlist = file.readlines()[0].strip('\n')
    i = 0
    scan = ''
    recover = []
    while(i != strlist.__len__()):
        scan = scan + strlist[i]
        for key in codeformat.keys():
            if scan == codeformat[key]:
                recover.append(key)
                scan = ''
                break
        i += 1
    print(pictureheight)
    print(picturewidth)
    p = PIL.Image.new('L',(picturewidth,pictureheight))
    k = 0
    for i in range(picturewidth):
        for j in range(pictureheight):
            p.putpixel((i,j),(int(recover[k])))
            k += 1
    p.save(outputfile)
    print("Decompress Finished")

if __name__ == '__main__':
    inputcode = input("输入操作：1.压缩文件 2.解压文件\n")
    if inputcode == '1':
        encode(input("输入待压缩文件名：\n"))
        compress(input("输入压缩后文件名：\n"))
    if inputcode == '2':
        decode(input("输入待解压文件：\n"))
        decompress('C:\\Users\\Jeremy\\Desktop\\软件技术基础大作业\\HuffmanCode\\testpicture\\output.bmp',800,600)
        #decompress(input("输入还原图像名：\n"),int(input("输入还原图像像素宽度：\n")),int(input("输入还原图像像素长度：\n")))

    

