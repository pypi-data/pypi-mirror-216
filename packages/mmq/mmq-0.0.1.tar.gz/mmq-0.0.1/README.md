# MMQ (Least Squares method) Package

## Description
The function takes a set of 2-D points **(np.array)** and returns the coefficients of the function that best fits the points, using the Least Squares method.
User needs to provide the function degree (1 for linear, 2 for quadratic, etc.) and the points (x and y) as np.arrays.

Maybe, for high degree functions, the function will face some problems. Be careful.

## Installation
```bash
pip install mmq
```

## Requirements
- numpy

## Usage
```python
from mmq import metodo_minimos_quadrados
metodo_minimos_quadrados.mmq(x, y, degree)
```

## Example
```python
from mmq import metodo_minimos_quadrados
import numpy as np

x = np.array([1, 2, 3, 4, 5])
y = np.array([1, 3, 5, 7, 9])
degree = 1

metodo_minimos_quadrados.mmq(x, y, degree)
```

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Author
[Igor Matheus Jasenovski]

## Version
0.0.1

## References
[Least Squares Method](https://en.wikipedia.org/wiki/Least_squares)