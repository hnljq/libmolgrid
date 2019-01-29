import pytest
import molgrid

def eqQ(q1, q2):
    assert q1.R_component_1() == q2.R_component_1()
    assert q1.R_component_2() == q2.R_component_2()
    assert q1.R_component_3() == q2.R_component_3()
    assert q1.R_component_4() == q2.R_component_4()
    
def neqQ(q1, q2):
    assert q1.R_component_1() != q2.R_component_1()
    assert q1.R_component_2() != q2.R_component_2()
    assert q1.R_component_3() != q2.R_component_3()
    assert q1.R_component_4() != q2.R_component_4()
    
def tup(pt):
    '''tuplize a grid or point'''
    try:
        x = pt.x
        y = pt.y
        z = pt.z
    except AttributeError: #guess its a grid
        x = pt[0]
        y = pt[1]
        z = pt[2]
    return (x,y,z)
        
def test_random_transform():
  from molgrid import Transform
  molgrid.set_random_seed(0)
  c1 = molgrid.float3(0,0,0);
  c2 = molgrid.float3(0,0,1);

  t1 = Transform(c1, 4.0, True)
  t2 = Transform(c2, 4.0, True)

  nrt1 = Transform (c1)
  nrt2 = Transform (c2)

  t = Transform()

  molgrid.set_random_seed(0) # reset, should get same sample
  t3 = Transform(c1, 4.0, True);

  neqQ(t1.quaternion(),t2.quaternion());
  neqQ(t1.quaternion(),nrt1.quaternion());
  eqQ(t1.quaternion(),t3.quaternion());
  eqQ(nrt1.quaternion(),nrt2.quaternion());

  assert tup(t1.translation()) != tup(t2.translation())
  assert tup(t1.translation()) != tup(nrt1.translation())
  assert tup(t1.translation()) == tup(t3.translation())
  assert tup(nrt1.translation()) == tup(nrt2.translation())

  assert tup(c1) == tup(t1.rotation_center())
  assert tup(c2) == tup(t2.rotation_center())
  assert tup(c1) == tup(nrt1.rotation_center())

  assert tup(c1) == tup(t.rotation_center())
  assert tup(c1) == tup(t.translation())

def test_apply_transform():
    '''non-random transform'''
    from molgrid import Transform, Quaternion, float3, MGrid2f, Grid2f
    from math import sqrt
    q = Quaternion(sqrt(0.5),0,0,sqrt(0.5)) # //z 90
    nr = Transform(q, float3(0,1,1), float3(2,0,-3))

    #random
    r = Transform(float3(0,1,1), 10.0, True)

    coord_data = [ [0,0,0],
                   [1,0,0],
                   [0,1,0],
                   [0,0,1],
                   [-1,.5,3],
                   [1,1,1],
                   [0,1,1],
                   [.333,.75,-9] ]
  
    coords = MGrid2f(8,3)
    coords2 = MGrid2f(8,3)
    
    for i in range(8):
        for j in range(3):
            coords[i][j] = coord_data[i][j]

    #does nr perform as expected?
    nr.forward(coords,coords2)

    assert tup(coords2[6]) == (2,1,-2) #at center
    assert tup(coords2[2]) == (2,1,-3) #on z-axis
    assert tup(coords2[5]) == (2,2,-2)

    #make sure input unchanged
    assert tup(coords[7]) == (0.333,.75,-9)

    # does random work both ways
    r.forward(coords,coords2);
    for i in range(8):
        assert tup(coords[i]) != tup(coords2[i])
        
    r.backward(coords2,coords2);
    for i in range(8):
        assert tup(coords[i]) == tup(coords2[i])
