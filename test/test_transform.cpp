/*
 * test_transform.cpp
 *
 *  Created on: Jan 10, 2019
 *      Author: dkoes
 */

#define BOOST_TEST_MODULE transform_test
#include <boost/test/unit_test.hpp>
#include <boost/test/floating_point_comparison.hpp>
#include <thrust/reduce.h>
#include <thrust/execution_policy.h>

#include "libmolgrid.h"
#include "transform.h"
#include "managed_grid.h"
#include "test_transform.h"
using namespace libmolgrid;



BOOST_AUTO_TEST_CASE( random_transform)
{
  random_engine.seed(0);
  float3 c1 = make_float3(0,0,0);
  float3 c2 = make_float3(0,0,1);

  Transform t1(c1, 4.0, true);
  Transform t2(c2, 4.0, true);

  Transform nrt1(c1);
  Transform nrt2(c2);

  Transform t;

  random_engine.seed(0); //reset, should get same sample
  Transform t3(c1, 4.0, true);

  neqQ(t1.quaternion(),t2.quaternion());
  neqQ(t1.quaternion(),nrt1.quaternion());
  eqQ(t1.quaternion(),t3.quaternion());
  eqQ(nrt1.quaternion(),nrt2.quaternion());

  neqPt(t1.translation(),t2.translation());
  neqPt(t1.translation(),nrt1.translation());
  eqPt(t1.translation(),t3.translation());
  eqPt(nrt1.translation(),nrt2.translation());

  eqPt(c1,t1.rotation_center());
  eqPt(c2,t2.rotation_center());
  eqPt(c1,nrt1.rotation_center());

  eqPt(c1,t.rotation_center());
  eqPt(c1,t.translation());
}

BOOST_AUTO_TEST_CASE(apply_transform)
{
  //non-random transform
  Quaternion q(sqrt(0.5),0,0,sqrt(0.5)); //z 90
  Transform nr(q, make_float3(0,1,1), make_float3(2,0,-3));

  //random
  Transform r(make_float3(0,1,1), 10.0, true);

  float coord_data[8][3] = { {0,0,0},
                         {1,0,0},
                         {0,1,0},
                         {0,0,1},
                         {-1,.5,3},
                         {1,1,1},
                         {0,1,1},
                         {.333,.75,-9}
  };
  float buffer[8][3] = {0,};

  Grid2f coords((float*)coord_data, 8, 3);
  Grid2f coords2((float*)buffer, 8, 3);

  //does nr perform as expected?
  nr.forward(coords,coords2);
  float3 expected = make_float3(2,1,-2);
  eqPt(coords2[6],expected); //at center

  expected = make_float3(2,1,-3);
  eqPt(coords2[2],expected); //on z-axis

  expected = make_float3(2,2,-2);
  eqPt(coords2[5],expected);

  //make sure input unchanged
  expected = make_float3(0.333,.75,-9);
  eqPt(coords[7],expected);

  //does random work both ways
  r.forward(coords,coords2);
  for(unsigned i = 0; i < 8; i++) {
    neqPt(coords[i],coords2[i]);
  }

  r.backward(coords2,coords2);
  for(unsigned i = 0; i < 8; i++) {
    eqPt(coords[i],coords2[i]);
  }
}
