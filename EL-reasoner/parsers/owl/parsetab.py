
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.5'

_lr_method = 'LALR'

_lr_signature = '82E56F61CC4C87949E5C0E89DDFC5C0D'
    
_lr_action_items = {'ID':([0,7,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,38,39,40,41,42,43,44,45,46,47,],[7,-11,7,7,7,7,7,28,29,30,31,7,7,7,7,7,7,-5,-3,-2,-4,-1,-9,-6,-10,-8,-7,]),'RPAREN':([7,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,],[-11,38,39,40,41,42,43,44,45,46,47,-5,-3,-2,-4,-1,-9,-6,-10,-8,-7,]),'EquivalentClasses':([0,7,13,14,15,16,17,22,23,24,25,26,27,38,39,40,41,42,43,44,45,46,47,],[3,-11,3,3,3,3,3,3,3,3,3,3,3,-5,-3,-2,-4,-1,-9,-6,-10,-8,-7,]),'SubClassOf':([0,7,13,14,15,16,17,22,23,24,25,26,27,38,39,40,41,42,43,44,45,46,47,],[4,-11,4,4,4,4,4,4,4,4,4,4,4,-5,-3,-2,-4,-1,-9,-6,-10,-8,-7,]),'ObjectIntersectionOf':([0,7,13,14,15,16,17,22,23,24,25,26,27,38,39,40,41,42,43,44,45,46,47,],[5,-11,5,5,5,5,5,5,5,5,5,5,5,-5,-3,-2,-4,-1,-9,-6,-10,-8,-7,]),'SubObjectPropertyOf':([0,7,13,14,15,16,17,22,23,24,25,26,27,38,39,40,41,42,43,44,45,46,47,],[6,-11,6,6,6,6,6,6,6,6,6,6,6,-5,-3,-2,-4,-1,-9,-6,-10,-8,-7,]),'ObjectSomeValuesFrom':([0,7,13,14,15,16,17,22,23,24,25,26,27,38,39,40,41,42,43,44,45,46,47,],[1,-11,1,1,1,1,1,1,1,1,1,1,1,-5,-3,-2,-4,-1,-9,-6,-10,-8,-7,]),'LPAREN':([1,3,4,5,6,8,9,10,11,12,],[13,14,15,16,17,18,19,20,21,22,]),'TransitiveObjectProperty':([0,7,13,14,15,16,17,22,23,24,25,26,27,38,39,40,41,42,43,44,45,46,47,],[8,-11,8,8,8,8,8,8,8,8,8,8,8,-5,-3,-2,-4,-1,-9,-6,-10,-8,-7,]),'ObjectProperty':([0,7,13,14,15,16,17,22,23,24,25,26,27,38,39,40,41,42,43,44,45,46,47,],[9,-11,9,9,9,9,9,9,9,9,9,9,9,-5,-3,-2,-4,-1,-9,-6,-10,-8,-7,]),'Class':([0,7,13,14,15,16,17,22,23,24,25,26,27,38,39,40,41,42,43,44,45,46,47,],[10,-11,10,10,10,10,10,10,10,10,10,10,10,-5,-3,-2,-4,-1,-9,-6,-10,-8,-7,]),'FunctionalObjectProperty':([0,7,13,14,15,16,17,22,23,24,25,26,27,38,39,40,41,42,43,44,45,46,47,],[11,-11,11,11,11,11,11,11,11,11,11,11,11,-5,-3,-2,-4,-1,-9,-6,-10,-8,-7,]),'$end':([2,7,38,39,40,41,42,43,44,45,46,47,],[0,-11,-5,-3,-2,-4,-1,-9,-6,-10,-8,-7,]),'Declaration':([0,7,13,14,15,16,17,22,23,24,25,26,27,38,39,40,41,42,43,44,45,46,47,],[12,-11,12,12,12,12,12,12,12,12,12,12,12,-5,-3,-2,-4,-1,-9,-6,-10,-8,-7,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([0,13,14,15,16,17,22,23,24,25,26,27,],[2,23,24,25,26,27,32,33,34,35,36,37,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> expression","S'",1,None,None,None),
  ('expression -> Declaration LPAREN expression RPAREN','expression',4,'p_declaration','owlparser.py',32),
  ('expression -> Class LPAREN ID RPAREN','expression',4,'p_class','owlparser.py',36),
  ('expression -> ObjectProperty LPAREN ID RPAREN','expression',4,'p_objectprop','owlparser.py',40),
  ('expression -> FunctionalObjectProperty LPAREN ID RPAREN','expression',4,'p_functional','owlparser.py',45),
  ('expression -> TransitiveObjectProperty LPAREN ID RPAREN','expression',4,'p_transitive','owlparser.py',49),
  ('expression -> EquivalentClasses LPAREN expression expression RPAREN','expression',5,'p_equivalent','owlparser.py',53),
  ('expression -> SubObjectPropertyOf LPAREN expression expression RPAREN','expression',5,'p_subobjectproperty','owlparser.py',58),
  ('expression -> ObjectIntersectionOf LPAREN expression expression RPAREN','expression',5,'p_objectintersection','owlparser.py',62),
  ('expression -> ObjectSomeValuesFrom LPAREN expression expression RPAREN','expression',5,'p_objectsomevalues','owlparser.py',66),
  ('expression -> SubClassOf LPAREN expression expression RPAREN','expression',5,'p_subclass','owlparser.py',70),
  ('expression -> ID','expression',1,'p_id','owlparser.py',74),
]