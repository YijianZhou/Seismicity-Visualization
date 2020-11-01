#!/bin/sh
R="101.4/103.4/28/30"
J="M14c"
fout="output/example_sta.ps"
grd="/home/public/GMT_data/earth_relief_15s.grd"
org_cpt="topo"
cpt="input/example.cpt"
fault='/home/public/GMT_data/CN-faults.dat'
sta_loc="input/sta_loc_example"
sta_name="input/sta_name_example"
events="input/catalog_example"

# prep input
sh csv2gmt.sh

# start gmt
gmt psxy -R$R -J$J -T -K > $fout
gmt psbasemap -R -J -B1 --MAP_FRAME_WIDTH=4p -K -O >> $fout
gmt makecpt -C$org_cpt -T-6000/6000/1 > $cpt
gmt grdimage $grd -R -J -C$cpt -I -K -O >> $fout
gmt psxy -R -J -W1.0p,black $fault -K -O >> $fout

# plot station
gmt psxy $sta_loc -R -J -St0.4c -Gblue -K -O >> $fout
gmt pstext $sta_name -R -J -F+f14p,1,black+jTL -K -O >> $fout
# plot events
awk '{print $1,$2,($3+1)*0.03}' $events | gmt psxy -R -J -Sc -Gdarkred -K -O  >> $fout

#end gmt
gmt psxy -R -J -T -O >>$fout
rm gmt*
