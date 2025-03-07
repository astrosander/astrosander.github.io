import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def analyze_data_lsq(csv_filename):
    data = pd.read_csv(csv_filename, encoding="latin1") 

    x = data.iloc[:, 0].values 
    y = data.iloc[:, 1].values 
    
    a, b = np.polyfit(x, y, 1)
    
    y_pred = a * x + b

    residuals = y - y_pred
    n = len(x)
    
    ss_res = np.sum(residuals ** 2)

    s_yx = np.sqrt(ss_res / (n - 2))

    S_xx = np.sum((x - np.mean(x))**2)
    SE_a = s_yx / np.sqrt(S_xx)
    SE_b = SE_a * np.sqrt(np.sum(x**2) / n)
    
    ss_tot = np.sum((y - np.mean(y))**2)
    r2 = 1 - (ss_res / ss_tot)
    
    print(f"Slope (a): {a:.6f} ± {SE_a:.6f}")
    print(f"Intercept (b): {b:.6f} ± {SE_b:.6f}")
    print(f"Mean Squared Error: {ss_res / n:.8f}")
    print(f"R^2: {r2:.4f}")
    
    plt.figure()
    plt.scatter(x, y, label='Data Points', color='black')
    plt.plot(x, y_pred, label='Fitted Line', color='red')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Least Squares Linear Regression')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    csv_filename = "raw_data.csv"
    analyze_data_lsq(csv_filename)