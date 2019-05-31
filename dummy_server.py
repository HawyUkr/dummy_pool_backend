
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

from jsonrpc import JSONRPCResponseManager, dispatcher
import random

difft =2e8
n_target = int(2**256//int(difft))

current_block = 0
def hash_by_heigth(height):
  return random.randint(1, int(1)).to_bytes(4,"big").hex().upper()+height.to_bytes(28, "big").hex().upper()


@dispatcher.add_method
def eth_getWork(*args):
      print("getWork")
      _hash = hash_by_heigth(current_block)
      seed = "0x"+"00"*32
      target = "0x"+n_target.to_bytes(32,"big").hex().upper()
      height = "0x"+current_block.to_bytes(8, "big").hex().upper()
      return _hash, seed, target, height 

@dispatcher.add_method
def eth_submitWork(*args):
      global current_block
      print("submitWork")
      current_block+=1
      return True

@dispatcher.add_method
def eth_getBlockByNumber(*args):
      print("gbbn")
      return {'number':"0x"+current_block.to_bytes(8, "big").hex(), 'difficulty':"0x"+difft.to_bytes(8,"big").hex().upper()}

@Request.application
def application(request):
    # Dispatcher is dictionary {<method_name>: callable}
    dispatcher["echo"] = lambda s: s
    dispatcher["add"] = lambda a, b: a + b
    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


run_simple('localhost', 4000, application)
