clear;
zero_date = datetime(2021, 9, 1);
min_date = datetime(2022, 9, 1);
abvs = readcell('us_states_abbr_list.txt');
st = readcell('us_states_list.txt');
fips_tab = readtable('reich_fips.txt', 'Format', '%s%s%s%d');
ns = length(abvs);
fips = cell(ns, 1);
for cid = 1:length(abvs)
    fips(cid) = fips_tab.location(strcmp(fips_tab.abbreviation, abvs(cid)));
end

source_path = 'Z:\Research\Flusight-forecast-data\data-forecasts';
dest_path = 'C:\Users\Batman\repos\Shapelet_Methods\Classification_task\Data_Sources\Flu-2023';
%%


D = dir(source_path); % A is a struct ... first elements are '.' and '..' used for navigation.
for k=3:length(D) % avoid using the first ones
    currD = D(k).name; % Get the current subdirectory name
    if currD == "README.md" || currD == "format_data.m" || currD == "METADATA.md"
%         currD
        continue;
    end
    % Run your function. Note, I am not sure on how your function is written,
    % but you may need some of the following
    %cd(currD) % change the directory (then cd('..') to get back)
    fList = dir([source_path '\' currD]); %(currD); % Get the file list in the subdirectory
    fList = fList(3:end);
    for i=1:numel(fList)
        if fList(i).name(end-2:end) ~= "csv" || fList(i).name(1) ~= '2'
            continue;
        end
        if days(datestr(fList(i).name(1:10)) - min_date) < 0
            continue;
        end

        data = readtable([source_path '\' currD '\' fList(i).name]);
        date = data.forecast_date(1);
        day = days(date-zero_date); 

%         indx1 = data.target == "1 wk ahead inc flu hosp" & data.type == "point";
%         indx2 = data.target == "2 wk ahead inc flu hosp" & data.type == "point";
%         indx3 = data.target == "3 wk ahead inc flu hosp" & data.type == "point";
%         indx4 = data.target == "4 wk ahead inc flu hosp" & data.type == "point";
%         
%         if(sum(indx1)==9)
        indx1 = data.target == "1 wk ahead inc flu hosp" & data.quantile == 0.5;
        indx2 = data.target == "2 wk ahead inc flu hosp" & data.quantile == 0.5;
        indx3 = data.target == "3 wk ahead inc flu hosp" & data.quantile == 0.5;
        indx4 = data.target == "4 wk ahead inc flu hosp" & data.quantile == 0.5;
%         end
        if(sum(indx1)==0)
            continue;
        end

        data_1 = data(indx1,:);
        data_2 = data(indx2,:);
        data_3 = data(indx3,:);
        data_4 = data(indx4,:);
        if(sum(indx4)==0)
            data_4 = array2table(nan(1,7));
            data_4.Properties.VariableNames("Var7") = "value";
        end
        
        data_temp = array2table(zeros(0,7));
        data_temp.Properties.VariableNames = {'id','State',int2str((day-1)+1),int2str((day-1)+7), int2str((day-1)+14),int2str((day-1)+21),int2str((day-1)+28)};
        for l =1:height(data_1)
            if isnumeric(data_1.location(l))
                idS = int2str(data_1.location(l));
            else
                idS = data_1.location(l);
            end
            ab = "US";
            if idS~="US" && idS~="NaN"
                if strlength(idS) == 1
                    id = find(ismember(fips, "0"+idS))-1;
                else
                    id = find(ismember(fips, idS))-1;
                end
                ab = convertCharsToStrings(st{id+1});
            else
                id = "US";
            end
            t = table(id,ab,0,data_1.value(l),data_2.value(l),data_3.value(l),data_4.value(1), ...
                'VariableNames',{'id','State',int2str((day-1)+1),int2str((day-1)+7), int2str((day-1)+14),int2str((day-1)+21),int2str((day-1)+28)});
            data_temp = [data_temp;t];
        end
        fullpath = [dest_path '\' currD];
        if ~exist(fullpath, 'dir')
            mkdir(fullpath);
        end
        writetable(data_temp, [fullpath '\' currD '_' num2str(day) '.csv']);
        %strfind(fips, "0"+int2str(6))
    end
    fprintf('.')
end