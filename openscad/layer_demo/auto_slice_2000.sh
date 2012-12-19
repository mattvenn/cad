#!/bin/bash
#don't know how to do this in openscad, so with a shell script instead,
#we export each layer in turn
for i in $(seq 0 1 34); do
  echo $i
  openscad -D 'import_slices=false' -D 'make_can=false' -D 'slice_can=false' -D 'get_single_slice=true' -D "cut_level=$i" layer_demo.scad -o layer$i.dxf
done
