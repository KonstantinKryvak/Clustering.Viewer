
"""Виконує рекурсивний пошук усіх модулів, що містять функції `Algorithm` або `DistanceMetric`."""

import os, sys, importlib.util, ntpath

def WalkTheRoad(path):
    visited = set()
    def Walk(path):
        try:
            st = os.stat(path)  # follows symlinks
        except OSError as e:
            print(f"Skipping {path!r}: {e}", file=sys.stderr)
            return

        key = (st.st_dev, st.st_ino)
        if key in visited:
            return

        visited.add(key)

        if os.path.isdir(path):
            try:
                for entry in os.scandir(path):
                    yield from Walk(entry.path)
            except OSError as e:
                print(f"Cannot access directory {path!r}: {e}", file=sys.stderr)
        else:
            yield path

    yield from Walk(path)


try:
    for filepath in WalkTheRoad('./Algorithms'):
        tail:str = ntpath.split(filepath)[1]
        
        if tail.endswith('.py') and tail not in ['__init__.py', '__main__.py']:
            
            if globals().setdefault('Algorithms', {}).get(tail[:-3]) or globals().setdefault('DistanceMetrics', {}).get(tail[:-3]):
                continue

            module = os.path.splitext(os.path.relpath(filepath, './Algorithms'))[0].replace(os.sep, '_')
            spec = importlib.util.spec_from_file_location(module, filepath)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                
                try:
                    spec.loader.exec_module(module)
                except:
                    continue

                address = getattr(module, 'Algorithm', None)
                if callable(address):
                    globals().setdefault('Algorithms', {})[tail[:-3]] = address
                else:
                    address = getattr(module, 'DistanceMetric', None)
                    if callable(address):
                        globals().setdefault('DistanceMetrics', {})[tail[:-3]] = address

    globals().setdefault('Algorithms',      None)
    globals().setdefault('DistanceMetrics', None)

except Exception as error:
    print(error)


