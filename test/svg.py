import pandas as pd
import matplotlib.pyplot as plt
for r in [16,32,64]:
    plt.plot(range(r))
    plt.ylabel('some numbers')
    plt.savefig(f'line{r}.svg')


