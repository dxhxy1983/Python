import numpy as np
import pandas as pd
import cufflinks as cf
import plotly.offline as plyo
import plotly.graph_objects as go

# Initialize Plotly notebook mode
plyo.init_notebook_mode(connected=True)

# Create random data
a = np.random.standard_normal((250, 5)).cumsum(axis=0)
index = pd.date_range('2019-1-1', freq='B', periods=len(a))
df = pd.DataFrame(100 + 5 * a, columns=list('abcde'), index=index)

# Plot the DataFrame and get the figure
fig = df.iplot(asFigure=True)

# Save the plot as a PNG file
fig.write_image("ply_01.png")
