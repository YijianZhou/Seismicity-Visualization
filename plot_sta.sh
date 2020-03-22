#!/bin/sh
R="102.4/104/24.25/26.6"
J="M10c"
fout="output/zsy_sta.ps"
grd="/home/zhouyj/GMT_data/earth_relief_15s.grd"
org_cpt="topo"
cpt="input/zsy.cpt"
fault='/home/zhouyj/GMT_data/CN-faults.dat'
# inputs
event1="input/zsy_pad_reloc"
fm1="input/xj_fm.gmt"
sta_loc1="input/zsy_loc"
sta_loc2="input/yn_loc"
sta_name1="input/zsy_name"
sta_name2="input/yn_name"

# start gmt
gmt psxy -R$R -J$J -T -K > $fout
gmt psbasemap -R -J -B0.5 --MAP_FRAME_WIDTH=4p -K -O >> $fout
gmt makecpt -C$org_cpt -T-4000/5000/1 > $cpt
gmt grdimage $grd -R -J -C$cpt -I -K -O >> $fout
gmt psxy -R -J -W1.0p,black $fault -K -O >> $fout

# plot fm
gmt psmeca $fm1 -R -J -Sa0.5c -K -O >> $fout
# plot events
awk '{print $1,$2,(1+$3)*0.04}' $event1 | gmt psxy -R -J -Sc -Gdarkred -W0.2p -K -O  >> $fout
# plot stations
gmt psxy $sta_loc1 -R -J -St0.4c -Gblue -K -O >> $fout
#gmt pstext $sta_name1 -R -J -F+f14p,1,black+jTL -K -O >> $fout
gmt psxy $sta_loc2 -R -J -Si0.4c -Gred -K -O >> $fout
#gmt pstext $sta_name2  -R -J -F+f14p,1,black+jTL -K -O >> $fout

#end gmt
gmt psxy -R -J -T -O >>$fout
rm gmt*
