//defined
//important stuff
thickness=3.2; //material thickness
pitch = 3.25; 
y_pitch = 2.5;
letters = 2;
min_spacing=2;
slider_solenoid_z_spacing = min_spacing;
edge_margin = 15;
spindle_radius = 1.5;
rotor_spindle_radius = 1.5;
rotor_thickness=2;
pin_radius=1;
pin_length=20;
rotor_diameter=8.8; //rotor diamter
smooth=10; //global smooth for small cylinders
bolt_radius=4.7/2;
beam_width = 0.15; //laser beam width
//solenoids
solenoid_length = 10.0;
solenoid_width= 10.8 - beam_width;
solenoid_height=20.6 - beam_width;
solenoid_plunger_radius=1.5;
solenoid_plunger_length=8;
solenoid_min_x_spacing=min_spacing; //minimum gap we can have between adjacent solenoids
solenoid_min_y_spacing=solenoid_height+solenoid_plunger_length+4*min_spacing; //minimum gap we can have between adjacent solenoids


//solenoids
num_solenoids = 2 * letters;
solenoid_rows = round((solenoid_width+solenoid_min_x_spacing) / pitch);
solenoid_columns = round(num_solenoids/solenoid_rows);
solenoid_total_y = solenoid_rows*(solenoid_min_y_spacing);
//solenoid_total_x = pitch*(solenoid_rows-1); // +solenoid_columns*(solenoid_length+pitch);
solenoid_x_spacing = solenoid_rows*pitch-solenoid_width;
solenoid_total_x = solenoid_columns*(solenoid_x_spacing+solenoid_width)-solenoid_x_spacing+(solenoid_rows-1)*pitch; //num_solenoids*pitch;
plunger_hole_distance=4.3; //distance from the top of the solenoid to the center of the plunger hole, when fully retracted

//sliders
slider_width=2;
slider_length=solenoid_total_y;
slider_height=10;
slider_move_length=2;
slider_move_height=2;
slider_pin_offset=plunger_hole_distance+slider_move_length; //distance we want the slider pin

//base
base_width=solenoid_total_x+2*edge_margin;
base_length=solenoid_total_y+2*edge_margin;
base_height=solenoid_length+slider_height+min_spacing+slider_move_height+slider_solenoid_z_spacing+min_spacing+pin_length;
pin_slider_move_height=2;

//comb
comb_width=num_solenoids*pitch+rotor_thickness+min_spacing*2;
comb_length=solenoid_min_y_spacing;

//pin slider
pin_slider_width=base_width+thickness*2;
