
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.5'

_lr_method = 'LALR'

_lr_signature = '5D636C90C5CF11D5A6868601407A53B8'
    
_lr_action_items = {'LPAREN':([0,1,2,10,11,12,13,14,15,20,25,],[1,1,9,1,1,1,1,1,1,1,1,]),'EXISTS':([0,1,10,11,12,13,14,15,20,25,],[2,2,2,2,2,2,2,2,2,2,]),'RIN':([3,4,5,7,16,18,22,24,28,],[-9,11,-8,-7,-10,-11,-5,-6,-12,]),'VIRG':([17,],[25,]),'$end':([3,5,6,7,16,18,19,21,22,23,24,26,28,],[-9,-8,0,-7,-10,-11,-4,-2,-5,-3,-6,-1,-12,]),'RCOMP':([3,4,5,7,8,16,18,19,21,22,23,24,26,27,28,],[-9,13,-8,-7,13,-10,13,13,13,13,13,13,13,13,-12,]),'NOT':([12,],[20,]),'IN':([3,4,5,7,16,18,22,24,28,],[-9,12,-8,-7,-10,-11,-5,-6,-12,]),'TOP':([0,1,10,11,12,13,14,15,20,25,],[3,3,3,3,3,3,3,3,3,3,]),'EQUIV':([3,4,5,7,16,18,22,24,28,],[-9,14,-8,-7,-10,-11,-5,-6,-12,]),'BOTTOM':([0,1,10,11,12,13,14,15,20,25,],[5,5,5,5,5,5,5,5,5,5,]),'INTER':([3,4,5,7,8,16,18,19,21,22,23,24,26,27,28,],[-9,15,-8,-7,15,-10,15,15,15,15,15,15,15,15,-12,]),'RPAREN':([3,5,7,8,16,18,22,24,27,28,],[-9,-8,-7,16,-10,-11,-5,-6,28,-12,]),'ID':([0,1,2,9,10,11,12,13,14,15,20,25,],[7,7,10,17,7,7,7,7,7,7,7,7,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([0,],[6,]),'rc':([0,1,10,11,12,13,14,15,20,25,],[4,8,18,19,21,22,23,24,26,27,]),}

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
  ('rc -> rc RCOMP rc','rc',3,'p_role_rcomp','elparser.py',66),
  ('rc -> rc INTER rc','rc',3,'p_concept_inter','elparser.py',70),
  ('rc -> ID','rc',1,'p_rc_id','elparser.py',74),
  ('rc -> BOTTOM','rc',1,'p_rc_bottom','elparser.py',78),
  ('rc -> TOP','rc',1,'p_rc_top','elparser.py',82),
  ('rc -> LPAREN rc RPAREN','rc',3,'p_rc_paren','elparser.py',86),
  ('rc -> EXISTS ID rc','rc',3,'p_concept_exists','elparser.py',90),
  ('rc -> EXISTS LPAREN ID VIRG rc RPAREN','rc',6,'p_concept_exists2','elparser.py',94),
]