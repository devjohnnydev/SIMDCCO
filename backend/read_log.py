try:
    with open('debug_output_clean.txt', 'r', errors='ignore') as f:
        lines = f.readlines()
        print("".join(lines[-100:]))
except Exception as e:
    print(e)
