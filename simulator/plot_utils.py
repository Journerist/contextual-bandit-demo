import matplotlib.pyplot as plt
import numpy as np

def plot_array_data(data_arr, title):

    y = moving_average(data_arr, 200)

    x = list(range(1,len(y)+1))


    
    # plotting the points
    plt.plot(x, y)
    
    # naming the x axis
    plt.xlabel('x - axis')
    # naming the y axis
    plt.ylabel('y - axis')
    
    # giving a title to my graph
    plt.title(title)
    
    # function to show the plot
    plt.show()

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w