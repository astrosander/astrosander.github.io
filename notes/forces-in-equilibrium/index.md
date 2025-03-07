
__NO: The Excel analysis & ploting data available here: [experimental_analysis.xlsx](experimental_analysis.xlsx) and [raw_data.csv](raw_data.csv)__

The equlibtium equation

$$
2mg\cos\theta = Mg \to \cos\theta = \frac{M}{2m}
$$
From the geometry:

$$
\cos\theta = \frac{y}{(L/2)^2+y^2} = \frac{M}{2m}
$$
Let's introduce the indementional variable

$$
\mu = \frac{M}{m}
$$
Then, 

$$
\frac{y}{(L/2)^2+y^2} = \frac{\mu}{2}
$$
From here,

$$
\boxed{y=L\frac{\mu}{2\sqrt{4-\mu ^2}}}
$$

The graph of the following function ([theoretical_plot.py](theoretical_plot.py)):

<center>
![Figure_1.png](Figure_1.svg)
</center>

The possible linearization gives:
$$
\frac{1}{y^2}=\frac{16}{L^2}\frac{1}{\mu ^2} - \frac{4}{L^2}
$$
We will use linear regression to compare theory with the experiment, using the Least Square Method for the equation $Y=BX+A$
where
$$
Y=\frac{1}{y^2}, ~B=\frac{16}{L^2},~X=\frac{1}{\mu^2},~A=-\frac{4}{L^2}
$$

The linearizated plot ([least_square_method.py](least_square_method.py))

<center>
![Figure_2.png](Figure_2.svg)
</center>

The coefficients calculated with the least square method gives:
$$
B= 0.004262 ± 0.000045
$$
$$
A= -0.001129 ± 0.000099
$$
And the correlation coefficient became close to 1: $R^2= 0.9994$
