from imageio import imread
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as plticker
from matplotlib.colors import to_hex

filename = 'titlescreen-1to1-staredited'
colourkey = {
    '#000000': ('K', '#cecece'),
    '#555555': ('G', '#efefef'),
    '#aaaaaa': ('g', '#1c1c1c'),
    '#ffffff': ('W', '#000000'),
    '#0000aa': ('B', '#ffffff'),
    '#5555ff': ('b', '#ffffff'),
    '#00aaaa': ('T', '#ffffff'),
    '#55ffff': ('t', '#000000'),
    '#ffff55': ('Y', '#000000'),
    '#aa5500': ('C', '#000000'),
    '#aa00aa': ('V', '#000000'),
    '#ff5555': ('P', '#000000')
}
pagewidth = 50    # stitches
pageheight = 80    # stitches

imgarray = imread(filename+".png", pilmode="RGB")

pixelCount = {}
for i in range(imgarray.shape[0]):
    for j in range(imgarray.shape[1]):
        hexvalue = to_hex(imgarray[i, j]/255.0)
        
        if hexvalue not in colourkey:
            print("No symbol found for colour " + hexvalue)
            print("Going to exit without output")
            exit()

        if hexvalue not in pixelCount:
            pixelCount[hexvalue] = 1
        else:
            pixelCount[hexvalue] = pixelCount[hexvalue] + 1
        

for colour, count in pixelCount.items():
    print(colourkey[colour][0] + ": " + str(count))

counter = 0
#fig = plt.figure(figsize=(0.2*pagewidth, 0.2*pageheight))
for min_x in range(0, imgarray.shape[1], pagewidth):
    for min_y in range(0, imgarray.shape[0], pageheight):
        counter += 1

        plotarea = imgarray[min_y : min_y + pageheight,
                                min_x : min_x + pagewidth]

        imgplot = plt.imshow(plotarea)

        fig = plt.gcf()
        ax = plt.gca()

        ax.grid(True)
        ax.grid(b=True, which='major', color='0.95', linestyle='-', linewidth=2.0)
        plt.minorticks_on()
        ax.grid(b=True, which='minor', color='0.7', linestyle='-', linewidth=1.0)

        if min_y + pageheight <= imgarray.shape[0]:
            max_y = min_y + pageheight
        else:
            max_y = imgarray.shape[0]

        if min_x + pagewidth <= imgarray.shape[1]:
            max_x = min_x + pagewidth
        else:
            max_x = imgarray.shape[1]
    
        height = max_y - min_y
        width = max_x - min_x

        fig.set_size_inches(0.22*width, 0.22*height)

        ax.tick_params('both', top = True, right = True)
        ax.tick_params('both', labeltop = True, labelright = True)

        # put a major gridline every 5 pixels
        ax.set_xticks(np.arange(-0.5, width + 1, 5))
        ax.set_yticks(np.arange(-0.5, height + 1, 5))

        # set ticks label
        ax.set_xticklabels(np.arange(min_x, max_x + 1, 5))
        ax.set_yticklabels(np.arange(min_y, max_y + 1, 5))

        # put a minor gridline every pixel
        ax.set_xticks(np.arange(-0.5, width, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, height, 1), minor=True)
        fig.tight_layout(pad=0)  # reduce space around image

        for i in range(plotarea.shape[0]):
            for j in range(plotarea.shape[1]):
                hexvalue = to_hex(plotarea[i, j]/255.0)
                ax.text(j, i, colourkey.get(hexvalue)[0], color=colourkey.get(hexvalue)[1],
            horizontalalignment='center', verticalalignment='center',
            fontsize=9)


        fig.savefig(filename + "-" + str(counter) + ".pdf", bbox_inches='tight')
        plt.cla()
        plt.clf()
