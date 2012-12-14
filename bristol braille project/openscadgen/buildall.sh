#!/bin/bash
dir="builddxf"
openscad makeall.scad -D 'export_slider_holder=true' -D 'build_slider_num=1' -x $dir/slider_holder_1.dxf
openscad makeall.scad -D 'export_slider_holder=true' -D 'build_slider_num=2' -x $dir/slider_holder_2.dxf
openscad makeall.scad -D 'export_base=true' -x $dir/base.dxf
openscad makeall.scad -D 'export_comb=true' -x $dir/comb.dxf
openscad makeall.scad -D 'export_lid=true' -x $dir/lid.dxf
openscad makeall.scad -D 'export_side=true' -x $dir/side.dxf
openscad makeall.scad -D 'export_pin_slider=true' -x $dir/pin_slider.dxf
