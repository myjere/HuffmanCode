import sys
#压缩大文件时修改递归深度限制
sys.setrecursionlimit(1000000)

#定义哈夫曼树的节点类，功能包括初始化节点信息、利用左右子节点构造父节点、对节点编码
class HuffNode(object):
    #初始化节点类的权重值、左子节点、右子节点、父节点
    def __init__(self,value = None,left = None,right = None,father = None):
        self.value = value
        self.left = left
        self.right = right
        self.father = father
    #定义通过左右子节点构建父节点的方法
    def buildfather(left,right):
        #父节点由左子节点和右子节点构成
        RNode = HuffNode(left.value+right.value,left,right)
        #构建父节点和两个子节点的关系
        left.father = RNode
        right.father = RNode
        return RNode
    #定义对哈夫曼树节点编码的方式,RNode表示的是哈夫曼树中某个节点
    def encode(RNode):
        #如果该节点就是哈夫曼树顶的节点
        if RNode.father == None:
            #以bytes返回
            return b''
        #如果该节点是某个父节点的左节点
        if RNode.father.left == RNode:
            #左子节点编码为0，该节点的全局编码是其父节点的编码后面加个0
            return HuffNode.encode(RNode.father) + b'0'
        #如果该节点是某个父节点的右节点
        else:
            return HuffNode.encode(RNode.father) + b'1'

#定义哈夫曼树的构建方法(循环构建)
def BuildHuffTree(HuffList):
    #当输入的列表中不止一个节点时，进行循环构建
    while len(HuffList) > 1:
        #按照权重值进行从小到大的排序
        lists = sorted(HuffList,key=lambda x:x.value,reverse = False)
        #取出其中最小的两个构建一个哈夫曼树，以RNode为父节点
        RNode = HuffNode.buildfather(lists[0],lists[1])
        #将这两个删除，并将新构建的父节点加入到列表中
        lists = lists[2:]
        lists.append(RNode)
    #最终经过循环，返回哈夫曼树顶端的节点
    return HuffList[0]

#定义文件压缩的方法
def compress(inputfile):
    print("开始编码")
    #以二进制格式打开文件
    f = open(inputfile,'rb')
    #每次读取宽度为一个字节
    bytes_width = 1
    #定义要读取的次数count
    f.seek(0,2)
    count = f.tell()/bytes_width
    print("读取次数："+count)
    #定义一个空的buff列表存的是每次读取的源数据，长度为要读取的次数，存入均以bytes形式存入
    buff = [b''] * int(count)
    f.seek(0)

    #进行第一次扫描，生成一个权值字典
    for i in range(0,count):
        buff[i] = f.read(bytes_width)
        #如果本次读取的字符不在权值字典中，则将其添加进去
        if char_dict.get(buff[i],10086) == 10086:
            char_dict[buff[i]] = 0
        char_dict[buff[i]] = char_dict[buff[i]] + 1
    print("第一次扫描完毕")
    #控制台输出权值字典
    for j in char_dict.keys():
        print(j,":",char_dict[j])
    #利用第一次扫描的权值字典生成原始哈夫曼节点（最底层的叶节点）
    nodes = []
    for i in char_dict.keys():
        node_dict[i] = HuffNode(char_dict[i])
        nodes.append(node_dict[i])

    







if __name__ == '__main__':
    char_dict = {}
    node_dict = {}
    nodes = []
