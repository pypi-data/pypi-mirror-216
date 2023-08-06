
from prolog_primitives.generatedProto import basicMessages_pb2 as basicMsg

class Struct:
    functor: str
    arguments: list
    
    def __init__(self, functor: str, arguments: list):
        self.functor = functor
        self.arguments = arguments
        
    def __str__(self):
        term = self.functor + "("
        for arg in self.arguments:
            term += str(arg) + ","
        if(term[-1] == ","):
            return term[:-1] + ")"
        else:
            return term[:-1]

def parseArgumentMsg(msg: basicMsg.ArgumentMsg):
    if(msg.HasField("struct")):
        if(msg.struct.functor == "."):
            return parseArgumentMsgList(msg)
        else:   
            return parseStructMsg(msg.struct)
    elif(msg.HasField("var")):
        return msg.var
    elif(msg.HasField("constant")):
        return msg.constant
    
def parseStructMsg(msg: basicMsg.StructMsg):
    if(len(msg.arguments) > 0):
        arguments = list()
        for arg in msg.arguments:
            arguments.append(parseArgumentMsg(arg))
        return Struct(msg.functor, arguments)
    else:   
        return msg.functor
    
    
def parseArgumentMsgList(msg: basicMsg.ArgumentMsg) -> list:
    returnValue = list()
    currentValue = msg.struct
    while(len(currentValue.arguments) != 0):
        returnValue.append(parseArgumentMsg(currentValue.arguments[0]))
        currentValue = currentValue.arguments[1].struct
    return returnValue 

def fromListToArgumentMsg(elements: list) -> basicMsg.ArgumentMsg:
    last_element = basicMsg.ArgumentMsg(
        struct=basicMsg.StructMsg(
                functor = "[]"
            )
        )
    
    elements.reverse()
    for i in elements:
        current_element = basicMsg.StructMsg(
            functor="."
        )
        if(type(i) is basicMsg.StructMsg):
            current_element.arguments.append(
                basicMsg.ArgumentMsg(struct=i)
            )
        else:
            current_element.arguments.append(
                basicMsg.ArgumentMsg(constant=str(i))
            )
        current_element.arguments.append(
                last_element
            )
        last_element = basicMsg.ArgumentMsg(
            struct = current_element
        )
    return last_element
      
def stringsConverter(x):
    if(type(x) is bytes):
        return x.decode('utf-8')
    else:
        return str(x)