% read catalog
function [lat, lon, dep, mag] = read_catalog(fctlg, lat_rng, lon_rng, dep_rng)
    f = load(fctlg);
    lat = f(:,2);
    lon = f(:,3);
    dep = f(:,4);
    mag = f(:,5);
    slice_idx = lat>lat_rng(1) & lat<lat_rng(2) & lon>lon_rng(1) & lon<lon_rng(2) & dep>dep_rng(1) & dep<dep_rng(2);
    lat = lat(slice_idx);
    lon = lon(slice_idx);
    dep = dep(slice_idx);
    mag = mag(slice_idx);
end