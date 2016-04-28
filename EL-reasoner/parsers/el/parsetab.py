
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.5'

_lr_method = 'LALR'

_lr_signature = '250610BCB2E7BB33E449A670A862575A'
    
_lr_action_items = {'RIN':([1,2,4,6,13,16,19,],[-9,-8,-10,8,-7,-5,-6,]),'ID':([0,5,7,8,9,10,11,12,18,],[2,7,2,2,2,2,2,2,2,]),'EQUIV':([1,2,4,6,13,16,19,],[-9,-8,-10,9,-7,-5,-6,]),'EXISTS':([0,7,8,9,10,11,12,18,],[5,5,5,5,5,5,5,5,]),'IN':([1,2,4,6,13,16,19,],[-9,-8,-10,11,-7,-5,-6,]),'NOT':([11,],[18,]),'TOP':([0,7,8,9,10,11,12,18,],[4,4,4,4,4,4,4,4,]),'INTER':([1,2,4,6,13,14,15,16,17,19,20,],[-9,-8,-10,12,12,12,12,12,12,12,12,]),'$end':([1,2,3,4,13,14,15,16,17,19,20,],[-9,-8,0,-10,-7,-4,-3,-5,-2,-6,-1,]),'BOTTOM':([0,7,8,9,10,11,12,18,],[1,1,1,1,1,1,1,1,]),'RCOMP':([1,2,4,6,13,14,15,16,17,19,20,],[-9,-8,-10,10,10,10,10,10,10,10,10,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([0,],[3,]),'rc':([0,7,8,9,10,11,12,18,],[6,13,14,15,16,17,19,20,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> expression","S'",1,None,None,None),
  ('expression -> rc IN NOT rc','expression',4,'p_concept_neg','elparser.py',49),
  ('expression -> rc IN rc','expression',3,'p_expression_in','elparser.py',53),
  ('expression -> rc EQUIV rc','expression',3,'p_expression_equiv','elparser.py',57),
  ('expression -> rc RIN rc','expression',3,'p_expression_rin','elparser.py',61),
  ('rc -> rc RCOMP rc','rc',3,'p_role_rcomp','elparser.py',65),
  ('rc -> rc INTER rc','rc',3,'p_concept_inter','elparser.py',69),
  ('rc -> EXISTS ID rc','rc',3,'p_concept_exists','elparser.py',73),
  ('rc -> ID','rc',1,'p_rc_id','elparser.py',77),
  ('rc -> BOTTOM','rc',1,'p_rc_bottom','elparser.py',81),
  ('rc -> TOP','rc',1,'p_rc_top','elparser.py',85),
]