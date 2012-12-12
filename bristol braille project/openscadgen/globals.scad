//defined
//important stuff
thickness=3; //material thickness
pitch = 3.25; 
letters = 1;
slider_solenoid_z_spacing = 2;
min_spacing=2;
edge_margin = 15;
spindle_radius = 1.5;
rotor_thickness=2;
comb_length=40;
pin_radius=1;
pin_length=20;
rotor_diameter=8.8; //rotor diamter
smooth=10; //global smooth for small cylinders

//solenoids
solenoid_length = 12.6;
solenoid_width= 10.6;
solenoid_height=20.6;
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

//sliders
slider_width=2;
slider_length=solenoid_total_y;
slider_height=10;
slider_move_length=2;
slider_move_height=2;
pin_slider_move_height=2;

//base
bolt_radius=2.0;
base_width=solenoid_total_x+2*edge_margin;
base_length=solenoid_total_y+2*edge_margin;
base_height=solenoid_length+slider_height+min_spacing+slider_move_height+min_spacing+min_spacing+pin_length;

//comb
comb_width=num_solenoids*pitch+rotor_thickness+min_spacing*2;

//pin slider
pin_slider_width=base_width+thickness*2;
