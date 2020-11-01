% read fault file
function faults = read_fault(fpath, lat_rng, lon_rng)
    f = fopen(fpath);
    faults = {};
    fault_idx = 1;
    point_idx = 1;
    line = fgetl(f);
    while ischar(line)
        if line(1)=='#'
            line = fgetl(f); 
            continue
        elseif line(1)=='>'
            if isempty(faults)
                line = fgetl(f); 
                continue
            elseif length(faults{length(faults)})>2
                fault_idx = length(faults) + 1;
            else
                fault_idx = length(faults);
                faults{fault_idx} = [];
            end
            point_idx = 1;
            line = fgetl(f); 
            continue
        end
        % read fault points
        line = split(line);
        lon = str2double(cell2mat(line(1)));
        lat = str2double(cell2mat(line(2)));
        if lat<lat_rng(1) || lat>lat_rng(2) || lon<lon_rng(1) || lon>lon_rng(2)
            line = fgetl(f); 
            continue
        end
        faults{fault_idx}(point_idx,:) = [lon, lat];
        point_idx = point_idx + 1;
        line = fgetl(f); 
    end
    if length(faults{length(faults)})<=2
        faults = faults(1:length(faults)-1);
    end
end