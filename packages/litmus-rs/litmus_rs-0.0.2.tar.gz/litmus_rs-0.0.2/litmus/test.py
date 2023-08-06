import litmus_rs
from tqdm import tqdm

iterations = 1000000

def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

for i in tqdm(range(iterations)):
    litmus_rs.fibonacci(16)

for i in tqdm(range(iterations)):
    fibonacci(16)

