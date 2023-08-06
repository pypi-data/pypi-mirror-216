from prolog_primitives.basic import DistributedElements
from prolog_primitives.generatedProto import basicMessages_pb2 as basicMsg
from typing import Generator
from prolog_primitives.basic import Utils
from ..Collections import SharedCollections
import tensorflow as tf
from datasets import Dataset
from abc import ABC, abstractmethod



class __AssessTemplate(DistributedElements.DistributedPrimitive, ABC):
    
    @abstractmethod
    def evaluator(self, y_true, y_pred):
        pass
    
    def solve(self, request: DistributedElements.DistributedRequest) -> Generator[DistributedElements.DistributedResponse, None, None]:
        y_true_ref = request.arguments[0]
        y_pred_ref = request.arguments[1]
        score = request.arguments[2]
        
        if(not y_true_ref.HasField('var') and not y_pred_ref.HasField('var') and
           score.HasField('var')):
            
            def parseY(input):
                if(type(input) is str):
                    dataset = SharedCollections().getDataset(input)
                    y = {}
                    for attr in dataset.column_names:
                        y[attr] = list(tf.get_static_value(dataset[attr]))
                    return y
                elif(type(input[0]) is list):
                    y = []
                    for x in range(len(input[0])):
                        y.append([float(input[0][x])])
                        
                    for row in input[1:]:
                        for x in range(len(row)):
                            y[x].append(float(row[x]))
                    return y
                else:
                    return [float(x) for x in input]
                
            y_true = parseY(Utils.parseArgumentMsg(y_true_ref))
                    
            y_pred = parseY(Utils.parseArgumentMsg(y_pred_ref))   
                
            scores = []   
            for (attr, y1), y2 in zip(y_true.items(), y_pred):
                scores.append(self.evaluator(y1, y2))
            
            totalscore = tf.get_static_value(sum(scores)/len(scores))
                            
            yield request.replySuccess(substitutions={
                score.var: basicMsg.ArgumentMsg(constant=str(totalscore))
            }, hasNext=False)

        else:
            yield request.replyFail()
            
class __Mse(__AssessTemplate):
    
    def evaluator(self, y_true, y_pred):
        return tf.keras.metrics.mean_squared_error(y_true, y_pred)
                 
msePrimitive = DistributedElements.DistributedPrimitiveWrapper("mse", 3, __Mse())


class __Mae(__AssessTemplate):
    
    def evaluator(self, y_true, y_pred):
        return tf.keras.metrics.mean_absolute_error(y_true, y_pred)
                 
maePrimitive = DistributedElements.DistributedPrimitiveWrapper("mae", 3, __Mae())

class __R(__AssessTemplate):
    
    def evaluator(self, y_true, y_pred):
        m = tf.keras.metrics.RootMeanSquaredError()
        m.update_state(y_true, y_pred)
        return m.result().numpy()
                 
rPrimitive = DistributedElements.DistributedPrimitiveWrapper("r", 3, __R())


class __Recall(__AssessTemplate):
    
    def evaluator(self, y_true, y_pred):
        m = tf.keras.metrics.Recall()
        m.update_state(y_true, y_pred)
        return m.result().numpy()
                 
recallPrimitive = DistributedElements.DistributedPrimitiveWrapper("recall", 3, __Recall())


class __Accuracy(__AssessTemplate):
    
    def evaluator(self, y_true, y_pred):
        m = tf.keras.metrics.Accuracy()
        m.update_state(y_true, y_pred)
        return m.result().numpy()
                 
accuracyPrimitive = DistributedElements.DistributedPrimitiveWrapper("accuracy", 3, __Accuracy())

#only available via pip install tf-nightly.
class __F1Score(__AssessTemplate):
    
    def evaluator(self, y_true, y_pred):
        m = tf.keras.metrics.F1Score()
        m.update_state(y_true, y_pred)
        return m.result().numpy()
                 
f1ScorePrimitive = DistributedElements.DistributedPrimitiveWrapper("f1_score", 3, __F1Score())