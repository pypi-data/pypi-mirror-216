from prolog_primitives.basic import DistributedElements
from prolog_primitives.generatedProto import basicMessages_pb2 as basicMsg
from typing import Generator
from prolog_primitives.basic import Utils
from ..Collections import SharedCollections
import tensorflow as tf
from datasets import Dataset

def parseParams(structs: list[Utils.Struct]):
    params = {
        "epoch": 1,
        "loss": "mse",
        "batch": None,
        "learning_rate": 0.001
    }
    for struct in structs:
        if(struct.functor == "max_epoch"):
            params['epoch'] = int(struct.arguments[0])
        elif(struct.functor == "batch_size"):
            params['batch'] = int(struct.arguments[0])
        elif(struct.functor == "learning_rate"):
            params['learning_rate'] = float(struct.arguments[0])
        elif(struct.functor == "loss"):
            loss = struct.arguments[0]
            if(loss == "mse"):
                params['loss'] = "mse"
            elif(loss == "mae"):
                params['loss'] = "mae"
            elif(loss == "cross_entropy"):
                params['loss'] = tf.keras.losses.BinaryCrossentropy()
    return params

class __Train(DistributedElements.DistributedPrimitive):
    
    def solve(self, request: DistributedElements.DistributedRequest) -> Generator[DistributedElements.DistributedResponse, None, None]:
        predictor_in_ref = request.arguments[0]
        dataset_ref = request.arguments[1]
        params = request.arguments[2]
        predictor_out_ref = request.arguments[3]
        
        if(not predictor_in_ref.HasField('var') and not dataset_ref.HasField('var') and
           not params.HasField('var') and predictor_out_ref.HasField('var')):
            model: tf.keras.Model = SharedCollections().getModel(Utils.parseArgumentMsg(predictor_in_ref))
            datasetId = Utils.parseArgumentMsg(dataset_ref)
            dataset: Dataset = SharedCollections().getDataset(datasetId)
            schema = SharedCollections().getSchema(SharedCollections().getSchemaIdFromDataset(datasetId))
            params = parseParams(Utils.parseArgumentMsg(params))
            
            input = None
            output = None
            for attr in dataset.column_names:
                if(attr in schema.targets):
                    if(output == None):
                        output = tf.cast(dataset[attr], tf.float32)
                    else:
                        output = tf.stack([output, tf.cast(dataset[attr], tf.float32)], axis = 1)
                else:
                    if(input == None):
                        input = tf.cast(dataset[attr], tf.float32)
                    else:
                        input = tf.stack([input, tf.cast(dataset[attr], tf.float32)], axis = 1)
            optimizer = tf.keras.optimizers.Adam(learning_rate=params["learning_rate"])
            model.compile(
                loss = params["loss"],
                optimizer=optimizer,
                metrics=[tf.keras.metrics.CategoricalAccuracy()],
            )
            
            model.fit(x=input,y=output, batch_size=params["batch"], epochs=params["epoch"])
            
            id = SharedCollections().addModel(model)
            yield request.replySuccess(substitutions={
                predictor_out_ref.var: basicMsg.ArgumentMsg(constant=id)
                }, hasNext=False)
        else:
            yield request.replyFail()
             
trainPrimitive = DistributedElements.DistributedPrimitiveWrapper("train", 4, __Train())