% plot seis 3d
% read file
lat_rng = [28.6, 30];
lon_rng = [101.8, 102.6];
dep_rng = [0, 40];
[grd_lon, grd_lat, grd_ele] = read_grd('input\azf_grd.xyz', lat_rng, lon_rng);
grd_ele = grd_ele / 1000; % to km 
[lat, lon, dep, mag] = read_catalog('input\ok_reloc.csv', lat_rng, lon_rng, dep_rng);
dep = -dep;
mag = 2 * (mag+2); % marker size
faults = read_fault('input\AZF_faults.dat', lat_rng, lon_rng);

% start plot
figure
% plot grd
cmap = load('C:\Users\zhouyj\MATLAB\ColorMaps\gist_earth.mat').gist_earth;
T=delaunay(grd_lon, grd_lat);
grd = trisurf(T, grd_lon, grd_lat, grd_ele);
colormap(cmap); 
set(grd, 'EdgeColor', 'none');
set(grd, 'FaceAlpha', 0.8);
hold on

% plot seis
seis = scatter3(lon, lat, dep, mag, 'filled');
set(seis, 'MarkerEdgeColor', 'none');
set(seis, 'MarkerFaceColor', '#A2142F');
hold on

% plot faults
for ii = 1:length(faults)
    fault = faults{ii};
    lon = [fault(:,1), fault(:,1)];
    lat = [fault(:,2), fault(:,2)];
    dep = [zeros(length(fault),1), -dep_rng(2)*ones(length(fault),1)];
    fault_plane = mesh(lon, lat, dep);
    set(fault_plane, 'EdgeColor', 'none');
    set(fault_plane, 'FaceColor', [0, 0.4470, 0.7410]);
    set(fault_plane, 'FaceAlpha', 0.4);
    hold on
    plot3(lon(:,1), lat(:,1), dep(:,1), 'black')
end
caxis([-2,5])
