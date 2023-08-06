from .ml_lib.schema.schema import schemaPrimitive
from .ml_lib.schema.theoryToSchema import theoryToSchemaPrimitive
from .ml_lib.dataset.theoryToDataset import theoryToDatasetPrimitive
from .ml_lib.dataset.randomSplit import randomSplitPrimitive
from .ml_lib.dataset.column import columnPrimitive
from .ml_lib.dataset.row import rowPrimitive
from .ml_lib.dataset.cell import cellPrimitive
from .ml_lib.dataset.fold import foldPrimitive
from .ml_lib.dataset.theory_from_Dataset import theoryFromDatasetPrimitive
from .ml_lib.trasformations.schema_trasformation import schemaTrasformation
from .ml_lib.trasformations.normalization import normalizePrimitive
from .ml_lib.trasformations.one_hot_encode import one_hot_encodePrimitive
from .ml_lib.trasformations.drop import dropPrimitive
from .ml_lib.trasformations.fit import fitPrimitive
from .ml_lib.trasformations.transform import transformPrimitive
from .ml_lib.neuralNetwork.inputLayer import inputLayerPrimitive
from .ml_lib.neuralNetwork.denseLayer import denseLayerPrimitive
from .ml_lib.neuralNetwork.outputLayer import outputLayerPrimitive
from .ml_lib.neuralNetwork.neuralNetwork import neuralNetworkPrimitive
from .ml_lib.predictors.train import trainPrimitive
from .ml_lib.predictors.predict import predictPrimitive
from .ml_lib.predictors.classify import classifyPrimitive
from .ml_lib.predictors.score import msePrimitive
from .basic import PrimitiveWrapper, DistributedElements
from concurrent.futures import ThreadPoolExecutor

servers = []
libraryName = "customLibrary"

def launchPrimitive(primitive: DistributedElements.DistributedPrimitiveWrapper, port: int):
    server = PrimitiveWrapper.serve(primitive, port, libraryName)
    servers.append(server)
    server.wait_for_termination()
    
primitives = [schemaPrimitive, theoryToSchemaPrimitive,
              theoryToDatasetPrimitive, randomSplitPrimitive,
              rowPrimitive, columnPrimitive, cellPrimitive, foldPrimitive, 
              theoryFromDatasetPrimitive, schemaTrasformation,
              normalizePrimitive, one_hot_encodePrimitive, dropPrimitive,
              fitPrimitive, transformPrimitive, inputLayerPrimitive,
              denseLayerPrimitive, outputLayerPrimitive, neuralNetworkPrimitive,
              trainPrimitive, predictPrimitive, classifyPrimitive, msePrimitive]

port = 8080
executor = ThreadPoolExecutor(max_workers=len(primitives))

for primitive in primitives:
    future = executor.submit(launchPrimitive, primitive, port)
    port += 1

try:
    for server in servers:
        server.wait_for_termination()
except (Exception, KeyboardInterrupt, SystemExit) as inst:
    from .basic import DBManager
    executor.shutdown(wait=False, cancel_futures=True)
    for server in servers:
        server.stop(0)

for primitive in primitives:
    DBManager.deletePrimitive(primitive.functor, primitive.arity, libraryName)
print("Done!")
