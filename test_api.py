import unittest
import json
from api import lambda_handler

class LambdaHandlerTestCase(unittest.TestCase):
  def test_lambda_handler(self):
    event = {
      'body': '[{"acceleration":{"timestamp":1523719520931,"z":9.883264541625977,"y":-0.1628057211637497,"x":-0.047884032130241394},"gyroscope":{"timestamp":1523719520891,"z":0,"y":0.0024434609804302454,"x":0}},{"acceleration":{"timestamp":1523719521031,"z":9.873687744140625,"y":-0.17238251864910126,"x":-0.07661445438861847},"gyroscope":{"timestamp":1523719520991,"z":0,"y":0.0024434609804302454,"x":0}},{"acceleration":{"timestamp":1523719521131,"z":9.864110946655273,"y":-0.15322890877723694,"x":-0.019153613597154617},"gyroscope":{"timestamp":1523719521091,"z":0,"y":0.0024434609804302454,"x":0}},{"acceleration":{"timestamp":1523719521231,"z":9.90241813659668,"y":-0.17238251864910126,"x":-0.038307227194309235},"gyroscope":{"timestamp":1523719521191,"z":0,"y":0.0024434609804302454,"x":0}},{"acceleration":{"timestamp":1523719521331,"z":9.864110946655273,"y":-0.181959331035614,"x":-0.07661445438861847},"gyroscope":{"timestamp":1523719521291,"z":0,"y":0.0024434609804302454,"x":0}}]',
      'queryStringParameters': {
        'device': '66549871'
      }
    }

    lambda_handler(event, None)