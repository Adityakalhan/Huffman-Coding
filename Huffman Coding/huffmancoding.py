import heapq
import os

#creating a binary tree node to store the frequency of characters and frequencies to generate the binary code
class BinaryTreeNode :
    
    def __init__(self,value,frequency) :
        self.value = value
        self.frequency = frequency
        self.left = None
        self.right = None
    
    def __lt__(self,other) : #we will give priority according to value of frequency of the char
        return self.frequency < other.frequency
#main
class HuffManCoding :

    def __init__(self,path) :
        self.path = path
        self.__heap = []
        self.__CodesMap = {} #char to code
        self.__reverseCodeMap = {} #code to char
        self.filetype = '.txt'


    def __createFequencyDict(self,text) :
        frequencyDict = {}

        for char in text :
            frequencyDict[char] = frequencyDict.get(char,0) + 1
        
        return frequencyDict

    def __createHeap(self,frequencyDict) :

        for key in frequencyDict :
            Heapnode = BinaryTreeNode(key,frequencyDict[key])
            heapq.heappush(self.__heap,Heapnode)

        
    def __createTree(self) :
        while len(self.__heap) > 1 :
            binaryTreeNode1 = heapq.heappop(self.__heap)
            binaryTreeNode2 = heapq.heappop(self.__heap)
            freq_sum = binaryTreeNode1.frequency + binaryTreeNode2.frequency
            newNode = BinaryTreeNode(None,freq_sum)
            newNode.left = binaryTreeNode1 
            newNode.right = binaryTreeNode2
            heapq.heappush(self.__heap,newNode)


    def __getCodeHelper(self,root,current_bits):
        if root == None : #base case
            return
        if root.value != None :
            self.__CodesMap[root.value] = current_bits
            self.__reverseCodeMap[current_bits] = root.value
            return
        
        self.__getCodeHelper(root.left,current_bits+'0')
        self.__getCodeHelper(root.right,current_bits+'1')
    def __getCode(self) :
        root = heapq.heappop(self.__heap)
        self.__getCodeHelper(root,'')

    def __getEncodedText(self,text) :

        encodedText = ''
        for char in text :
            encodedText += self.__CodesMap[char]
        
        return encodedText

    def __padEncodedText(self,text) :
        paddingAdded = 8 - (len(text)%8)
        for i in range(paddingAdded) :
            text += '0'

        padding = '{0:08b}'.format(paddingAdded)
        padded_encoded_text = padding + text
        return padded_encoded_text

    def __getBytesArray(self,padded_encoded_text) :
        bytesArr = []
        for i in range(0,len(padded_encoded_text),8) :
            bytesArr.append(int(padded_encoded_text[i:i+8],2))
        return bytesArr
    def compress(self) :
        filename,filetype = os.path.splitext(self.path)
        self.filetype = filetype
        output_path = filename + '.bin' #for returning the binary file
        with open(self.path,'r+') as file, open(output_path,'wb') as output :

            text = file.read() #read the file
            text = text.rstrip() #remove any extra spaces

            #create a dictionary for all the frequency of the letters.
            frequencyDict = self.__createFequencyDict(text)
            #we now have to create a minimum heap using the frequency.
            self.__createHeap(frequencyDict)
            #we now have to create a binary tree using heap
            self.__createTree()
            #we now create maps for the char to code and code to char.
            self.__getCode()
            
            #we now need to make an encoded text, ie binary text with the codes from our codemap.
            encodedText = self.__getEncodedText(text)
            #we need to add padding to our code to make it a perfect multiple of 8 and keep track of the number of 0 added at the add.
            padded_encoded_text = self.__padEncodedText(encodedText)
            #we now have all the bits required, we now have to convert it into bytes.
            bytesArr = self.__getBytesArray(padded_encoded_text)
            #we now create the final bytes by creating this byteArray into bytes
            final_byte = bytes(bytesArr)
            #now we write our output in the binary file
            output.write(final_byte)
        print('compressed')
        return output_path

    def __removepadding(self,bitstring) :
        paddedbits = bitstring[:8]
        amount_padded = int(paddedbits,2)
        #bitstring = bitstring[8:]
        encoded_text = bitstring[8:-1*amount_padded]
        
            
        return encoded_text
    
    def __decompressText(self,actual_text) :

        decoded_text = ''
        bitstring = ''

        for bits in actual_text :
            bitstring += bits
            if bitstring in self.__reverseCodeMap :
               
                decoded_text += self.__reverseCodeMap[bitstring]
                bitstring = ''
        
        return decoded_text


    def decompress(self,binFilePath) :
        filename,filetype = os.path.splitext(binFilePath)
        output_path = filename + '_decompressed' + self.filetype
        with open (binFilePath,'rb') as file, open(output_path,'w') as output :
            #we need to get the bit string from the byte file
            bitstring = ''
            byte = file.read(1) #reading the byte one by one
            while byte :
                byte = ord(byte)
                #getting bits from byte
                bits = bin(byte)[2:].rjust(8,'0') 
                #appending the bit in the bitstring
                bitstring += bits
                byte = file.read(1)

                #byte will be null when it reached the end
            
            #we need to remove padding to get the encoded text
            actual_text = self.__removepadding(bitstring)
            #we need to get the text from the encoded text
            decompressed_text = self.__decompressText(actual_text)
            output.write(decompressed_text)
        
        print('decompressed')
        #return output_path

path = r'C:\Users\Aditya Kalhan\OneDrive\Desktop\College\Coding Ninja\codes\Milestone 3\Huffman Coding\sample.docx'
# h = HuffManCoding(path)
# h.compress()
# reversePath = r'C:\Users\Aditya Kalhan\OneDrive\Desktop\College\Coding Ninja\codes\Milestone 3\Huffman Coding\sample.txt'
# h.decompress(reversePath)
h = HuffManCoding(path)
reversepath = h.compress()
h.decompress(reversepath)
