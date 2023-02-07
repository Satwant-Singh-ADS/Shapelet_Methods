from transformation_defs import *
#%%
time_series = [ 347873,  379981,  408488,  446443,  452351,  423100,
        388181,  343304,  314540,  290811,  273840,  272592,
        280230,  299329,  321059,  349835,  414934,  500665,
        642533,  830546, 1033438, 1144914, 1262889, 1365306,
       1492764, 1456160, 1452552, 1518310, 1593263, 1483297,
       1250532, 1015500,  832722,  641966,  525904,  452068,
        422603,  391484,  400992,  424949,  460410,  469997,
        456936,  408827,  346896,  288361,  232440,  183767,
        139974,  114176,   94157,   89204,   85818,  105950,
        154609,  247571,  390043,  567394,  751642,  908103,
       1018844, 1097530, 1092602, 1071038,  968568,  877159,
        752011,  666283,  582269,  536468,  511297,  532844,
        578161,  574516,  672099,  734423,  880669, 1059553,
       1720036 ]

reps = find_shapelet_space_ts(time_series, 100000) # 100,000 cases per week to be consdiered low flatness (\phi = 0.1)

fig, ax  = plt.subplots(2, 2, sharex='col', gridspec_kw={'width_ratios':[100,5]})
ax[0,1].remove()
ax[0,0].plot(time_series)
# permuting the dimensions to improve visualization
perm_shapes = [3, 1, 5, 0, 4, 2] # surge, inc, peak
rep_perm = reps[perm_shapes, :]
plt.figure()
sns.heatmap(rep_perm,cmap="hot", square=False, ax=ax[1,0], cbar_ax=ax[1,1])
