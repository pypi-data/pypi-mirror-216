from prolog_primitives.basic import DistributedElements
from prolog_primitives.generatedProto import basicMessages_pb2 as basicMsg
from typing import Generator
from prolog_primitives.basic import Utils
from ..Collections import SharedCollections
import tensorflow as tf

class __ColumnPrimitive(DistributedElements.DistributedPrimitive):
    
    def solve(self, request: DistributedElements.DistributedRequest) -> Generator[DistributedElements.DistributedResponse, None, None]:
        dataset_ref = request.arguments[0]
        column = request.arguments[1]
        values = request.arguments[2]
        
        if(not dataset_ref.HasField("var") and values.HasField("var")):
            dataset = SharedCollections().getDataset(str(Utils.parseArgumentMsg(dataset_ref)))
                
            if(not column.HasField("var")): 
                i = Utils.parseArgumentMsg(column)
                if(i.isdigit()):
                    i = dataset.column_names[int(i)]
                column = list(map(Utils.stringsConverter, tf.get_static_value(dataset[i])))
                yield request.replySuccess({
                    values.var: Utils.fromListToArgumentMsg(column)
                }, hasNext=False)
            else:
                i = 0
                while(i < dataset.shape[1]):
                    name = dataset.column_names[i]
                    col = list(map(Utils.stringsConverter, tf.get_static_value(dataset[name])))
                    i += 1
                    yield request.replySuccess({
                        column.var: basicMsg.ArgumentMsg(constant=name),
                        values.var: Utils.fromListToArgumentMsg(col)
                    }, hasNext= (i < dataset.shape[1]))
                
        else:
            yield request.replyFail()
            
            
columnPrimitive = DistributedElements.DistributedPrimitiveWrapper("column", 3, __ColumnPrimitive())