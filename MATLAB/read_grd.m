% read grd file (.xyz)
function [lon, lat, ele] = read_grd(fgrd, lat_rng, lon_rng)
    f = load(fgrd);
    lon = f(:,1);
    lat = f(:,2);
    ele = f(:,3);
    slice_idx = lat>lat_rng(1) & lat<lat_rng(2) & lon>lon_rng(1) & lon<lon_rng(2);
    lat = lat(slice_idx);
    lon = lon(slice_idx);
    ele = ele(slice_idx);
end